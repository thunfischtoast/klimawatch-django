from django.contrib import admin


from .models import Kommune, MarkdownContent, EmissionData

admin.site.register(Kommune)
admin.site.register(MarkdownContent)
admin.site.register(EmissionData)
