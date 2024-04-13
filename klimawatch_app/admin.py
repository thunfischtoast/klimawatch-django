from django.contrib import admin


from .models import Kommune
from .models import MarkdownContent

admin.site.register(Kommune)
admin.site.register(MarkdownContent)
