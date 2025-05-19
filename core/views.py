from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Post, Like, Comment, FriendRequest, Friendship
from django.db.models import Q

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        bio = request.POST.get('bio', '')
        profile_pic = request.FILES.get('profile_pic')
        
        if password != password2:
            messages.error(request, "Passwords don't match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.bio = bio
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        
        login(request, user)
        return redirect('index')
    
    return render(request, 'core/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'core/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):

    friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).values_list('user1', 'user2')
    
    friend_ids = set()
    for pair in friends:
        friend_ids.add(pair[0])
        friend_ids.add(pair[1])
    friend_ids.discard(request.user.id)
    
    posts = Post.objects.filter(
        Q(user__in=friend_ids, privacy='friends') | 
        Q(privacy='public') |
        Q(user=request.user)
    ).order_by('-created_at').select_related('user')
    
    context = {
        'posts': posts,
    }
    return render(request, 'core/index.html', context)


@login_required
def friends_list_view(request, username):
    user = get_object_or_404(User, username=username)
    is_own_profile = (request.user == user)
    
    
    friendships = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    )
    
    friends = []
    for friendship in friendships:
        friend = friendship.user1 if friendship.user1 != user else friendship.user2
        friends.append(friend)
    
    context = {
        'profile_user': user,
        'friends': friends,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'core/friends_list.html', context)

@login_required
def friend_requests_view(request):

    received_requests = FriendRequest.objects.filter(
        to_user=request.user
    ).select_related('from_user')
    
    sent_requests = FriendRequest.objects.filter(
        from_user=request.user
    ).select_related('to_user')
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'core/friend_requests.html', context)

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    
    is_own_profile = user == request.user
    profile_user = get_object_or_404(User, username=username)

    is_friend = Friendship.objects.filter(
        Q(user1=request.user, user2=user) | 
        Q(user1=user, user2=request.user)
    ).exists()
    friends_count = Friendship.objects.filter(
    Q(user1=profile_user) | Q(user2=profile_user)
).count()

    friend_request_sent = FriendRequest.objects.filter(
        from_user=request.user, to_user=user).exists()
    
    friend_requests_received = FriendRequest.objects.filter(
        from_user=profile_user,
        to_user=request.user
    )
    
    if is_own_profile:
        visible_posts = posts
    elif is_friend:
        visible_posts = posts.filter(privacy__in=['friends', 'public'])
    else:
        visible_posts = posts.filter(privacy='public')
    
    context = {
        'profile_user': profile_user,
        'posts': visible_posts.order_by('-created_at'),
        'is_own_profile': is_own_profile,
        'is_friend': is_friend,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_requests_received,
         'friends_count': friends_count,
    }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.bio = request.POST.get('bio', user.bio)
        
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
        
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile', username=user.username)
    
    return render(request, 'core/edit_profile.html')

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')

        video = request.FILES.get('video')


        privacy = request.POST.get('privacy', 'public')
        
        if not content and not image:
            messages.error(request, "Post cannot be empty")
            return redirect('create_post')
        
        post = Post.objects.create(
            user=request.user,
            content=content,
            image=image,

            video=video,

            privacy=privacy
        )
        messages.success(request, "Post created successfully")
        return redirect('index')
    
    return render(request, 'core/create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user already liked the post
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        like.delete()
    
    return redirect('index')

@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        
        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )
    
    return redirect('index')

@login_required
def search(request):
    query = request.GET.get('q', '')
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=request.user.id)
    else:
        users = User.objects.none()
    
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'core/search.html', context)

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    
    if Friendship.objects.filter(
        Q(user1=request.user, user2=to_user) | 
        Q(user1=to_user, user2=request.user)
    ).exists():
        messages.error(request, "You are already friends")
        return redirect('profile', username=username)
    
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        messages.error(request, "Friend request already sent")
        return redirect('profile', username=username)
    
    reverse_request = FriendRequest.objects.filter(from_user=to_user, to_user=request.user).first()
    if reverse_request:
        Friendship.objects.create(user1=request.user, user2=to_user)
        reverse_request.delete()
        messages.success(request, f"You are now friends with {to_user.username}")
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, "Friend request sent")
    
    return redirect('profile', username=username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
    
    friend_request.delete()
    
    messages.success(request, f"You are now friends with {friend_request.from_user.username}")
    return redirect('profile', username=friend_request.from_user.username)

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    messages.info(request, "Friend request rejected")
    return redirect('profile', username=friend_request.from_user.username)

@login_required
def remove_friend(request, username):
    friend = get_object_or_404(User, username=username)
    
    friendship = Friendship.objects.filter(
        Q(user1=request.user, user2=friend) | 
        Q(user1=friend, user2=request.user)
    ).first()
    
    if friendship:
        friendship.delete()
        messages.info(request, f"You are no longer friends with {friend.username}")
    
    return redirect('profile', username=username)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.user:  
        post.delete()
    
    return redirect('profile',username=request.user.username)