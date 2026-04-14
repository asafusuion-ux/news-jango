from post.models import Article, Category
from django.db.models import Count

def common(request):
    articles = Article.objects.all()[:5]  # топ 5 для дропдауна
    categories = Category.objects.annotate(
        articles_count=Count('articles')
    ).filter(articles_count__gt=0)[:6]
    
    return {
        'articles': articles,
        'categories': categories,
    }