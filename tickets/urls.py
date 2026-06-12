from django.urls import path
from .views import RegisterView, TicketDetailView, UpdateTicketStatusView, check_email, forgot_password_page, reset_password, reset_password_page
from .views import RegisterView, TestAuthView
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from .views import (RegisterView,TestAuthView,TicketCreateView,MyTicketsView)
from .views import (login_page,register_page,dashboard_page,create_ticket_page,my_tickets_page)
from .views import (admin_login,admin_dashboard_page,AdminTicketsView,admin_login_page)
from .views import DeleteTicketView


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('test/',TestAuthView.as_view(),name='test'),
    path('tickets/create/',TicketCreateView.as_view(),name='ticket-create'),
    path('tickets/',MyTicketsView.as_view(),name='my-tickets'),
    path('tickets/<int:pk>/',TicketDetailView.as_view(),name='ticket-detail'),
    path('tickets/<int:pk>/status/',UpdateTicketStatusView.as_view(),name='update-ticket-status'),
    path('', login_page, name='login-page'),
    path('register-page/', register_page, name='register-page'),
    path('dashboard/', dashboard_page, name='dashboard'),
    path('create-ticket-page/', create_ticket_page, name='create-ticket-page'),
    path('my-tickets-page/', my_tickets_page, name='my-tickets-page'),
    path('forgot-password/', forgot_password_page, name='forgot-password'),
    path('reset-password/', reset_password_page, name='reset-password-page'),
    path('reset-password-api/', reset_password, name='reset-password-api'),
    path('check-email/', check_email),
    path('reset-password-api/', reset_password),
    path('test-auth/', TestAuthView.as_view()),
    path(
    'admin-login/',
    admin_login_page,
    name='admin-login-page'
),

path(
    'admin-dashboard/',
    admin_dashboard_page,
    name='admin-dashboard'
),

path(
    'admin-login-api/',
    admin_login
),

path(
    'admin-tickets/',
    AdminTicketsView.as_view()
),

path(
    'tickets/<int:pk>/delete/',
    DeleteTicketView.as_view()
),
]