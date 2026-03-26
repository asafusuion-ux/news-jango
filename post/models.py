from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    img = models.ImageField(blank=True, upload_to='images')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title