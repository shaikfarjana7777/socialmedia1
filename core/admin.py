from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Like, Comment, FriendRequest, Friendship

admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(FriendRequest)
admin.site.register(Friendship)