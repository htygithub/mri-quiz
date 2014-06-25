import random
import os
import string

from django.db import models
from django.core.urlresolvers import reverse

def gen_filename(obj, filename):
    return os.path.join(
        "mri-images",
        ''.join(random.choice(string.ascii_letters) for i in range(12)) + ".png"
    )

def get_structure_names():
    names = []

    query = BrainStructure.objects.all()
    for row in query:
        names.append(row.latin_name)

    return names

def generate_random_queue():
    query = BrainStructure.objects.order_by('?').all()

    ids = []

    for row in query:
        ids.append(row.id)

    return ids

class BrainStructure(models.Model):
    """
        Quiz model for MRI images
    """
    latin_name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return "{} ({})".format(self.latin_name, self.english_name)

    def restart_url(self):
        return reverse('restart_mri_quiz')

class MRISet(models.Model):
    """
        Sets of MRI images which correspond to a certain brain structure
    """
    structure = models.ForeignKey(BrainStructure, related_name="mri_sets")
    image1 = models.ImageField(upload_to=gen_filename)
    image2 = models.ImageField(upload_to=gen_filename)
    image3 = models.ImageField(upload_to=gen_filename)

class Quiz(models.Model):
    """
        A collection of questions
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    class Meta:
        verbose_name_plural = 'Quizes'

    def restart_url(self):
        return reverse('restart_quiz', quiz=self.slug)

    def __str__(self):
        return self.name

class Question(models.Model):
    """
        A general multiple choice question
    """

    quiz = models.ForeignKey(Quiz, related_name="questions")
    question = models.CharField(max_length=255)
    additional_info = models.TextField(blank=True)
    image = models.ImageField(upload_to=gen_filename, blank=True)
    right_answer = models.ForeignKey('Answer', blank=True, null=True, related_name="questions")

    def __str__(self):
        return self.question

class Answer(models.Model):
    """
        Possible answers for a question
    """

    question = models.ForeignKey(Question, related_name="answers")
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer

