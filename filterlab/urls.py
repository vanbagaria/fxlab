from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_image, name="upload_image"),
    path('cleanup/', views.cleanup_filtered_image, name='cleanup_filtered_image'),
]

