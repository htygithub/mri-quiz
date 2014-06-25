from django.views import generic

from quiz.views.base import QuizMixin
from quiz.models import BrainStructure

class AnswerView(generic.ListView, QuizMixin):
    template_name = "quiz_answers.html"
    context_object_name = "questions"

    def get_queryset(self):
        self.quiz = self.get_quiz()
        return self.quiz.questions

class MRIAnswerView(AnswerView):
    template_name = "mri_quiz_answers.html"

    def get_queryset(self):
        return BrainStructure.objects.all().select_related()
