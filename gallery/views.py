from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
from .models import Category, MediaItem


def home(request):
    qs = MediaItem.objects.filter(is_published=True).select_related("category")
    q = request.GET.get("q", "").strip()
    kind = request.GET.get("kind", "")
    cat = request.GET.get("cat", "")

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if kind in (MediaItem.PHOTO, MediaItem.VIDEO):
        qs = qs.filter(kind=kind)
    if cat.isdigit():
        qs = qs.filter(category_id=int(cat))

    featured = None
    if not (q or kind or cat):
        featured = MediaItem.objects.filter(is_published=True, featured=True).first()

    page = Paginator(qs, 12).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)

    return render(request, "gallery/home.html", {
        "page": page, "featured": featured,
        "categories": Category.objects.all(),
        "q": q, "kind": kind, "cat": cat,
        "qs": params.urlencode(),
    })


def detail(request, pk):
    item = get_object_or_404(MediaItem, pk=pk, is_published=True)
    MediaItem.objects.filter(pk=pk).update(views=F("views") + 1)
    item.refresh_from_db(fields=["views"])
    related = (MediaItem.objects.filter(is_published=True, category=item.category)
               .exclude(pk=pk)[:4] if item.category else
               MediaItem.objects.filter(is_published=True).exclude(pk=pk)[:4])
    return render(request, "gallery/detail.html", {"item": item, "related": related})
