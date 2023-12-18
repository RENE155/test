from django.contrib import admin

# Register your models here.
from .models import Question, TestResult, PersonalityAdvice

admin.site.register(Question)
admin.site.register(TestResult)
admin.site.register(PersonalityAdvice)


