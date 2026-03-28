from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category_Name', unique=True)
    img = models.ImageField(blank=True, upload_to='images/category')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name



class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True,
        related_name='articles', verbose_name='Category'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    img = models.ImageField(blank=True, upload_to='images')
    data = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f'ID:{self.id} - Name: {self.title}'