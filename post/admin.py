from django.contrib import admin
from post.models import Article
from post.models import Category

admin.site.register(Article)
admin.site.register(Category)