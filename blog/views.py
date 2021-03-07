from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import logout
from django.contrib import messages

from authentification.views import main
from blog.forms import TicketForm, ReviewForm
from blog.models import Ticket, Review

def flux(request):
    if request.user.is_authenticated:
        tickets = [ticket for ticket in Ticket.objects.all()]
        reviews = [review for review in Review.objects.all()]
        datas = tickets + reviews
        datas = sorted(datas, key= lambda data: data.time_created, reverse=True)
        datas_type = []
        for data in datas:
            if isinstance(data, Ticket):
                datas_type.append(("ticket", data))
            elif isinstance(data, Review):
                datas_type.append(("review", data))

        return render(request, 'blog/flux.html', {'datas' : datas_type})

    else:
        return redirect('main')

def create_ticket(request):
    if request.user.is_authenticated :
        if request.method == 'POST':
            ticket=Ticket(title=request.POST['title'],
                description=request.POST['description'],
                image=request.FILES['image'],
                user=request.user)
            ticket.save()
            return redirect('flux')

        else:
            form = TicketForm()
            return render(request, 'blog/create_ticket.html', {'form' : form})

    else :
        return redirect('main')


def modify_ticket(request, _id):
    if request.user.is_authenticated :
        ticket = get_object_or_404(Ticket, pk=_id)
        if request.method == 'POST' :
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
            return redirect('flux')
        else:
            form = TicketForm(instance = ticket)
            return render(request, 'blog/modify_ticket.html', {'form' : form})
    else :
        return redirect('main')


def delete_ticket(request, _id):
    if request.user.is_authenticated :
        ticket_to_delete = get_object_or_404(Ticket, pk=_id)
        if ticket_to_delete.user == request.user:
            ticket_to_delete.delete()
        return redirect('flux')
    else :
        return redirect('main')


def create_review(request):
    if request.user.is_authenticated :
        if request.method == 'POST':
            ticket = Ticket(user=request.user)
            review = Review(user=request.user)
            form_ticket = TicketForm(request.POST, instance=ticket)
            if form_ticket.is_valid():
                form_ticket.save()

        else:
            form_review = ReviewForm()
            form_ticket = TicketForm()
            return render(request, 'blog/create_review.html', {'form_review' : form_review, 'form_ticket' : form_ticket})
    else :
        return redirect('main')


def modify_review(request, _id):
    if request.user.is_authenticated :
        review = get_object_or_404(Review, pk=_id)
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('flux')
            else:
                pass

        else:
            form_review = ReviewForm(instance=review)
            ticket = Ticket(review.ticket)
            return render(request, 'blog/modify_review.html', {
                'form_review' : form_review,
                'ticket' : ticket})
    else :
        return redirect('main')

def post(request):
    if request.user.is_authenticated :
        tickets = [ticket for ticket in Ticket.objects.filter(user=request.user)]
        reviews = [review for review in Review.objects.filter(user=request.user)]
        datas = tickets + reviews
        datas = sorted(datas, key= lambda data: data.time_created, reverse=True)
        datas_type = []
        for data in datas:
            if isinstance(data, Ticket):
                datas_type.append(("ticket", data))
            elif isinstance(data, Review):
                datas_type.append(("review", data))

        return render(request, 'blog/post.html', {'datas' : datas_type})
    else :
        return redirect('main')

def logout_request(request):
    logout(request)
    return redirect('main')