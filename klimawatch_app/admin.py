from django.contrib import admin


from .models import Kommune
from .models import Article, ArticleContent

admin.site.register(Kommune)
admin.site.register(Article)
admin.site.register(ArticleContent)