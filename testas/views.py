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
    # Ensure there's a 'responses' key in the session, with an empty dictionary as a default
    if 'responses' not in request.session:
        request.session['responses'] = {}

    if request.method == 'POST':
        responses = request.session['responses']
        
        if 'submit' in request.POST:
            if responses:  # Check if the responses dictionary is not empty
                # Calculate the average score and determine the personality type
                total_score = sum(int(value) for value in responses.values())
                average_score = total_score / len(responses)
                if average_score <= 2:
                    personality = "Realist"
                elif average_score <= 4:
                    personality = "Dreamer"
                else:
                    personality = "Visionary"
            else:
                # Default values in case there are no responses
                average_score = 0
                personality = "Undefined"

            # Save the test result
            TestResult.objects.create(
                date_taken=timezone.now(),
                average_score=average_score,
                personality_type=personality
            )
            
            # Clear 'responses' and 'current_page' from the session
            if 'responses' in request.session:
                del request.session['responses']
            if 'current_page' in request.session:
                del request.session['current_page']
            
            return redirect('test_results')  # Redirect to the first page or results page

        else:
            # Update responses with the current POST data
            for key, value in request.POST.items():
                if key.startswith('response_'):
                    question_id = key.split('_')[1]
                    responses[question_id] = value

            request.session.modified = True
            page_number = request.POST.get('page', 1)
            return redirect(f'/testas/test?page={page_number}')

    else:
        # Handle GET requests: prepare and render the test questions
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

    



