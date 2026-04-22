from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from post import views
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('register/', views.register, name='register'),
    path('login/' ,auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/' ,auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('', views.index, name='home'),
    path('search/', views.search, name='search'),
    path('set-theme/', views.set_theme, name='set_theme'),
    path('favorite/<slug:slug>', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_list, name='favorites'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('hashtag/<int:pk>/', views.hashtag_posts, name='hashtag_category_posts'),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)