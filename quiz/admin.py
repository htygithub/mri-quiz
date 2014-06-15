from django.contrib import admin
from quiz.models import BrainStructure, MRISet

class MRISetInline(admin.TabularInline):
    model = MRISet
    extra = 1

class BrainStructureAdmin(admin.ModelAdmin):
    inlines = [MRISetInline]

admin.site.register(BrainStructure, BrainStructureAdmin)
