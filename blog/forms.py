from django.forms import ModelForm
from django import forms

from blog.models import Ticket, Review, UserFollows

class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		fields = ['title', 'description', 'image']

class ReviewForm(ModelForm):
	class Meta:
		model = Review

		fields = ['ticket', 'headline', 'rating', 'body']
	CHOICES=[
		('0', '0'),
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5')]
	rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)