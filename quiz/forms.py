from django import forms

from quiz.models import BrainStructure

class MRIQuizSubmitForm(forms.Form):
    answer = forms.ModelChoiceField(
        queryset=BrainStructure.objects.order_by('latin_name'), to_field_name="latin_name",
        widget=forms.RadioSelect, empty_label=None
    )

def create_quiz_form(quiz):
    class QuizSubmitForm(forms.Form):
        answer = forms.ModelChoiceField(
            queryset=quiz.answers.order_by('?'),
            widget=forms.RadioSelect,
            empty_label=None
        )

    return QuizSubmitForm

