from django.db import models
from django_currentuser.middleware import get_current_user

from profiles.models import Profile


class Post(models.Model):
    author = models.ForeignKey(Profile, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_owner_pk(self):
        return self.author.pk

    def get_author(self):
        return self.author.get_full_name()

    def get_author_username(self):
        return self.author.get_username()

    def who_liked(self):
        return PostRating.objects.filter(liked=True, post=self).values_list('by', flat=True)

    def who_disliked(self):
        return PostRating.objects.filter(liked=False, post=self).values_list('by', flat=True)

    def get_likes(self):
        return PostRating.objects.filter(liked=True, post=self).count()

    def get_dislikes(self):
        return PostRating.objects.filter(liked=False, post=self).count()


class PostRating(models.Model):
    liked = models.BooleanField(null=True)
    post = models.ForeignKey(Post, related_name='rated', on_delete=models.CASCADE)
    by = models.ForeignKey(Profile, related_name='rates', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.by} rated ({self.liked}) {self.post}'
