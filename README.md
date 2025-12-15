---

# Mini Social Network – Backend API (Phase 1)

This project is a backend RESTful API for a mini social network, built with Django and Django REST Framework.
It focuses on authentication, privacy-aware content, social interactions, and clean API design.

> This repository represents Phase 1 of the project (Core Backend).

---

## 🚀 Tech Stack

- Python 3.12+
- Django 5.x
- Django REST Framework (DRF)
- JWT Authentication (SimpleJWT)
- Token Authentication
- SQLite (development database)

---

## 📁 Project Structure

mini_social/ │ ├── manage.py ├── db.sqlite3 │ ├── social_network/        # Project settings & main routing │   ├── settings.py │   ├── urls.py │   └── wsgi.py │ ├── users/                 # Users, profiles, auth, follow system │   ├── models.py          # UserProfile, Follow │   ├── serializers.py │   ├── views.py           # ProfileViewSet, FollowViewSet │   ├── views_auth.py      # JWT & Token auth views │   ├── permissions.py │   └── admin.py │ ├── posts/                 # Posts and likes │   ├── models.py          # Post, Like │   ├── serializers.py │   ├── views.py │   └── admin.py │ ├── comments/              # Comments and replies │   ├── models.py          # Comment (self-referenced) │   ├── serializers.py │   ├── views.py │   └── admin.py │ ├── feed/                  # Feed and explore logic │   └── views.py │ └── .gitignore

---

## ⚙️ Setup & Run

`bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Base URL:

http://127.0.0.1:8000

---

🔐 Authentication

The API supports multiple authentication methods.

1️⃣ JWT Authentication (Recommended)

Method	Endpoint	Description

POST	/api/auth/jwt-login/	Login & get access/refresh
POST	/api/auth/jwt-refresh/	Refresh access token
GET	/api/auth/me/	Get current user info


Header:

Authorization: Bearer <access_token>


---

2️⃣ Token Authentication

Method	Endpoint	Description

POST	/api/auth/token-login/	Get token
POST	/api/auth/token-logout/	Revoke token


Header:

Authorization: Token <token>


---

👤 Profiles API

Method	Endpoint	Description

GET	/api/profiles/	List profiles
GET	/api/profiles/{id}/	Retrieve profile
PATCH	/api/profiles/{id}/	Update own profile


🔒 Private Profiles:

Visible only to the owner or accepted followers.



---

📝 Posts API

Method	Endpoint	Description

GET	/api/posts/	List posts (privacy enforced)
POST	/api/posts/	Create post
GET	/api/posts/{id}/	Retrieve post
PATCH	/api/posts/{id}/	Update own post
DELETE	/api/posts/{id}/	Delete own post


Post Visibility

public → visible to everyone

followers → visible to accepted followers

private → visible only to author



---

❤️ Likes API

Method	Endpoint	Description

POST	/api/posts/{id}/like/	Toggle like / unlike


One like per user per post

Like count is returned with posts

---

💬 Comments & Replies API

Comments on Posts

Method	Endpoint

GET	/api/posts/{post_id}/comments/
POST	/api/posts/{post_id}/comments/


Replies to Comments

Method	Endpoint

GET	/api/comments/{id}/replies/
POST	/api/comments/{id}/replies/


Rules:

Replies must belong to the same post

Only author can edit/delete own comments



---

🤝 Follow System API

Method	Endpoint	Description

POST	/api/follows/request/	Send follow request
POST	/api/follows/{id}/accept/	Accept follow
POST	/api/follows/{id}/reject/	Reject follow
POST	/api/follows/{id}/unfollow/	Unfollow


Rules:

Cannot follow yourself

Private accounts → follow status = pending

Public accounts → follow status = accepted



---

📰 Feed & Explore

Method	Endpoint	Description

GET	/api/feed/	Personalized feed
GET	/api/explore/	Public posts only


Feed Logic

User’s own posts

Accepted followers’ posts

Visibility rules fully enforced



---

🛡️ Permissions Summary

IsAuthenticated (default)

IsOwnerOrReadOnly

IsAuthorOrReadOnly

CanViewProfile

Follow-based access control



---

📌 Project Status

✅ Phase 1 Completed

Core backend

Secure authentication

Privacy-aware social features

Clean API architecture


Future phases may include media uploads, messaging, notifications, and optimizations.


---