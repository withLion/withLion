from django import forms
from django.db import models
from .models import Event

class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    exclude = []
    widgets = {
      'start_at': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'class':'form-control', 'type':'datetime-local'}),
      'end_at': forms.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs={'class':'form-control', 'type':'datetime-local'}),
    }