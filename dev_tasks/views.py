from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView

from dev_tasks.forms import WorkerCreationForm
from dev_tasks.models import Task

@login_required
def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.all()
    total = tasks.count()
    done = tasks.filter(is_completed=True).count()
    in_progress = tasks.filter(is_completed=False, deadline__gte=timezone.now()).count()
    overdue = tasks.filter(is_completed=False, deadline__lt=timezone.now()).count()
    context = {
        "total": total,
        "done": done,
        "in_progress": in_progress,
        "overdue": overdue,
        "recent_tasks": tasks,
        "now": timezone.now(),
    }
    return render(
        request, "dev_tasks/index.html", context=context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        tasks = Task.objects.all()
        status = self.request.GET.get("status")
        priority = self.request.GET.get("priority")
        if status:
            if status == "done":
                tasks = tasks.filter(is_completed=True)
            elif status == "overdue":
                tasks = tasks.filter(is_completed=False, deadline__lt=timezone.now())
            elif status == "progress":
                tasks = tasks.filter(is_completed=False, deadline__gte=timezone.now())
        if priority:
            tasks = tasks.filter(priority=priority)

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class MyTaskListView(TaskListView):
    template_name = "dev_tasks/my_task_list.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(assignees=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class WorkerCreateView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
