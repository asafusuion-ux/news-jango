from django.db import models


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

class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True,
        related_name='articles', verbose_name='Категория'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    img = models.ImageField(blank=True, upload_to='images')
    data = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)
    tag = models.ManyToManyField(Hashtag, blank=True, null=True,
    related_name='hashtags', verbose_name='Хэштеги')

    def __str__(self):
        return f'ID:{self.id} - Name: {self.title}'

    class Meta:
        verbose_name = 'Артикль'
        verbose_name_plural = "Артикли"
        ordering = ['-id']
    