from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'profiles'
user_list = views.ProfileViewSet.as_view(dict(get='list'))
user_detail = views.ProfileViewSet.as_view(dict(get='retrieve',
                                                put='update',
                                                patch='partial_update',
                                                delete='destroy'
                                                ))

urlpatterns = [
    path(r'users/', user_list, name='profile-list'),
    path(r'users/<int:pk>', user_detail, name='profile'),
    path(r'users/<int:pk>/update', user_detail, name='profile-update'),
    path(r'users/<int:pk>/delete', user_detail, name='profile-delete'),
    path(r'users/<int:pk>/update-password', views.UpdatePasswordView.as_view(), name='password-update'),
    path(r'signup/', views.ProfileCreation.as_view(), name='sign-up'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
