from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [

    path('', views.tables, name='home'),
    path('create_task/', views.create_task, name="create_task"),
    path('create_comment/', views.create_comment, name="create_comment"),
    path('edit_task/<slug:task_slug>/', views.edit_task_view, name='edit_task'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)