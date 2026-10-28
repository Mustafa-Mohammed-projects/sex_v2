import re
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("الاسم", max_length=80, unique=True)

    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MediaItem(models.Model):
    PHOTO, VIDEO = "photo", "video"
    KIND_CHOICES = [(PHOTO, "صورة"), (VIDEO, "فيديو")]

    title = models.CharField("العنوان", max_length=150)
    description = models.TextField("الوصف", blank=True)
    kind = models.CharField("النوع", max_length=10, choices=KIND_CHOICES, default=PHOTO)
    category = models.ForeignKey(Category, verbose_name="التصنيف", null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name="items")
    image = models.ImageField("الصورة", upload_to="photos/%Y/%m/", blank=True)
    video_file = models.FileField("ملف الفيديو", upload_to="videos/%Y/%m/", blank=True)
    video_url = models.URLField("رابط يوتيوب (بديل عن الرفع)", blank=True)
    thumbnail = models.ImageField("صورة مصغّرة للفيديو", upload_to="thumbs/%Y/%m/", blank=True)
    featured = models.BooleanField("مميّز", default=False)
    is_published = models.BooleanField("منشور", default=True)
    views = models.PositiveIntegerField("المشاهدات", default=0, editable=False)
    created = models.DateTimeField("تاريخ النشر", auto_now_add=True)

    class Meta:
        verbose_name = "وسيط"
        verbose_name_plural = "الصور والفيديوهات"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gallery:detail", args=[self.pk])

    def clean(self):
        if self.kind == self.PHOTO and not self.image:
            raise ValidationError({"image": "ارفع صورة عند اختيار النوع صورة."})
        if self.kind == self.VIDEO and not (self.video_file or self.video_url):
            raise ValidationError("ارفع ملف فيديو أو ضع رابط يوتيوب.")

    @property
    def cover(self):
        if self.kind == self.PHOTO:
            return self.image or None
        return self.thumbnail or None

    @property
    def youtube_embed(self):
        m = re.search(r"(?:youtu\.be/|v=|embed/|shorts/)([\w-]{11})", self.video_url or "")
        return f"https://www.youtube.com/embed/{m.group(1)}" if m else ""
