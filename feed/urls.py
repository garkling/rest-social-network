from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'feed'
post_list = views.PostViewSet.as_view(dict(get='list', post='create'))
post_detail = views.PostViewSet.as_view(dict(get='retrieve',
                                             put='update',
                                             patch='partial_update',
                                             delete='destroy'
                                             ))

urlpatterns = [

    path(r'posts/', post_list, name='post-list'),
    path(r'posts/create', post_list, name='post-create'),
    path(r'posts/<int:pk>', post_detail, name='post'),
    path(r'posts/<int:pk>/update', post_detail, name='post-update'),
    path(r'posts/<int:pk>/delete', post_detail, name='post-delete'),
    path(r'posts/rate', views.rate_post, name='rate'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
