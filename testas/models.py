from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class TestResult(models.Model):
    date_taken = models.DateTimeField(auto_now_add=True)
    average_score = models.FloatField()
    personality_type = models.CharField(max_length=255)  

    def __str__(self):
        return f"{self.date_taken.strftime('%Y-%m-%d')}: {self.personality_type}"
    
class PersonalityAdvice(models.Model):
    personality_type = models.CharField(max_length=100, unique=True)
    professional_advice = models.TextField(help_text="Advice for professional development.")
    personal_advice = models.TextField(help_text="Advice for personal growth.")
    growth_advice = models.TextField(help_text="Advice for overall growth and development.")

    def __str__(self):
        return f"Advice for {self.personality_type}"

