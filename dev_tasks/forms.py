from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from dev_tasks.models import Worker, Position, Task, TaskType


User = get_user_model()


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
        queryset=User.objects.all(),
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


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search...",
                "class": "form-control mr-2",
                "style": "min-width: 250px;",
            }
        ),
    )

    def filter_queryset(self, queryset, *fields):
        query = self.cleaned_data.get("query")
        if query:
            from django.db.models import Q
            q_object = Q()
            for field in fields:
                q_object |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(q_object)
        return queryset


class UpdateMeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "position"]