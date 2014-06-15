from django import forms

from quiz.models import BrainStructure

class QuizSubmitForm(forms.Form):
    answer = forms.ModelChoiceField(
        queryset=BrainStructure.objects.all(), to_field_name="latin_name",
        widget=forms.RadioSelect, empty_label=None
    )


