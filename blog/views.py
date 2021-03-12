from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from authentification.views import main
from blog.forms import TicketForm, ReviewForm
from blog.models import Ticket, Review, UserFollows
from authentification.models import CustomUser


def flux(request):
    if request.user.is_authenticated:
        users_list_flux = [
            user.followed_user for user in UserFollows.objects.filter(user=request.user)]
        users_list_flux += CustomUser.objects.filter(username=request.user)
        tickets = [
            ticket for user in users_list_flux for ticket in Ticket.objects.filter(user=user)]
        reviews = [review for review in Review.objects.all()]
        datas = tickets + reviews
        datas = sorted(datas, key=lambda data: data.time_created, reverse=True)
        datas_type = []
        for data in datas:
            if isinstance(data, Ticket):
                datas_type.append(("ticket", data))
            elif isinstance(data, Review):
                datas_type.append(("review", data, range(data.rating)))
        titre = 'Flux'

        return render(request, 'blog/flux.html', {'datas': datas_type, 'titre': titre})

    else:
        return redirect('main')


def create_ticket(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket = Ticket(title=request.POST['title'],
                            description=request.POST['description'],
                            image=request.FILES['image'],
                            user=request.user)
            ticket.save()
            return redirect('flux')

        else:
            form = TicketForm()
            return render(request, 'blog/create_ticket.html', {'form': form})

    else:
        return redirect('main')


def modify_ticket(request, _id):
    if request.user.is_authenticated:
        ticket = get_object_or_404(Ticket, pk=_id)
        if request.method == 'POST':
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            if form.is_valid():
                form.save()
            return redirect('post')
        else:
            form = TicketForm(instance=ticket)
            return render(request, 'blog/modify_ticket.html', {'form': form, 'image' : ticket.image.url})
    else:
        return redirect('main')


def delete_ticket(request, _id):
    if request.user.is_authenticated:
        ticket_to_delete = get_object_or_404(Ticket, pk=_id)
        if ticket_to_delete.user == request.user:
            ticket_to_delete.delete()
        return redirect('post')
    else:
        return redirect('main')


def create_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            ticket = Ticket(title=request.POST['title'],
                            description=request.POST['description'],
                            image=request.FILES['image'],
                            user=request.user,
                            response=True)
            ticket.save()
            review = Review(ticket=ticket,
                            rating=request.POST['rating'],
                            headline=request.POST['headline'],
                            body=request.POST['body'],
                            user=request.user)
            review.save()
            return redirect('flux')

        else:

            form_ticket = TicketForm()
            form_review = ReviewForm()
            return render(request, 'blog/create_review.html', {'form_review': form_review, 'form_ticket': form_ticket})
    else:
        return redirect('main')


def create_response_review(request, _id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            ticket = get_object_or_404(Ticket, pk=_id)
            ticket.response = True
            ticket.save()
            review = Review(ticket=ticket,
                            rating=request.POST['rating'],
                            headline=request.POST['headline'],
                            body=request.POST['body'],
                            user=request.user)
            review.save()
            print('save')
            return redirect('flux')

        else:
            ticket = get_object_or_404(Ticket, pk=_id)
            form_review = ReviewForm()
            return render(request, 'blog/create_response_review.html', {'form_review': form_review, 'ticket': ticket})
    else:
        return redirect('main')
    pass


def modify_review(request, _id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=_id)
        print(review.ticket)
        if request.method == 'POST':
            review.rating = int(request.POST['rating'])
            review.headline = request.POST['headline']
            review.body = request.POST['body']
            form = ReviewForm(instance=review)
            try:
                form.is_valid()
                form.save()
            except:
                pass
            return redirect('post')     
        else:
            form_review = ReviewForm(instance=review)
            return render(request, 'blog/modify_review.html', {
                'form_review': form_review,
                'ticket': review.ticket})
    else:
        return redirect('main')


def delete_review(request, _id):
    if request.user.is_authenticated:
        review_to_delete = get_object_or_404(Review, pk=_id)
        if review_to_delete.user == request.user:
            ticket = review_to_delete.ticket
            ticket.response = False
            ticket.save()
            review_to_delete.delete()
        return redirect('post')
    else:
        return redirect('main')


def post(request):
    if request.user.is_authenticated:
        tickets = [ticket for ticket in Ticket.objects.filter(
            user=request.user)]
        reviews = [review for review in Review.objects.filter(
            user=request.user)]
        datas = tickets + reviews
        datas = sorted(datas, key=lambda data: data.time_created, reverse=True)
        datas_type = []
        for data in datas:
            if isinstance(data, Ticket):
                datas_type.append(("ticket", data))
            elif isinstance(data, Review):
                datas_type.append(("review", data))

        return render(request, 'blog/post.html', {'datas': datas_type})
    else:
        return redirect('main')


def follow(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                followed_user = CustomUser.objects.get(
                    username=request.POST['followed_user'])
            except ObjectDoesNotExist:
                return redirect('follow')
            user = CustomUser.objects.get(username=request.user)
            new_user_followed = UserFollows(
                user=user, followed_user=followed_user)
            new_user_followed.save()
            return redirect('follow')
        else:
            followed_user = UserFollows.objects.filter(user=request.user)
            users_follow_user = UserFollows.objects.filter(
                followed_user=request.user)
            return render(request, 'blog/follow.html', {'followed_user': followed_user, 'users_follow_user': users_follow_user})
    else:
        return redirect('main')


def delete_follow(request, _id):
    if request.user.is_authenticated:
        user_follow = UserFollows.objects.get(pk=_id).delete()
        return redirect('follow')
    else:
        return redirect('main')


def logout_request(request):
    logout(request)
    return redirect('main')
