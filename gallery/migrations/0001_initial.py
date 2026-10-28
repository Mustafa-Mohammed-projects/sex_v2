import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="الاسم")),
            ],
            options={"verbose_name": "تصنيف", "verbose_name_plural": "التصنيفات", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="MediaItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, verbose_name="العنوان")),
                ("description", models.TextField(blank=True, verbose_name="الوصف")),
                ("kind", models.CharField(choices=[("photo", "صورة"), ("video", "فيديو")], default="photo", max_length=10, verbose_name="النوع")),
                ("image", models.ImageField(blank=True, upload_to="photos/%Y/%m/", verbose_name="الصورة")),
                ("video_file", models.FileField(blank=True, upload_to="videos/%Y/%m/", verbose_name="ملف الفيديو")),
                ("video_url", models.URLField(blank=True, verbose_name="رابط يوتيوب (بديل عن الرفع)")),
                ("thumbnail", models.ImageField(blank=True, upload_to="thumbs/%Y/%m/", verbose_name="صورة مصغّرة للفيديو")),
                ("featured", models.BooleanField(default=False, verbose_name="مميّز")),
                ("is_published", models.BooleanField(default=True, verbose_name="منشور")),
                ("views", models.PositiveIntegerField(default=0, editable=False, verbose_name="المشاهدات")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="items", to="gallery.category", verbose_name="التصنيف")),
            ],
            options={"verbose_name": "وسيط", "verbose_name_plural": "الصور والفيديوهات", "ordering": ["-created"]},
        ),
    ]
