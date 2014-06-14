import json

from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib import messages

from quiz.models import BrainStructure
from quiz.forms import QuizSubmitForm

class QuizView(generic.FormView):
    template_name = "quiz.html"
    form_class = "QuizSubmitForm"
    success_url = reverse('quiz_view')

    def get_context_data(self, **kwargs):
        context = generic.TemplateView.get_context_data(self, **kwargs)

        if not 'quiz_queue' in self.request.session:
            self.request.session['quiz_queue'] = BrainStructure.generate_random_queue()
            self.request.session['score'] = 0
            self.request.session['total'] = 0

        current_structure = self.request.session['quiz_queue'].pop()

        context['current_structure'] = current_structure
        self.request.session['current_structure'] = current_structure

    def form_valid(self, form):
        if 'current_structure' in self.request.session:
            right_answer = self.request.session['current_structure'].latin_name

            if form.cleaned_data['answer'] == right_answer:
                messages.success(self.request, "Heel goed! U heeft het juiste antwoord gegeven!")
                self.request.session['score'] += 1
                self.request.session['total'] += 1
            else:
                messages.error(self.request, "Helaas... Dit was niet het juiste antwoord.")
                self.request.session['total'] += 1

        return generic.FormView.form_valid(self, form)
        




