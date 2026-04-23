from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category_Name', unique=True)
    img = models.ImageField(blank=True, upload_to='images/category')
    slug = models.SlugField(
        unique=True, null=True, blank=True, verbose_name='путь', 
        help_text='оно автоматически дополняет когда вы пишите имя категории'
        )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = "Категории"

class Hashtag(models.Model):
    name = models.CharField(max_length=255)
    slug =  models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
            verbose_name = 'Хэштег'
            verbose_name_plural = "Хэштеги"
class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True,
        related_name='articles', verbose_name='Категория'
    )
    title = models.CharField(max_length=255)
    description = CKEditor5Field('Описание', config_name='extends')
    img = models.ImageField(blank=True, upload_to='images')
    data = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)
    tag = models.ManyToManyField(Hashtag, blank=True,
    related_name='hashtags', verbose_name='Хэштеги')

    def __str__(self):
        return f'ID:{self.id} - Name: {self.title}'

    class Meta:
        verbose_name = 'Артикль'
        verbose_name_plural = "Артикли"
        ordering = ['-id']
    
class Comments(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='comments', null=True
    )
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} {self.article.title}'
    
    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='favorites' 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Избранные'
        verbose_name = 'Избранное'
        unique_together = ('user', 'article')

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='likes', null=True
        )
    # created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Лайки'
        verbose_name = 'Лайк'
        unique_together = ('user', 'article')