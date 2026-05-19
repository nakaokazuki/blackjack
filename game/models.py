from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ユーザー名・パスワード（ハッシュ）は AbstractUser 由来。ポイントを追加。"""

    points = models.IntegerField(default=0, verbose_name="ポイント")

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def __str__(self) -> str:
        return self.username
