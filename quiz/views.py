import json

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from quiz.models import BrainStructure, generate_random_queue
from quiz.forms import QuizSubmitForm

class QuizView(generic.FormView):
    template_name = "quiz.html"
    form_class = QuizSubmitForm

    def get_context_data(self, **kwargs):
        context = generic.TemplateView.get_context_data(self, **kwargs)

        print(self.request.session)
        if (not 'quiz_queue' in self.request.session or 
            'restart' in self.request.GET):
            self.request.session['quiz_queue'] = generate_random_queue()
            self.request.session['score'] = 0
            self.request.session['total'] = 0

        show_score = False

        try:
            current_structure_id = self.request.session['quiz_queue'][0]
        except IndexError:
            show_score = True

        if show_score:
            context['current_structure'] = None
            context['current_mriset'] = None
            context['show_score'] = show_score
        else:
            current_structure = BrainStructure.objects.get(pk=current_structure_id)

            context['current_structure'] = current_structure
            context['current_mriset'] = current_structure.mri_sets.order_by('?').first()
            context['show_score'] = show_score

            if self.request.method == 'GET':
                # don't change structure on form submit
                self.request.session['current_structure'] = current_structure_id

        return context

    def form_valid(self, form):
        if 'current_structure' in self.request.session:
            current_structure = BrainStructure.objects.get(
                pk=self.request.session['current_structure'])

            if str(form.cleaned_data['answer'].latin_name) == str(current_structure.latin_name):
                messages.success(self.request, "Heel goed! U heeft het juiste antwoord gegeven!")
                self.request.session['score'] += 1
                self.request.session['total'] += 1
            else:
                messages.error(self.request, "Helaas... Dit was niet het juiste antwoord. Het juiste antwoord was {}".format(current_structure.latin_name))
                self.request.session['total'] += 1

            self.request.session['quiz_queue'].pop(0)

        return generic.FormView.form_valid(self, form)

    def get_success_url(self):
        return reverse('quiz_view')

class RestartView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        request.session.flush()
        request.session['quiz_queue'] = generate_random_queue()
        request.session['score'] = 0
        request.session['total'] = 0
        
        return HttpResponseRedirect(reverse('quiz_view'))

