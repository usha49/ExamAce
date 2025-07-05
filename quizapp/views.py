from django.shortcuts import render
from .models import MCQ  
import json
from django.views.decorators.csrf import csrf_exempt  # for form handling
from django.db.models import Count
from random import sample


@csrf_exempt  # only during testing; remove this when using csrf_token properly
def take_test(request):
    if request.method == "POST":
        questions=MCQ.objects.all()[:10]
        total_questions= questions.count()
        score = 0
        results = {}

        for q in questions:
            selected = request.POST.get(f'q_{q.id}')
            results[q.id] = selected

            try:
                # mapping options to letter ("A":"option 1","B":"option 2" etc)
                option_map={ chr(65+i): opt for i, opt in enumerate(q.options)}
                # finding the correct option text from the letter of correct answer 
                correct_text=option_map.get(q.answer)

                if selected == correct_text:
                    score +=1

            except Exception as e:
                print(f"Error processing question id {q.id}:{e}")

        
        return render(request, "quiz/result.html", {
            'results': results,
            'score': score,
            'total': len(questions),
        })
    else :
        questions= MCQ.objects.all()[:10]
        return render(request, 'quiz/test.html', {'questions': questions})
