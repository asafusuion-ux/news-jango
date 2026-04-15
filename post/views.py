from django.shortcuts import render, get_object_or_404, redirect
from post.models import Article, Category, Hashtag, Comments
from django.db.models import Count, Q
from django.core.paginator import Paginator

def index(request):
    articles = Article.objects.all()
    hashtags = Hashtag.objects.all()

    paginator = Paginator(articles, 3) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # calculator start
    result = None
    if request.method == 'POST':
        a = request.POST.get('a')
        dollar = 87.2000
        euro = 101.8000
        tenge = 0.1800
        operation = request.POST.get('operation')
        if operation == 'dollar':
            result = str(round(int(a) / dollar, 2))+ ' dollar'
        if operation == 'euro':
            result = str(round(int(a) / euro, 2))+ ' euro'
        if operation == 'tenge':
            result = str(round(int(a) / tenge, 2)) + ' tenge'
    # calculator end
    context = {
        'page_obj':page_obj,
        'hashtags':hashtags,
        'result':result,
    }

    return render(request, 'index.html', context)



def search(request):
    query = request.GET.get('search', '')
    results = None
    if query:
        results = Article.objects.all()
        for word in query.split():
            results = results.filter(
                Q(title__icontains=word) |
                Q(description__icontains=word) |
                Q(category__name__icontains=word) |
                Q(tag__name__icontains=word) 
            ).distinct()
    else:
        results = Article.objects.none()
    paginator = Paginator(results, 3) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'results':results,
        'query': query,
    }
    return render(request, 'search.html', context)


def post_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        name = request.POST.get('name')
        text = request.POST.get('text')
        if name and text:
            Comments.objects.create(
                article=article,
                name=name,
                text=text,
            )
            return redirect('post_detail', slug=slug)
    comments = Comments.objects.all().order_by('-id')
    context = {
        'article':article,
        'comments':comments,
    }
    return render(request, 'post-detail.html', context)



def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)

    paginator = Paginator(articles, 3) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category':category,
        'page_obj':page_obj,

    }
    return render(request, 'category.html', context)

def hashtag_posts(request, pk):
    hashtag = get_object_or_404(Hashtag, pk=pk)
    articles = Article.objects.filter(tag=hashtag)

    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'hashtag': hashtag,
        'page_obj': page_obj,
    }
    return render(request, 'category.html', context)

def set_theme(request):
    theme = request.POST.get('theme', 'light')
    request.session['theme'] = theme
    print("THEME:", theme, request.session.get('theme'))
    return redirect(request.META.get('HTTP_REFERER', '/'))
