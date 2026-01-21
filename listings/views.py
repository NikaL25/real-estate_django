from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg  # <- вот сюда
from .models import Listing, Booking, Review
from .form import ListingForm, RegisterForm, ReviewForm, BookingForm


# -------------------
# LISTINGS
# -------------------

from django.db.models import Avg

from listings import models


def listing_list(request):
    listings = Listing.objects.all()
    for listing in listings:
        # Вычисляем средний рейтинг для каждого listing
        reviews = getattr(listing, 'reviews', []).all(
        ) if hasattr(listing, 'reviews') else []
        listing.avg_rating = reviews.aggregate(
            Avg('rating'))['rating__avg'] if reviews else None
    context = {
        "listings": listings,
        "stars": range(1, 6)  # список [1,2,3,4,5] для шаблона
    }
    return render(request, "listings.html", context)


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = getattr(listing, 'reviews', []).all(
    ) if hasattr(listing, 'reviews') else []

    avg_rating = reviews.aggregate(Avg('rating'))[
        'rating__avg'] if reviews else None

    review_form = None
    booking_form = None
    if request.user.is_authenticated:
        review_form = ReviewForm()
        booking_form = BookingForm()

    context = {
        "listing": listing,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "review_form": review_form,
        "booking_form": booking_form,
        "stars": range(1, 11)  # список [1,2,3,4,5] для шаблона
    }
    return render(request, "listing.html", context)


@login_required
def listing_create(request):
    form = ListingForm()

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request, "listing_create.html", {"form": form})


@login_required
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    form = ListingForm(instance=listing)

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("/")

    return render(request, "listing_update.html", {"form": form})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.delete()
    return redirect("/")


# -------------------
# AUTH
# -------------------

def register_view(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return redirect("/")

    return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


# -------------------
# REVIEWS & BOOKINGS
# -------------------

@login_required
def add_review(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.listing = listing
        review.save()

    return redirect("listing_detail", pk=pk)


@login_required
def book_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    form = BookingForm(request.POST)

    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.listing = listing
        booking.save()

    return redirect("listing_detail", pk=pk)


@login_required
def profile_view(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).select_related('listing')
    reviews = Review.objects.filter(user=user).select_related('listing')

    return render(request, "auth/profile.html", {
        "bookings": bookings,
        "reviews": reviews
    })
