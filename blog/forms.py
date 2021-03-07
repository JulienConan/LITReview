from django.forms import forms, ModelForm

from blog.models import Ticket, Review, UserFollows

class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		fields = ['title', 'description', 'image']

class ReviewForm(ModelForm):
	class Meta:
		model = Review
		fields = ['ticket', 'headline', 'rating', 'body']