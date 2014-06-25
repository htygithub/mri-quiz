from django import template

from quiz.models import Quiz

register = template.Library()

@register.inclusion_tag("quiz/quiz_list.html")
def quiz_list():
    quizes = Quiz.objects.order_by('name')

    return {
        'quizes': quizes
    }

@register.simple_tag(takes_context=True)
def quiz_score(context, quiz):
    session = context['request'].session

    if not hasattr(quiz, 'id'):
        quiz_id = 'mri'
    else:
        quiz_id = str(quiz.id)

    return session['quiz_data'][quiz_id]['score']

@register.simple_tag(takes_context=True)
def quiz_total(context, quiz):
    session = context['request'].session

    if not hasattr(quiz, 'id'):
        quiz_id = 'mri'
    else:
        quiz_id = str(quiz.id)

    return session['quiz_data'][quiz_id]['total']

