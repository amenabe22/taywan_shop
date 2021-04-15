from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
# from core_marketing.models import Rank
# from core_marketing.models import CoreLevelPlans


class CustomUser(AbstractUser):
    user_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    phone = models.CharField(
        max_length=200, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True)
    is_blocked = models.BooleanField(default=False)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return str(self.username)
