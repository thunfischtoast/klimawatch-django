from django.http import HttpResponse
from django.template import loader

from .models import Kommune, Article


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
    template = loader.get_template("kommune_detail.html")
    kommune = Kommune.objects.get(slug=municipality_slug)
    article = Article.objects.filter(kommune=kommune).first()
    return HttpResponse(
        template.render(
            request=request, context={"kommune": kommune, "article": article}
        )
    )
