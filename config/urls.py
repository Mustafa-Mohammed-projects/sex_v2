from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "لوحة تحكم المعرض"
admin.site.site_title = "إدارة المعرض"
admin.site.index_title = "إدارة الصور والفيديوهات"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("gallery.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
