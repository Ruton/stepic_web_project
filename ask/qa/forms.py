# -*- coding: utf-8 -*-
from django import forms
from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=255)
    text = forms.CharField(widget=forms.Textarea)

    def clear_title(self):
        message = self.cleaned_data['title']
        return message

    def clear_text(self):
        message = self.cleaned_data['text']
        return message


    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'question']
