from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question, Choice, Player
from .models import Quiz, QuizAttempt, Question, UserAnswer, Choice
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from django.db import transaction

@login_required
def home(request):
  return render(request, "home.html")
 

def authView(request):
 if request.method == "POST":
  form = UserCreationForm(request.POST or None)
  if form.is_valid():
   form.save()
   return redirect("base:login")
 else:
  form = UserCreationForm()
 return render(request, "registration/signup.html", {"form": form})

#Create and display players
def PlayerView(request):
  # p1 = Player(pseudo= "TRUCMACHIN",score =4 )
  # p1.save()
  allPlayer = Player.objects.order_by("score").reverse()

  return render(request, "classement/classement.html", {"allPlayer" : allPlayer })



class QuizDetailView(DetailView):
    model = Quiz
    template_name = 'quiz/quiz_detail.html'  # You can customize the template name

@login_required
@csrf_exempt
@require_POST
def save_quiz(request):
    try:
        data = json.loads(request.body)
        quiz = Quiz.objects.create(
            title=data['title'],
            description=data['description'],
            creator=request.user
        )

        for question_data in data['questions']:
            question = Question.objects.create(
                quiz=quiz,
                text=question_data['text']
            )
            for choice_data in question_data['choices']:
                Choice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )

        return JsonResponse({"message": "Quiz created successfully!"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@login_required
@csrf_exempt
def get_quiz_json(request, id):
    quiz = Quiz.objects.get(pk=id)
    quiz_data = {
        "title": quiz.title,
        "description": quiz.description,
        "questions": [
            {
                "text": question.text,
                "choices": [
                    {"text": choice.text, "is_correct": choice.is_correct}
                    for choice in question.choices.all()
                ]
            } for question in quiz.questions.all()
        ]
    }
    return JsonResponse(quiz_data)


@login_required
@csrf_exempt
@require_POST
def update_quiz_form(request, id):
    try:
        data = json.loads(request.body.decode('utf-8'))  # Make sure to decode the request body
        print(data)  # Debugging to see the full data

        quiz = Quiz.objects.get(pk=id)
        quiz.title = data['title']
        quiz.description = data['description']
        quiz.save()

        # Clear existing questions and choices
        Question.objects.filter(quiz=quiz).delete()

        for question_data in data['questions']:
            question = Question.objects.create(quiz=quiz, text=question_data['text'])
            for choice_data in question_data['choices']:
                Choice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )

        return JsonResponse({"message": "Quiz updated successfully!"}, status=200)

    except Exception as e:
        print("Error updating quiz: ", str(e))  # Log the error for debugging
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
def get_quiz_details(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all()
    quiz_data = {
        'id': quiz.id,
        'title': quiz.title,
        'description': quiz.description,
        'questions': [{
            'id': question.id,
            'text': question.text,
            'choices': [
                {'id': choice.id, 'text': choice.text}
                for choice in question.choices.all()
            ]
        } for question in questions]
    }
    return JsonResponse(quiz_data)

@require_POST
@login_required
@csrf_exempt
def submit_quiz(request, quiz_id):
    user = request.user
    data = request.POST
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    try:
        with transaction.atomic():
            quiz_attempt = QuizAttempt.objects.create(user=user, quiz=quiz, score=0)
            total_score = 0

            for key, values in data.lists():  # Use .lists() to correctly handle multiple values
                if key.startswith('question_'):
                    # Properly extract the question ID
                    question_id = key.split('_')[1].rstrip('[]')  # Strip '[]' from the question ID
                    for value in values:  # Handle multiple choice values
                        chosen_choice = get_object_or_404(Choice, pk=value)
                        correct = chosen_choice.is_correct
                        UserAnswer.objects.create(
                            attempt=quiz_attempt,
                            question_id=question_id,
                            choice=chosen_choice
                        )
                        if correct:
                            total_score += 1

            quiz_attempt.score = total_score
            quiz_attempt.save()

    except Exception as e:
        print("Error during submission:", e)
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'status': 'ok', 'score': total_score})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    return render(request, 'quiz/take_quiz.html', {'quiz_id': quiz_id})

@login_required
def create_quiz(request):
   return render(request, 'quiz/create_quiz.html')


@login_required
def QuizList(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        quiz.delete()
        return redirect('base:quiz_list')
    else:
        # Retourner une page qui demande confirmation
        return render(request, 'delete_confirmation.html', {'quiz': quiz})

@login_required
def update_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    return render(request, 'quiz/update_quiz.html', {
        'quiz_id': pk,
    })