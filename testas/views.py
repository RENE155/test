# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Question, TestResult, PersonalityAdvice
from django.db.models import Avg

CHOICES = (
    (1, 'Strongly disagree'),
    (2, 'Disagree'),
    (3, 'Neutral'),
    (4, 'Agree'),
    (5, 'Strongly agree'),
)


def test(request):
    request.session.setdefault('responses', {})

    if request.method == 'POST':
        responses = request.session['responses']
        
        if 'submit' in request.POST:
            average_score = sum(int(value) for value in responses.values()) / len(responses)
            personality = ("Realist" if average_score <= 2 else
                           "Dreamer" if average_score <= 4 else
                           "Visionary")
            TestResult.objects.create(date_taken=timezone.now(),
                                      average_score=average_score,
                                      personality_type=personality)
            
            request.session.pop('responses', None)
            request.session.pop('current_page', None)
            return redirect('test_results')
        else:
            for key, value in request.POST.items():
                if key.startswith('response_'):
                    question_id = key.split('_')[1]
                    responses[question_id] = int(value)

            request.session.modified = True
            page_number = request.POST.get('page', 1)
            return redirect(f'{reverse("test")}?page={page_number}')

    else:
        questions = Question.objects.all()
        paginator = Paginator(questions, 10)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        progress_percentage = (page_obj.number / paginator.num_pages) * 100

        return render(request, 'tests/test.html', {
            'page_obj': page_obj,
            'progress_percentage': progress_percentage,
            'choices': CHOICES 
        })

    

def index(request):
    total_results = TestResult.objects.count()
    percent_realists = percent_dreamers = percent_visionaries = average_score = 0

    if total_results > 0:
        total_realists = TestResult.objects.filter(personality_type="Realist").count()
        total_dreamers = TestResult.objects.filter(personality_type="Dreamer").count()
        total_visionaries = TestResult.objects.filter(personality_type="Visionary").count()

        percent_realists = (total_realists / total_results) * 100
        percent_dreamers = (total_dreamers / total_results) * 100
        percent_visionaries = (total_visionaries / total_results) * 100

        average_score = TestResult.objects.aggregate(avg_score=Avg('average_score'))['avg_score']
    
    tests = Question.objects.all()
    context = {
        'tests': tests,
        'percent_realists': percent_realists,
        'percent_dreamers': percent_dreamers,
        'percent_visionaries': percent_visionaries,
        'average_score': average_score
    }
    return render(request, 'tests/index.html', context)


def test_results(request):
    try:
        latest_result = TestResult.objects.latest('date_taken')
        personality_type = latest_result.personality_type
        try:
            advice = PersonalityAdvice.objects.get(personality_type=personality_type)
        except PersonalityAdvice.DoesNotExist:
            advice = None

        return render(request, 'tests/result.html', {
            'personality': personality_type,
            'advice': advice
        })
    except TestResult.DoesNotExist:
        return render(request, 'tests/result.html', {'message': 'No test results found.'})

    



