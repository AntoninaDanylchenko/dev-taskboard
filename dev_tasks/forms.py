from django import forms
from django.contrib.auth.forms import UserCreationForm

from dev_tasks.models import Worker, Position


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
