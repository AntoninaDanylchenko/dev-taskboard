from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from dev_tasks.models import Task


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.all()
    total = tasks.count()
    done = tasks.filter(is_completed=True).count()
    in_progress = tasks.filter(is_completed=False, deadline__gte=timezone.now()).count()
    overdue = tasks.filter(is_completed=True, deadline__lt=timezone.now()).count()
    context = {
        "tasks": tasks,
        "total": total,
        "done": done,
        "in_progress": in_progress,
        "overdue": overdue,
    }
    return render(
        request, "dev_tasks/index.html", context=context)
