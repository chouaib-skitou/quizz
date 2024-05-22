from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question, Choice, Player
from django.views.generic import DetailView

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
    template_name = 'quiz_detail.html'  # You can customize the template name

def create_quiz(request):
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)
    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=1)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, queryset=Question.objects.none(), prefix='questions')
        choice_formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none(), prefix='choices')

        if quiz_form.is_valid() and question_formset.is_valid() and choice_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user
            quiz.save()

            for question_form in question_formset:
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.save()

                for choice_form in choice_formset:
                    if choice_form.cleaned_data and choice_form.cleaned_data.get('text'):
                        choice = choice_form.save(commit=False)
                        choice.question = question
                        choice.save()

            return redirect('base:quiz_detail', pk=quiz.pk)  # Use the namespace here

    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(queryset=Question.objects.none(), prefix='questions')
        choice_formset = ChoiceFormSet(queryset=Choice.objects.none(), prefix='choices')

    return render(request, 'create_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'choice_formset': choice_formset,
    })


@login_required
def QuizList(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def delete_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    return redirect('base:quiz_list')

@login_required
def update_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1)
    ChoiceFormSet = modelformset_factory(Choice, form=ChoiceForm, extra=1, can_delete=True)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_formset = QuestionFormSet(request.POST, queryset=Question.objects.filter(quiz=quiz), prefix='questions')
        choice_formset = ChoiceFormSet(request.POST, queryset=Choice.objects.filter(question__quiz=quiz), prefix='choices')

        if quiz_form.is_valid() and question_formset.is_valid() and choice_formset.is_valid():
            quiz = quiz_form.save()

            for question_form in question_formset:
                question = question_form.save(commit=False)
                question.quiz = quiz
                question.save()

                for choice_form in choice_formset:
                    if choice_form.cleaned_data and choice_form.cleaned_data.get('text'):
                        choice = choice_form.save(commit=False)
                        choice.question = question
                        choice.save()

            return redirect('base:quiz_list')

    else:
        quiz_form = QuizForm(instance=quiz)
        question_formset = QuestionFormSet(queryset=Question.objects.filter(quiz=quiz), prefix='questions')
        choice_formset = ChoiceFormSet(queryset=Choice.objects.filter(question__quiz=quiz), prefix='choices')

    return render(request, 'update_quiz.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'choice_formset': choice_formset,
    })