
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # path("posts/all", views.allposts, name="allposts"),
    path("posts/all/page<int:apage>", views.allposts, name="allposts"),
    path("newpost", views.newpost, name="newpost"),
    path("editpost", views.editpost, name="editpost"),
    path("likepost", views.likepost, name="likepost"),
    path("posts/following/page<int:apage>", views.followingposts, name="following"),
    path("users/<str:user>/page<int:apage>", views.user, name="user"),
    path("followuser", views.followuser, name="followuser")
]
