INSTA_CLONE USING DJANGO
________________________________________________________________________________________________


Authentication & User Management
signup(request)
Handles user registration.

Validates:

Password match

Unique username/email

Accepts profile picture and bio.

Logs in the user upon successful signup.

user_login(request)
Authenticates and logs in the user based on username and password.

Displays error message if credentials are invalid.

user_logout(request)
Logs out the currently authenticated user.

Home & Profiles
index(request)
Displays posts from:

Current user

Friends of the current user (if post is friends)

Public posts

Posts are ordered by created_at.

profile(request, username)
Displays the profile of a user.

Shows their posts based on visibility (public/friends).

Indicates friendship status and allows sending/receiving friend requests.

edit_profile(request)
Allows the user to update their email, bio, and profile picture.

Friendship System
send_friend_request(request, username)
Sends a friend request to another user.

If the reverse friend request exists, it accepts it instead.

accept_friend_request(request, request_id)
Accepts a friend request and creates a Friendship.

reject_friend_request(request, request_id)
Deletes a received friend request.

remove_friend(request, username)
Removes an existing friend relationship.

friend_requests_view(request)
Shows both:

Friend requests received

Friend requests sent

friends_list_view(request, username)
Displays the list of friends for a specific user.

📢 Posts, Likes, and Comments
create_post(request)
Allows the user to create a new post with:

Text content (optional)

Image (optional)

Video (optional)

Privacy level (public or friends)

delete_post(request, post_id)
Deletes a post owned by the logged-in user.

like_post(request, post_id)
Likes or unlikes a post (toggle behavior).

add_comment(request, post_id)
Adds a comment to a post.

🔍 Search
search(request)
Searches for users by username or email.

Excludes the currently logged-in user from the results.

🛠️ Models Used (Referenced in Code)
User: Custom user model with profile fields.

Post: User posts with optional image/video and privacy.

Like: Like relationship between user and post.

Comment: Comments on posts.

FriendRequest: Represents pending friend requests.

Friendship: Represents confirmed friendships between users.


🔍 Search
search(request)
Searches for users by username or email.

Excludes the currently logged-in user from the results.

🛠️ Models Used (Referenced in Code)
User: Custom user model with profile fields.

Post: User posts with optional image/video and privacy.

Like: Like relationship between user and post.

Comment: Comments on posts.

FriendRequest: Represents pending friend requests.

Friendship: Represents confirmed friendships between users.
