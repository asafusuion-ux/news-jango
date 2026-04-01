from django.shortcuts import render, get_object_or_404
from post.models import Article, Category 


def index(request):
    articles = Article.objects.all()
    context = {
        'articles':articles
    }
    return render(request, 'index.html', context)



def post_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {
        'article':article
    }
    return render(request, 'post-detail.html', context)