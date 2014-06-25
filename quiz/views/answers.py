from django.views import generic

from quiz.views.base import QuizMixin
from quiz.models import BrainStructure

class AnswerView(generic.ListView, QuizMixin):
    template_name = "quiz_answers.html"
    context_object_name = "questions"

    def get_queryset(self):
        self.quiz = self.get_quiz()
        return self.quiz.questions.all()

    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)

        context['current_quiz'] = self.quiz
        context['num_questions'] = self.quiz.questions.count()

        return context

class MRIAnswerView(generic.ListView):
    template_name = "mri_quiz_answers.html"
    context_object_name = "questions"

    def get_queryset(self):
        return BrainStructure.objects.all().select_related()
