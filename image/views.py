from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render

from image.models import Image


def health(request):
    return JsonResponse({"status": "ok"})


def image_list(request):
    query = request.GET.get("q", "").strip()
    grouped_images = Image.objects.all()
    if query:
        grouped_images = grouped_images.filter(Q(prn__icontains=query) | Q(name__icontains=query))

    groups = list(
        grouped_images.values("prn")
        .annotate(image_count=Count("id"))
        .order_by("prn")
    )
    if groups:
        prns = [group["prn"] for group in groups]
        images_by_prn = {}
        for image in grouped_images.filter(prn__in=prns).order_by("prn", "-is_main", "position", "name"):
            images_by_prn.setdefault(image.prn, []).append(image)
        for group in groups:
            group["images"] = images_by_prn.get(group["prn"], [])

    return render(request, "image/image_list.html", {"groups": groups, "query": query})
