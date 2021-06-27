from django.contrib.auth.models import AbstractUser
from django.db import models
import json


class User(AbstractUser):
    following = models.ManyToManyField("User", related_name="thefollowing", blank=True)
    likedposts = models.TextField(default="[]")

    def followingCount(self):
        return self.following.count()

    def followersCount(self):
        return self.thefollowing.count()

    def __str__(self):
        return f"id: {self.id}, username: {self.username}, followingCount: {self.followingCount()}, followersCount: {self.followersCount()}\n"

    def towork(self):
        return json.loads(self.likedposts)

    def tojsondumps(self, thelist):
        self.likedposts = json.dumps(thelist)
        self.save()
        return


class posts(models.Model):
    puser = models.ForeignKey("User", related_name="thepuser", on_delete=models.CASCADE)
    post = models.CharField(max_length=280)
    pdate = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", related_name="thelikes", blank=True)

    def postLikes(self):
        return self.likes.count()

    def __str__(self):
        return f"id: {self.id}, puser: {self.puser.username}, post: {self.post}, likes: {self.postLikes()}\n"
    

class comments(models.Model):
    cuser = models.ForeignKey("User", related_name="thecuser", on_delete=models.CASCADE)
    cdate = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=280)
    cpost = models.ForeignKey("posts", related_name="thecpost", on_delete=models.CASCADE)

    def __str__(self):
        return f"id: {self.id}, cuser: {self.cuser.username}, comment: {self.comment}, cpost: {self.cpost}\n"


