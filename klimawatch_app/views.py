from django.http import HttpResponse
from django.template import loader
import markdown


from .models import Kommune, MarkdownContent


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

    return HttpResponse(
        template.render(
            request=request,
            context={"kommune": kommune, "markdown_content": markdown_content},
        )
    )
