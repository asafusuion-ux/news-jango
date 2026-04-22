from modeltranslation.translator import register, TranslationOptions
from post.models import Article, Hashtag, Category
@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ['title']
@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['name']
@register(Hashtag)
class HashtagTranslationOptions(TranslationOptions):
    fields = ['name']