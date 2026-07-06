from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from guard.forms_queue import QueueItemForm
from guard.models import QueueItem


def get_owned_item_or_403(pk, user):
    item = get_object_or_404(QueueItem, pk=pk)

    if item.user_id != user.id:
        raise PermissionDenied("他人のキューは操作できません。")

    return item


@login_required
def queue_list(request):
    category = request.GET.get("category")

    items = QueueItem.objects.filter(user=request.user).order_by("-created_at")

    if category:
        items = items.filter(category=category)

    return render(
        request,
        "guard/queue_list.html",
        {
            "items": items,
            "category_choices": QueueItem.CATEGORY_CHOICES,
            "selected_category": category,
        },
    )


@login_required
def queue_create(request):
    if request.method == "POST":
        form = QueueItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect("queue_detail", pk=item.pk)
    else:
        form = QueueItemForm()

    return render(
        request,
        "guard/queue_form.html",
        {
            "form": form,
            "page_title": "URLの登録",
            "button_label": "登録",
        },
    )


@login_required
def queue_detail(request, pk):
    item = get_owned_item_or_403(pk, request.user)

    return render(
        request,
        "guard/queue_detail.html",
        {
            "item": item,
        },
    )


@login_required
def queue_edit(request, pk):
    item = get_owned_item_or_403(pk, request.user)

    if request.method == "POST":
        form = QueueItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()
            return redirect("queue_detail", pk=item.pk)
    else:
        form = QueueItemForm(instance=item)

    return render(
        request,
        "guard/queue_form.html",
        {
            "form": form,
            "item": item,
            "page_title": "URLの編集",
            "button_label": "保存",
        },
    )


@login_required
def queue_delete(request, pk):
    item = get_owned_item_or_403(pk, request.user)

    if request.method == "POST":
        item.delete()
        return redirect("queue_list")

    return render(
        request,
        "guard/queue_confirm_delete.html",
        {
            "item": item,
        },
    )


from django.shortcuts import render

# Create your views here.
