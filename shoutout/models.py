from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

# update is_read with help of bulk update django method
class Shoutouts(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # user_img = models.CharField(photoURL)
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message + " " + "||" + f" Read {self.is_read} " + f"Publised {self.is_published}"

    class Meta:
        ordering = ['-created_at']