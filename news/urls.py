from django.contrib import admin
from django.urls import path
from post import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('category/', views.category)

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)