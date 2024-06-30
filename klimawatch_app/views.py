import datetime
import json

import markdown
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.forms.models import model_to_dict
from scipy import interpolate

from .models import EmissionData, Kommune, MarkdownContent, Action


def index(request):
    template = loader.get_template("index.html")
    kommunen_list = Kommune.objects.all()
    return HttpResponse(
        template.render(request=request, context={"kommunen_list": kommunen_list})
    )


def paris_limits(request):
    template = loader.get_template("paris-limits.html")
    return HttpResponse(template.render(request=request))


def anleitung(request):
    template = loader.get_template("anleitung.html")
    return HttpResponse(template.render(request=request))


def actions(request, municipality_slug):
    template = loader.get_template("actions.html")
    kommune = Kommune.objects.get(slug=municipality_slug)

    if kommune is None:
        return HttpResponse("Kommune not found")

    actions = Action.objects.filter(kommune=kommune).all()

    # if no actions are found
    if actions is None:
        return HttpResponse("No actions found")

    # create dict that maps fields to actions
    fields = list({action.field for action in actions})
    field_to_actions = {field.name: [] for field in fields}
    for action in actions:
        action_field_name = action.field.name
        # append action as dict
        field_to_actions[action_field_name].append(model_to_dict(action))

    return HttpResponse(
        template.render(
            request=request,
            context={"kommune": kommune, "actions": field_to_actions, "fields": fields},
        )
    )


def kommune_detail(request, municipality_slug):
    md = markdown.Markdown(extensions=["fenced_code"])

    template = loader.get_template("kommune_detail.html")
    kommune = Kommune.objects.get(slug=municipality_slug)
    markdown_content = MarkdownContent.objects.filter(kommune=kommune).first()
    markdown_content.content = md.convert(markdown_content.content)

    emission_data = EmissionData.objects.filter(kommune=kommune).first()
    if emission_data:
        data = emission_data.emissions
        # print(data)
        years = [int(timepoint[0]) for timepoint in data]
        values = [float(timepoint[3]) for timepoint in data]
    else:
        years = [2000, 2010, 2020]
        values = [1000, 1500, 700]

    arr = np.array([years, values])
    # remove all years after the current year
    currentyear = datetime.datetime.now().year
    minyear = arr[0].min() if arr.size > 0 else 0
    # round up to next 5 year interval
    minyear = int(minyear + 5 - minyear % 5)
    arr = arr[:, arr[0] <= currentyear]

    # add 2035 with value 0
    arr = np.append(arr, [[2035, 2050], [0, 0]], axis=1)

    # interpolate to 5 year intervals, until 2050
    x = arr[0]
    y = arr[1]
    f = interpolate.interp1d(x, y, kind="linear")
    xnew = np.arange(minyear, 2051, 5)
    ynew = f(xnew)
    data = list(zip(xnew, ynew))
    data = [{str(timepoint[0]): timepoint[1]} for timepoint in data]
    lastshownyear = xnew[xnew <= currentyear][-1]

    rendered_content = template.render(
        request=request,
        context={
            "kommune": kommune,
            "markdown_content": markdown_content,
            "emissions": data,
            "lastshownyear": lastshownyear,
        },
    )

    if "{{ youdrawit }}" in markdown_content.content:
        youdrawit_template = loader.get_template("youdrawit.html")
        context = {"emissions": data, "lastshownyear": lastshownyear}
        youdrawit_content = f"<div id=youdrawitroot>{youdrawit_template.render(request=request, context=context)}</div>"
        rendered_content = rendered_content.replace(
            "{{ youdrawit }}", youdrawit_content
        )

    return HttpResponse(rendered_content)


def spreadsheet(request, municipality_slug):
    template = loader.get_template("spreadsheet.html")
    kommune = Kommune.objects.get(slug=municipality_slug)

    emission_data = EmissionData.objects.filter(kommune=kommune).first()

    if emission_data:
        data = emission_data.emissions
    else:
        data = []

    return HttpResponse(
        template.render(request=request, context={"kommune": kommune, "data": data})
    )


@csrf_exempt
def emission_data(request, municipality_slug):
    if request.method == "POST":
        data = json.loads(request.body)  # load json data from request
        kommune = Kommune.objects.get(slug=municipality_slug)
        emission_data, created = EmissionData.objects.update_or_create(
            kommune=kommune, defaults={"emissions": data}
        )  # update or create data in model
        return JsonResponse({"status": "success"}, status=200)
    else:
        kommune = Kommune.objects.get(slug=municipality_slug)
        data = serializers.serialize(
            "json", EmissionData.objects.filter(kommune=kommune)
        )
        return JsonResponse({"status": "success", "data": data}, status=200)
