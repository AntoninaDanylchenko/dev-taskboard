from django.urls import path

from dev_tasks.views import (index,
                             TaskListView,
                             MyTaskListView,
                             TaskDetailView,
                             TaskCreateView,
                             WorkerCreateView)


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("my-tasks/", MyTaskListView.as_view(), name="my-tasks-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),

    path("signup/", WorkerCreateView.as_view(), name="signup"),

]

app_name = "dev-tasks"
