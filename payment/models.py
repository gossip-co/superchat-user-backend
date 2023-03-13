from django.db import models
from django.contrib.auth.models import User

from uuid import uuid4

from shoutout.models import Shoutouts


class Orders(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    shoutout = models.ForeignKey(Shoutouts, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
