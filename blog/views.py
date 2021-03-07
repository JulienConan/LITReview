from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import logout
from django.contrib import messages

from blog.forms import TicketForm, ReviewForm
from blog.models import Ticket, Review

def home(request):
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

    return render(request, 'blog/home.html', {'datas' : datas_type})

def create_ticket(request):
    if request.method == 'POST':
        print(request)
        form = TicketForm(request.POST)
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return render(request, 'blog/home.html')

    else:
        print('pas une requete post')
        form = TicketForm()
        return render(request, 'blog/create_ticket.html', {'form' : form})

def modify_ticket(request, _id):
    try:
        old_ticket = Ticket.objects.get(id=_id)
        print('lkqjsqld')
    except Ticket.DoesNotExist:
        raise Http404("Le Ticket n'existe pas !")

    form = old_ticket

    if form.is_valid():
        form.save()
        return redirect('/home')
    else:
        print('formulaire invalide')
        form = TicketForm(instance=old_ticket)
        return render(request, 'blog/modify_ticket.html', {'form' : form})

def delete_ticket(request, _id):
    ticket_to_delete = Ticket.objects.filter(pk=_id).delete()
    return render(request, 'blog/home.html')


def create_review(request):

    form_review = ReviewForm()
    form_ticket = TicketForm()
    return render(request, 'blog/create_review.html', {'form_review' : form_review, 'form_ticket' : form_ticket})

def modify_review(request, _id):
    try:
        old_review = Review.objects.get(id=_id)
    except Review.DoesNotExist:
        raise Http404("Le Ticket n'existe pas !")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=old_review)
        print(form)

        if form.is_valid():
            form.save()
            return redirect('/home')
        else:
            print('formulaire invalide')
            form = TicketForm(instance=old_review)
            return render(request, 'blog/modify_review.html', {'form' : form})

    else:
        form_review = ReviewForm(instance=old_review)
        return render(request, 'blog/modify_review.html', {
            'form_review' : form_review,
            'ticket' : old_review.ticket})

def post(request):
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

def logout_request(request):
    logout(request)
    return redirect('main')