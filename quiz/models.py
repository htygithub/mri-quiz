import random
import os
import string

from django.db import models

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

class MRISet(models.Model):
    """
        Sets of MRI images which correspond to a certain brain structure
    """
    structure = models.ForeignKey(BrainStructure, related_name="mri_sets")
    image1 = models.ImageField(upload_to=gen_filename)
    image2 = models.ImageField(upload_to=gen_filename)
    image3 = models.ImageField(upload_to=gen_filename)

class Group(models.Model):
    """
        A group which holds multiple quizes
    """

    name = models.CharField(max_length=200)

class Quiz(models.Model):
    """
        General multiple choice quiz
    """

    group = models.ForeignKey(Group, related_name="quizes")
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to=gen_filename, blank=True)

class Answers(models.Model):
    """
        Possible answers for a quiz
    """

    quiz = models.ForeignKey(Quiz, related_name="answers")
    answer = models.CharField(max_length=255)

