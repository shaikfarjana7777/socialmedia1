from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    path('create-post/', views.create_post, name='create_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    
    path('search/', views.search, name='search'),
    path('friend-request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('remove-friend/<str:username>/', views.remove_friend, name='remove_friend'),
     path('friend-requests/', views.friend_requests_view, name='friend_requests'),
     path('friends/<str:username>/', views.friends_list_view, name='friends_list'),

    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),


]
