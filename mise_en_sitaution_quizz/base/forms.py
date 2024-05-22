from django import forms
from .models import Quiz, Question, Choice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the quiz title'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter a description for the quiz', 'rows': 2})
        for field_name, field in self.fields.items():
            field.label = ''  # Remove the label

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the question text'})
        for field_name, field in self.fields.items():
            field.label = ''  # Remove the label

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter the choice text'})
        self.fields['is_correct'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_correct'].label = 'Correct answer'
        for field_name, field in self.fields.items():
            if field_name != 'is_correct':  # Don't remove the label for 'is_correct'
                field.label = ''  # Remove the label
