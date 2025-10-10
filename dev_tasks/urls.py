from django.urls import path

from dev_tasks.views import index, TaskListView, MyTaskListView, WorkerCreateView


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("my-tasks/", MyTaskListView.as_view(), name="my-tasks-list"),

    path("signup/", WorkerCreateView.as_view(), name="signup"),

]

app_name = "dev-tasks"
