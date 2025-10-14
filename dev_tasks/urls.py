from django.urls import path

from dev_tasks.views import (index,
                             TaskListView,
                             MyTaskListView,
                             TaskDetailView,
                             TaskUpdateView,
                             TaskDeleteView,
                             ToggleAssignToTaskView,
                             ToggleTaskStatusView,
                             TaskCreateView,
                             WorkerListView,
                             WorkerDetailView,
                             AboutMeDetailView,
                             UpdateMeView,
                             WorkerCreateView,)


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TaskListView.as_view(), name="tasks-list"),
    path("my-tasks/", MyTaskListView.as_view(), name="my-tasks-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/toggle-assign/", ToggleAssignToTaskView.as_view(), name="toggle-task-assign"),
    path("tasks/<int:pk>/toggle-status/", ToggleTaskStatusView.as_view(), name="toggle-task-status"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("workers/", WorkerListView.as_view(), name="workers-list"),
    path("workers/<int:pk>", WorkerDetailView.as_view(), name="worker-detail"),
    path("about-me/", AboutMeDetailView.as_view(), name="about-me"),
    path("update-me/", UpdateMeView.as_view(), name="update-me"),
    path("signup/", WorkerCreateView.as_view(), name="signup"),
]

app_name = "dev-tasks"
