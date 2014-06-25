import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.forms import Form

from quiz.models import BrainStructure, Quiz, Question, generate_random_queue
from quiz.forms import MRIQuizSubmitForm, create_quiz_form

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
        if not 'quiz_data' in self.request.session:
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


class QuizView(generic.FormView, QuizMixin):
    template_name = "quiz.html"

    def dispatch(self, request, *args, **kwargs):
        self.current_question = None
        self.quiz = None

        return generic.FormView.dispatch(self, request, *args, **kwargs)

    def get_form_class(self):
        self.quiz = self.get_quiz()

        if not self.check_quiz() or 'restart' in self.request.GET:
            print("initialize")
            self.init_quiz_session()

        try:
            form_class = create_quiz_form(self.get_current_question())
        except IndexError:
            form_class = Form

        return form_class

    def get_quiz_id(self):
        return str(self.quiz.id)

    def get_current_question(self, force=False):
        print(self.request.session['quiz_data'][self.get_quiz_id()]['queue'])
        if not self.current_question or force:
            print("select question")
            current_id = self.request.session['quiz_data'][self.get_quiz_id()]['queue'][0]
            self.current_question = Question.objects.get(pk=current_id)

        return self.current_question

    def check_answer(self, answer):
        return answer == self.get_current_question().right_answer

    def get_right_answer(self):
        return self.get_current_question().right_answer

    def get_context_data(self, **kwargs):
        context = generic.TemplateView.get_context_data(self, **kwargs)
        show_score = False

        try:
            current_question = self.get_current_question(True)
        except IndexError:
            show_score = True

        context['show_score'] = show_score
        context['current_quiz'] = self.quiz

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
        return reverse('quiz_view', kwargs={'quiz': self.quiz.slug})

class MRIQuizView(QuizView):
    template_name = "mri_quiz.html"

    def get_quiz(self):
        raise NotImplementedError

    def get_quiz_id(self):
        return 'mri'

    def get_form_class(self):
        if not self.check_quiz() or 'restart' in self.request.GET:
            self.init_quiz_session()

        return MRIQuizSubmitForm

    def get_current_question(self, force=False):
        if not self.current_question or force:
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
            context['current_mriset'] = \
                self.get_current_question().mri_sets.order_by('?').first()

        return context

    def get_success_url(self):
        return reverse('mri_quiz_view')

class RestartView(generic.View, QuizMixin):

    def get_quiz_id(self):
        if self.kwargs['quiz'] == 'mri':
            return 'mri'
        else:
            return QuizMixin.get_quiz_id(self)

    def dispatch(self, request, *args, **kwargs):
        self.init_quiz_session()

        if kwargs['quiz'] == 'mri':
            return HttpResponseRedirect(reverse('mri_quiz_view'))
        else:
            return HttpResponseRedirect(reverse('quiz_view', kwargs=kwargs))

