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
    latin_name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.latin_name

class MRISet(models.Model):
    structure = models.ForeignKey(BrainStructure, related_name="mri_sets")
    image1 = models.ImageField(upload_to=gen_filename)
    image2 = models.ImageField(upload_to=gen_filename)
    image3 = models.ImageField(upload_to=gen_filename)
