import json

import markdown
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import EmissionData, Kommune, MarkdownContent


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


def kommune_detail(request, municipality_slug):
    md = markdown.Markdown(extensions=["fenced_code"])

    template = loader.get_template("kommune_detail.html")
    kommune = Kommune.objects.get(slug=municipality_slug)
    markdown_content = MarkdownContent.objects.filter(kommune=kommune).first()
    markdown_content.content = md.convert(markdown_content.content)

    rendered_content = template.render(
        request=request,
        context={"kommune": kommune, "markdown_content": markdown_content},
    )

    if "{{ youdrawit }}" in markdown_content.content:
        youdrawit_template = loader.get_template("youdrawit.html")
        youdrawit_content = (
            f"<div id=youdrawitroot>{youdrawit_template.render(request=request)}</div>"
        )
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

    return HttpResponse(template.render(request=request, context={"kommune": kommune, "data": data}))


@csrf_exempt
def emission_data(request, municipality_slug):
    if request.method == "POST":
        data = json.loads(request.body)  # load json data from request
        kommune = Kommune.objects.get(slug=municipality_slug)
        EmissionData.objects.update_or_create(
            emissions=data, kommune=kommune
        )  # update or create data in model
        return JsonResponse({"status": "success"}, status=200)
    else:
        kommune = Kommune.objects.get(slug=municipality_slug)
        data = serializers.serialize(
            "json", EmissionData.objects.filter(kommune=kommune)
        )
        return JsonResponse({"status": "success", "data": data}, status=200)
