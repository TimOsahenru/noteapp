from django.db import models
from django.contrib.auth.models import AbstractUser


class Creator(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(default='avatar.svg')
    # followers =

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Note(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(Creator, default=None, related_name='likes', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=False)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.creator.username

    class Meta:
        ordering = ['-created_date']


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


class Liked(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    likes = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.note)
