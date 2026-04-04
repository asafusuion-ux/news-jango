from django.shortcuts import render, get_object_or_404
from post.models import Article, Category, Hashtag
from django.db.models import Count
from django.core.paginator import Paginator

def index(request):
    articles = Article.objects.all()

    hashtags = Hashtag.objects.all()

    paginator = Paginator(articles, 3) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'page_obj':page_obj,
        'categories':categories,
        'hashtags':hashtags
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'article':article,
        'categories':categories
    }
    return render(request, 'post-detail.html', context)



def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)

    paginator = Paginator(articles, 3) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    context = {
        'category':category,
        'page_obj':page_obj,
        'categories':categories,
    }
    return render(request, 'category.html', context)