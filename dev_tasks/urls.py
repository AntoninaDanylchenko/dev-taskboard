from django.urls import path

from dev_tasks.views import index, TaskListView, WorkerCreateView


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("signup/", WorkerCreateView.as_view(), name="signup"),

]

app_name = "dev-tasks"
