from django.contrib import admin
from post.models import Article, Category, Hashtag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug':('title',)}

@admin.register(Hashtag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug':('name',)}