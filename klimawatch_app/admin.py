from django.contrib import admin


from .models import Kommune
from .models import Article, ArticleContent, MarkdownContent

admin.site.register(Kommune)
admin.site.register(Article)
admin.site.register(ArticleContent)
admin.site.register(MarkdownContent)
