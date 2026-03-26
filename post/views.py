from django.shortcuts import render
from post.models import Article


def index(request):
    articles = Article.objects.all()
    context = {
        'articles':articles
    }
    return render(request, 'index.html', context)