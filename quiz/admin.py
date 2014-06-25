from django.contrib import admin
from django.template.defaultfilters import slugify

from quiz.models import BrainStructure, MRISet, Quiz, Question, Answer

class MRISetInline(admin.TabularInline):
    model = MRISet
    extra = 1

class BrainStructureAdmin(admin.ModelAdmin):
    inlines = [MRISetInline]

def clone_question(modeladmin, request, queryset):
    for obj in queryset:
        new_obj = Question()
        new_obj.quiz = obj.quiz
        new_obj.question += "{} (kopie)".format(obj.question)
        new_obj.additional_info = obj.additional_info
        new_obj.image = obj.image

        new_obj.save()

        for answer in obj.answers.all():
            print("Test", answer)
            new_answer = Answer()
            new_answer.answer = answer.answer
            new_answer.question = new_obj

            new_answer.save()

            if answer == obj.right_answer:
                new_obj.right_answer = new_answer
                new_obj.save()

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    actions = [clone_question]

    def get_form(self, request, obj=None, **kwargs):
        request.current_question = obj
        return admin.ModelAdmin.get_form(self, request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
            Limit answers to current question
        """

        if db_field.name == 'right_answer':
            if request.current_question:
                kwargs["queryset"] = request.current_question.answers.all()
            else:
                kwargs["queryset"] = Answer.objects.none()

        return admin.ModelAdmin.formfield_for_foreignkey(self, db_field, request, **kwargs)

class QuizAdmin(admin.ModelAdmin):
    fields = ['name']

    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.name)
        obj.save()


admin.site.register(BrainStructure, BrainStructureAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
