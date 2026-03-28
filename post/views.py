from django.shortcuts import render
from post.models import Article
from post.models import Category

def index(request):
    articles = Article.objects.all()
    context = {
        'articles':articles
    }
    return render(request, 'index.html', context)

def category(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'categories.html', context)
