import random
import os
import string

from django.db import models

def gen_filename(obj, filename):
    return os.path.join(
        "mri-images",
        ''.join(random.choice(string.ascii_letters) for i in range(12))
    )

def get_structure_names():
    names = []
    
    query = BrainStructure.objects.all()
    for row in query:
        names.append(row.latin_name)

    return names

class BrainStructure(models.Model):
    latin_name = models.CharField(max_length=200)
    english_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=gen_filename)

    @classmethod
    def generate_random_queue(cls):
        query = cls.objects.order_by('?').all()

        return list(query)

class MRISet(models.Model):
    structure = models.ForeignKey(BrainStructure)
    image1 = models.ImageField(upload_to=gen_filename)
    image2 = models.ImageField(upload_to=gen_filename)
    image3 = models.ImageField(upload_to=gen_filename)
