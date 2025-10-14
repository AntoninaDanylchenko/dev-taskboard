from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from dev_tasks.forms import WorkerCreationForm, TaskForm, SearchForm, UpdateMeForm
from dev_tasks.models import Task, Worker


User = get_user_model()
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
        form = SearchForm(self.request.GET)
        if form.is_valid():
            tasks = form.filter_queryset(tasks, "name", "description")

        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(initial={"query": self.request.GET.get("query", "")})
        context["now"] = timezone.now()
        return context


class MyTaskListView(TaskListView):
    template_name = "dev_tasks/my_task_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(assignees=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("dev-tasks:tasks-list")
    template_name = "dev_tasks/task_form.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("dev-tasks:tasks-list")
    template_name = "dev_tasks/task_delete.html"

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("dev-tasks:task-list")


class WorkerListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "workers"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(initial={"query": self.request.GET.get("query", "")})
        return context

    def get_queryset(self):
        queryset = super().get_queryset().select_related("position")
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter_queryset(queryset, "first_name", "last_name", "position__name")
        return queryset


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "worker"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        context["completed_tasks_count"] = worker.tasks.filter(is_completed=True).count()
        context["active_tasks_count"] = worker.tasks.filter(is_completed=False).count()
        context["now"] = timezone.now()
        return context


class AboutMeDetailView( WorkerDetailView):
    template_name = "dev_tasks/worker_detail.html"
    def get_object(self, queryset=None):
        return self.request.user


class UpdateMeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UpdateMeForm
    template_name = "dev_tasks/worker_form.html"
    success_url = reverse_lazy("dev-tasks:about-me")

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        return self.request.user == self.get_object()


class WorkerCreateView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


class ToggleAssignToTaskView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        worker = request.user  # same as Worker.objects.get(id=request.user.id)

        if worker in task.assignees.all():
            task.assignees.remove(worker)
        else:
            task.assignees.add(worker)

        return redirect("dev-tasks:task-detail", pk=pk)


class ToggleTaskStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)

        if request.user in task.assignees.all() or request.user.is_staff:
            task.is_completed = not task.is_completed
            task.save()

        return redirect("dev-tasks:task-detail", pk=pk)
