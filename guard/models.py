from django.conf import settings
from django.db import models
from django.utils import timezone


class QueueItem(models.Model):
    CATEGORY_CHOICES = [
        ("youtube", "YouTube"),
        ("article", "記事"),
        ("sns", "SNS"),
        ("shopping", "商品ページ"),
        ("other", "その他"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="ユーザー",
        on_delete=models.CASCADE,
        related_name="queue_items",
    )
    title = models.CharField("タイトル", max_length=100)
    url = models.URLField("URL")
    category = models.CharField(
        "カテゴリ",
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
    )
    release_at = models.DateTimeField("解放日時")
    memo = models.TextField("メモ", blank=True)
    created_at = models.DateTimeField("登録日時", auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_released(self):
        return timezone.now() >= self.release_at

    @property
    def status_label(self):
        if self.is_released:
            return "解放済み"
        return "ロック中"