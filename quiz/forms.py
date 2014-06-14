from django import forms

from quiz.models import get_structure_names

class QuizSubmitForm(forms.Form):
    answer = forms.RadioSelect(choices=get_structure_names)


