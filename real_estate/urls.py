from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from listings.views import (
    listing_list,
    listing_detail,
    listing_create,
    listing_update,
    listing_delete,
    register_view,
    login_view,
    logout_view,
    add_review,
    book_listing,
    profile_view
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", listing_list, name="listings"),
    path("add-listing/", listing_create),

    path("listings/<int:pk>/", listing_detail, name="listing_detail"),
    path("listings/<int:pk>/edit/", listing_update),
    path("listings/<int:pk>/delete/", listing_delete),

    path("listings/<int:pk>/review/", add_review, name="add_review"),
    path("listings/<int:pk>/book/", book_listing, name="book_listing"),

    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("profile/", profile_view, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
