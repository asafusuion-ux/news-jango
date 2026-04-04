from django.contrib import admin
from django.urls import path
from post import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, ),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)