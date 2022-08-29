"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static
import authentication.views
import reviews.views

"""give a path to all site url, a class to handle the request and a name"""
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('home/', reviews.views.Home.as_view(), name='home'),
    path('posts/<int:user_id>',
         reviews.views.PostsList.as_view(),
         name='posts'),

    # authentication Views
    path('', authentication.views.LoginPageView.as_view(),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/',
         authentication.views.SignupPageView.as_view(),
         name='signup'),

    #follow un-follow
    path('follow/<int:user_id>',
         reviews.views.Follow.as_view(),
         name='follow'),

    # reviews Views
    path('tickets/add/', reviews.views.AddTicket.as_view(), name='add_ticket'),
    path('add_review/',
         reviews.views.AddTicketReview.as_view(),
         name='add_review'),
    path('tickets/<int:ticket_id>/',
         reviews.views.TicketDetail.as_view(),
         name='ticket-detail'),
    path('tickets/<int:ticket_id>/add_review/',
         reviews.views.AddTicketReview.as_view(),
         name='add_review_to_ticket'),

    path('reviews/<int:review_id>/',
         reviews.views.ReviewDetail.as_view(),
         name='review-detail')
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
