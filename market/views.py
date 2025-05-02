from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ListingForm, MessageForm, BuyListingsForm
from .models import Listing, Message, CustomUser
from django.core.paginator import Paginator
from django.db.models import Q
import requests

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'market/register.html', {'form': form})

@login_required
def create_listing(request):
    today = timezone.now().date()
    user_post_count = Listing.objects.filter(user=request.user, created_at__date=today).count()

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            max_allowed = 3 + request.user.extra_listings
            if user_post_count >= max_allowed:
                error = f"You have reached your daily quota of 3 listings. Please buy more to post additional listings."
                return render(request, 'market/create_listing.html', {'form': form, 'error': error})

            listing = form.save(commit=False)
            listing.user = request.user
            listing.status = 'Available'
            listing.save()
            return redirect('/')
    else:
        form = ListingForm()

    return render(request, 'market/create_listing.html', {'form': form})

@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, user=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'market/edit_listing.html', {'form': form})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, user=request.user)

    if request.method == 'POST':
        listing.delete()
        return redirect('/')
    
    return render(request, 'market/delete_listing.html', {'listing': listing})

@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(CustomUser, id=receiver_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()

    return render(request, 'market/send_message.html', {'form': form, 'receiver': receiver})

@login_required
def inbox(request):
    messages = Message.objects.filter(
        Q(receiver=request.user) | Q(sender=request.user)
    ).order_by('-timestamp')
    return render(request, 'market/inbox.html', {'messages': messages, 'user': request.user})

@login_required
def home(request):
    query = request.GET.get('q')
    listings = Listing.objects.filter(status='Available')

    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    listings = listings.order_by('-created_at')

    paginator = Paginator(listings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'market/home.html', {'page_obj': page_obj, 'query': query})

@login_required
def buy_listings(request):
    if request.method == 'POST':
        form = BuyListingsForm(request.POST)
        if form.is_valid():
            number_to_buy = form.cleaned_data['number_of_listings']
            
            access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MzYzOTg2LCJpYXQiOjE3NDU3MjM5ODYsImp0aSI6IjA1MmZiMzFmYTQ2ODRhZmM4YTc3OWNkN2U2ZTY5YTNkIiwidXNlcl9pZCI6ODJ9.RAjfHJFYw0BvlbVqLAUvGnqzPr6RA91eyta922uh4Dc"
            email = request.user.email
            group_number = "group26"

            headers = {'Authorization': f'Bearer {access_token}'}
            data = {"amount": number_to_buy}

            response = requests.post(
                f"https://jcssantos.pythonanywhere.com/api/{group_number}/{group_number}/player/{email}/pay",
                headers=headers,
                data=data
            )

            if response.status_code == 200:
                user = CustomUser.objects.get(id=request.user.id)
                user.extra_listings += number_to_buy
                user.save()

                message = f"Successfully purchased {number_to_buy} extra daily listings!"
                return render(request, 'market/buy_listings.html', {'form': form, 'message': message})
            else:
                error_msg = f"Transaction failed: {response.json().get('detail', 'Unknown error')}"
                return render(request, 'market/buy_listings.html', {'form': form, 'error': error_msg})

    else:
        form = BuyListingsForm()

    return render(request, 'market/buy_listings.html', {'form': form})