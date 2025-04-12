from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import ListingForm
from .models import Listing

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
            if user_post_count >= 3:
                error_msg = "You’ve reached your daily post limit of 3. Buy more posts to continue."
                return render(request, 'market/create_listing.html', {'form': form, 'error': error_msg})
            
            listing = form.save(commit=False)
            listing.user = request.user
            listing.status = 'Available'
            listing.save()
            return redirect('/')  # or some confirmation page
    else:
        form = ListingForm()

    return render(request, 'market/create_listing.html', {'form': form})

@login_required
def home(request):
    return render(request, 'market/home.html')