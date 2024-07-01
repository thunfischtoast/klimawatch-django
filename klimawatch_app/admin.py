from django.contrib import admin


from .models import (
    Kommune,
    MarkdownContent,
    EmissionData,
    ActionSource,
    ActionField,
    Action,
    ActionProgress,
)

admin.site.register(Kommune)
admin.site.register(MarkdownContent)
admin.site.register(EmissionData)
admin.site.register(ActionSource)
admin.site.register(ActionField)
admin.site.register(Action)
admin.site.register(ActionProgress)
