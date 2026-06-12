from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer
from .gemini_service import (categorize_ticket,generate_ai_response)
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth.decorators import user_passes_test


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer

class TestAuthView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        return Response({
            "message": f"Hello {request.user.username}"
        })
    
class TicketCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        title = request.data.get('title')
        description = request.data.get('description')

        category = categorize_ticket(
            description
        )

        ai_response = generate_ai_response(
            description
        )

        ticket = Ticket.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            ai_response=ai_response
        )

        serializer = TicketSerializer(ticket)

        return Response(serializer.data)
    
class MyTicketsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        tickets = Ticket.objects.filter(
            user=request.user
        )

        serializer = TicketSerializer(
            tickets,
            many=True
        )

        return Response(serializer.data)
    
class TicketDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:
            ticket = Ticket.objects.get(
                id=pk,
                user=request.user
            )

            serializer = TicketSerializer(ticket)

            return Response(serializer.data)

        except Ticket.DoesNotExist:

            return Response(
                {"error": "Ticket not found"},
                status=404
            )
        
class UpdateTicketStatusView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        if not request.user.is_staff:

            return Response(
                {"error": "Only admin can update status"},
                status=403
            )

        try:

            ticket = Ticket.objects.get(id=pk)

            status_value = request.data.get('status')

            allowed_status = [
                'OPEN',
                'IN_PROGRESS',
                'RESOLVED'
            ]

            if status_value not in allowed_status:

                return Response(
                    {"error": "Invalid status"},
                    status=400
                )

            ticket.status = status_value

            ticket.save()

            serializer = TicketSerializer(ticket)

            return Response(serializer.data)

        except Ticket.DoesNotExist:

            return Response(
                {"error": "Ticket not found"},
                status=404
            )
        
def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')


def create_ticket_page(request):
    return render(request, 'create_ticket.html')

def my_tickets_page(request):
    return render(request, 'my_tickets.html')

def forgot_password_page(request):
    return render(request, 'forgot_password.html')

def reset_password_page(request):
    return render(request, 'reset_password.html')

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def check_email(request):

    email = request.data.get('email')

    if not email:
        return Response({"exists": False})

    exists = User.objects.filter(email=email).exists()

    return Response({"exists": exists})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):

    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})

    except User.DoesNotExist:
        return Response({"message": "User not found"})
    
@api_view(['POST'])
def login_view(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=400
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {"error": "Invalid credentials"},
            status=401
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "username": user.username
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(
        username=username,
        password=password
    )

    if user and user.is_staff:

        refresh = RefreshToken.for_user(user)

        return Response({
            "success": True,
            "access": str(refresh.access_token)
        })

    return Response({
        "success": False,
        "error": "Invalid admin credentials"
    })

def admin_dashboard_page(request):

    return render(
        request,
        'admin_dashboard.html'
    )

class AdminTicketsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_staff:

            return Response(
                {"error":"Admin only"},
                status=403
            )

        tickets = Ticket.objects.all()

        serializer = TicketSerializer(
            tickets,
            many=True
        )

        return Response({

    "total_users":
        User.objects.count(),

    "total_tickets":
        Ticket.objects.count(),

    "open_tickets":
        Ticket.objects.filter(
            status='OPEN'
        ).count(),

    "tickets":
        serializer.data
})
    
def admin_login_page(request):

    return render(
        request,
        'admin_login.html'
    )

class DeleteTicketView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        if not request.user.is_staff:

            return Response(
                {"error":"Admin only"},
                status=403
            )

        try:

            ticket = Ticket.objects.get(id=pk)

            ticket.delete()

            return Response({
                "message":
                "Ticket deleted successfully"
            })

        except Ticket.DoesNotExist:

            return Response(
                {"error":"Ticket not found"},
                status=404
            )
        
