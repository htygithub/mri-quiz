from django import template

from quiz.models import Quiz

register = template.Library()

@register.inclusion_tag("quiz/quiz_list.html")
def quiz_list():
    quizes = Quiz.objects.order_by('name')

    return {
        'quizes': quizes
    }
