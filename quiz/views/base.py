from django.shortcuts import get_object_or_404
from django.views import generic

from quiz.models import Quiz, generate_random_queue

class IndexView(generic.ListView):
    template_name = "home.html"
    queryset = Quiz.objects.order_by('name')
    context_object_name = "quiz_list"

class QuizMixin:
    def check_quiz(self):
        return (
            'quiz_data' in self.request.session and
            self.get_quiz_id() in self.request.session['quiz_data']
        )

    def init_quiz_session(self):
        if 'quiz_data' not in self.request.session:
            self.request.session['quiz_data'] = {}

        self.request.session['quiz_data'][self.get_quiz_id()] = {
            'queue': generate_random_queue(self.get_quiz_id()),
            'score': 0,
            'total': 0
        }

        self.request.session.modified = True

    def get_quiz(self):
        return get_object_or_404(Quiz, slug=self.kwargs['quiz'])

    def get_quiz_id(self):
        return str(self.get_quiz().id)

    def update_queue(self):
        self.request.session.modified = True
        return self.request.session['quiz_data'][self.get_quiz_id()]['queue'].pop(0)

    def update_score(self, success):
        self.request.session['quiz_data'][self.get_quiz_id()]['total'] += 1

        if success:
            self.request.session['quiz_data'][self.get_quiz_id()]['score'] += 1

        self.request.session.modified = True

