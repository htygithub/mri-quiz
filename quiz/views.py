import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from quiz.models import BrainStructure, Quiz, Question, generate_random_queue
from quiz.forms import MRIQuizSubmitForm, create_quiz_form

class QuizView(generic.FormView):
    template_name = "quiz.html"

    def __init__(self, *args, **kwargs):
        self.current_question = None
        self.quiz = None

        generic.FormView.__init__(self, *args, **kwargs)

    def check_quiz():
        return (
            'quiz_data' in self.request.session and
            self.get_quiz_id() in self.request.session['quiz_data']
        )

    def init_quiz_session():
        if not 'quiz_data' in self.request.session:
            self.request.session['quiz_data'] = {}

        self.request.session['quiz_data'][self.get_quiz_id()] = {
            'queue': generate_random_queue(self.get_quiz_id()),
            'score': 0,
            'total': 0
        }

    def get_form_class(self):
        self.quiz = self.get_quiz()
        return create_quiz_form(self.quiz)

    def get_quiz(self):
        return get_object_or_404(Quiz, slug=self.args['quiz'])

    def get_quiz_id(self):
        return self.quiz.id

    def get_current_question(self):
        if not self.current_question:
            current_id = self.request.session['quiz_data'][self.get_quiz_id()]['queue'][0]
            self.current_question = Question.objects.get(pk=current_id)

        return self.current_question

    def update_queue(self):
        return self.request.session['quiz_data'][self.get_quiz_id()]['queue'].pop(0)

    def update_score(self, success):
        self.request.session['quiz_data'][self.get_quiz_id()]['total'] += 1

        if success:
            self.request.session['quiz_data'][self.get_quiz_id()]['score'] += 1

    def check_answer(self, answer):
        return answer == self.quiz.right_answer

    def get_right_answer(self):
        return self.quiz.right_answer
            
    def get_context_data(self, **kwargs):
        context = generic.TemplateView.get_context_data(self, **kwargs)

        if not self.check_quiz() or 'restart' in self.request.GET:
            self.init_quiz_session()

        show_score = False

        try:
            current_question = self.get_current_question()
        except IndexError:
            show_score = True

        context['show_score'] = show_score

        if show_score:
            context['current_question'] = None
        else:
            context['current_question'] = current_question

        return context

    def form_valid(self, form):
        current = self.get_current_question()
        if current:
            if self.check_answer(form.cleaned_data['answer']):
                messages.success(self.request, "Heel goed! U heeft het juiste antwoord gegeven!")
                self.update_score(True)
            else:
                messages.error(self.request, "Helaas... Dit was niet het juiste antwoord. Het juiste antwoord was {}".format(self.get_right_answer()))
                self.update_score(False)

            self.update_queue()

        return generic.FormView.form_valid(self, form)

    def get_success_url(self):
        return reverse('quiz_view', quiz=self.quiz.slug)

class MRIQuizView(QuizView):
    template_name = "mri_quiz.html"

    def get_quiz(self):
        raise NotImplementedError

    def get_quiz_id(self):
        return 'mri'

    def get_form_class(self):
        return MRIQuizSubmitForm

    def get_current_question(self):
        if not self.current_question:
            current_id = self.request.session['quiz_data'][self.get_quiz_id()]['queue'][0]
            self.current_question = BrainStructure.objects.get(id=current_id)

        return self.current_question

    def check_answer(self, answer):
        return answer.latin_name == self.get_current_question().latin_name

    def get_right_answer(self):
        return self.get_current_question().latin_name

    def get_context_data(self, **kwargs):
        context = QuizView.get_context_data(self, **kwargs)

        if not context['show_score']:
            context['current_mriset'] = 
                self.get_current_question().mri_sets.order_by('?').first()

        return context

    def get_success_url(self):
        return reverse('mri_quiz_view')

class RestartView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        request.session.flush()
        request.session['quiz_queue'] = generate_random_queue()
        request.session['score'] = 0
        request.session['total'] = 0
        
        return HttpResponseRedirect(reverse('quiz_view'))

