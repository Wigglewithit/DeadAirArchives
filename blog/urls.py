from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # New static pages
    path('about/', views.about, name='about'),
    path('videos/', views.videos, name='videos'),
    path('conspiracy/', views.conspiracy, name='conspiracy'),
    path('tech/', views.tech, name='tech'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('videos/', views.videos_view, name='videos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
