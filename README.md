INSTA_CLONE USING DJANGO
________________________________________________________________________________________________


🧑‍💻Authentication & User Management
signup(request)

     1.Handles user registration.

     2.Validates:

          Password match

          Unique username/email

      3.Accepts profile picture and bio.

      4.Logs in the user upon successful signup.

 user_login(request)
      
      Authenticates and logs in the user based on username and password.

      Displays error message if credentials are invalid.

user_logout(request)
     
      Logs out the currently authenticated user.

🏠Home & Profiles
      
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

🧑‍🤝‍🧑Friendship System
        
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

🛠️ Technologies Used
     
     Python 3

     Django 4

     SQLite (default database)

     HTML/CSS

     Pillow (for image upload)

🛠️ Installation Steps     

     ✅ 1. Install Python
          If you don’t have Python installed:

          Download from: https://www.python.org/downloads/

          Install Python and now check with python --version

      ✅ 2. Install Django    
            Install Django using pip:
                  "pip install django"
                  "django-admin --version"

       ✅ 3. Create a New Django Project           
                  django-admin startproject projectname
                  cd projectname

        ✅ 4. Create a Django App    
                  python manage.py startapp appname
                  
         ✅ 6. Install Required Packages
                  Pillow>=9.0.0
         
         ✅ 7. Apply Database Migrations
                 Create the database tables:

                    python manage.py makemigrations
                    python manage.py migrate

         ✅ 9. Run the Server  
                   Start the Django development server:
                         python manage.py runserver
          
          Open your browser and go to:

                    http://127.0.0.1:8000/
