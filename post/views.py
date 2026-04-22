from django.shortcuts import render, get_object_or_404, redirect
from post.models import Article, Category, Hashtag, Comments, Favorite
from django.db.models import Count, Q
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
import xml.etree.ElementTree as ET



@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        if not username:
            return redirect('profile')
        if len(username) >150:
            return redirect('profile')
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            return redirect('profile')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                return redirect('profile')
        user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        user.save()
        return redirect('profile')
    context ={
        'user':user,
    }
    return render(request, 'auth/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'auth/change_password.html', context)
               
def register(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {
        'form':form,
    }
    return render(request, 'auth/register.html', context)

def index(request):
    articles = Article.objects.all()
    hashtags = Hashtag.objects.all()

    paginator = Paginator(articles, 3) # кол-во постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj':page_obj,
        'hashtags':hashtags,
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
    return render(request, 'pages/search.html', context)


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
    comments = Comments.objects.all().filter(article=article).order_by('-id')
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = article.favorites.filter(user=request.user).exists()
    context = {
        'article':article,
        'comments':comments,
        'is_favorite':is_favorite
    }
    return render(request, 'pages/post-detail.html', context)



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
    return render(request, 'pages/category.html', context)

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
    return render(request, 'pages/category.html', context)

def set_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        request.session['theme'] = theme
        request.session.modified = True  
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def toggle_favorite(request, slug):
    article = get_object_or_404(Article, slug=slug)
    fav, created = Favorite.objects.get_or_create(
        user=request.user,
        article=article
    )
    if not created:
        fav.delete()
    return redirect('post_detail', slug=slug)

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user)\
        .select_related('article').order_by('-created_at')
    return render(request, 'pages/favorites.html', {'favorites':favorites})