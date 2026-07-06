from django import forms

from guard.models import QueueItem


class QueueItemForm(forms.ModelForm):
    release_at = forms.DateTimeField(
        label="解放日時",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )

    class Meta:
        model = QueueItem
        fields = [
            "title",
            "url",
            "category",
            "release_at",
            "memo",
        ]
        widgets = {
            "memo": forms.Textarea(attrs={"rows": 4}),
        }