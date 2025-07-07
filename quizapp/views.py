from django.shortcuts import render
from .models import MCQ, TestResult
import json
from django.views.decorators.csrf import csrf_exempt  # for form handling
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from random import sample

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            password = form.cleaned_data.get('password')
            user = authenticate(user = user, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html', {'form' : form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in automatically
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def chapter_list(request):
    return render(request,'quiz/chapters.html')

@login_required
def home(request):
    test_results = TestResult.objects.filter(user=request.user).order_by('date_taken')
    scores = [result.score for result in test_results]
    labels = [result.date_taken.strftime("%b %d") for result in test_results]

    return render(request, 'quiz/home.html', {
        'scores': scores,
        'labels': labels,
        'username': request.user.username
    })

def map_options(options):  # mapping options to letter ("A":"option 1","B":"option 2" etc)
    return {chr(65+i): opt for i, opt in enumerate(options)}

def build_question_list(questions):
    question_list=[]
    for q in questions:
        question_data = {
            'id': q.id,
            'question': q.question,
            'answer': q.answer,
            'options': q.options,
            'explanation': q.explanation,
            'topic': q.topic,
            'difficulty': q.difficulty,
            'chapter': q.chapter,
            'option_map': map_options(q.options)  
        }
        question_list.append(question_data)
    return question_list


@login_required(login_url='/accounts/login/')
@csrf_exempt  # only during testing; remove this when using csrf_token properly
def take_test(request):
    chapter = request.GET.get("chapter")

    if request.method == "POST":
        ids = request.session.get('question_ids',[])
        ids = list(map(int, ids))
        questions=MCQ.objects.filter(id__in=ids)
        question_list = build_question_list(questions)
        total_questions= questions.count()
        score = 0
        results = {}

        for q in questions:
            selected = request.POST.get(f'q_{q.id}')
            results[q.id] = selected

            try:
                # finding the correct option text from the letter of correct answer 
                correct_text=map_options(q.options).get(q.answer)

                if selected == correct_text:
                    score +=1

            except Exception as e:
                print(f"Error processing question id {q.id}:{e}")

        
        return render(request, "quiz/result.html", {
            'selected': results,
            'score': score,
            'total': len(questions),
            'questions': question_list,
        })
    
        # Save test result
        TestResult.objects.create(user=request.user, score=score, total=len(questions))

    else :
        all_questions= MCQ.objects.filter(chapter = chapter)
        questions= sample(list(all_questions),min(10,len(all_questions)))
        # saving the selected ids in the session
        request.session['question_ids']= [q.id for q in questions]
        question_list = build_question_list(questions)
        return render(request, 'quiz/test.html', {
            'questions': question_list,
            'chapter': chapter
            })
