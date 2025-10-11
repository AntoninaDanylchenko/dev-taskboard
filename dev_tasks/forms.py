from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from dev_tasks.models import Worker, Position, Task, TaskType


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select,
        required=True,
        label="Position"
    )

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = (
            "username",
            "first_name",
            "last_name",
            "position",
            "password1",
            "password2",
        )

class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.Select,
        required=True,
    )

    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M"
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
        label="Deadline",
    )

    class Meta:
        model = Task
        fields = "__all__"

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")

        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline