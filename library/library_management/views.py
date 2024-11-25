from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import AddBooks, Barrow
from .serializers import BookSerializeers, UserSerializer, BorrowSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils.timezone import now

def hello_world(request):
    from library_management.tasks import add
    add.delay()
    return HttpResponse('its running')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book(request):
    if request.method == 'POST':
        serializer = BookSerializeers(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book(request,id):
    try:
        book = AddBooks.objects.get(id=id)
        serializer = BookSerializeers(book)
        return Response(serializer.data)
    except AddBooks.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_all(request):
    try:
        book=AddBooks.objects.all()
        serializer = BookSerializeers(book,many=True)
        return Response(serializer.data)
    except:
        return Response({'error': 'Books are not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT','PATCH'])
def book_update(request,id):
    try:
        book = AddBooks.objects.get(id=id)
    except:
        return Response({'error':'no book record'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = BookSerializeers(book , data=request.data)
    if request.method == 'PATCH':
        serializer = BookSerializeers(book, data = request.data ,partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_book(request,id):
    try:
        book = AddBooks.objects.get(id=id)
        book.delete()
        return Response({'message':'successfully deleted'},status=status.HTTP_204_NO_CONTENT)
    except AddBooks.DoesNotExist:
        return Response({'error':'no book record'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_user(request,id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data , status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT','PATCH'])
def update_user(request,id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({'message': 'User successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AttributeError:
            return Response({'error': 'No token found'}, status=status.HTTP_400_BAD_REQUEST)

from django.utils import timezone
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def barrow_book(request, id):
    try:
        book = AddBooks.objects.get(id=id)
        if book.availability_status != 'available':
            return Response({'error': 'Book is not available for borrowing.'}, status=status.HTTP_400_BAD_REQUEST)
        barrow_record = Barrow.objects.create(
            user=request.user,
            book=book,
            borrow_date=timezone.now(),
            is_returned=False 
        )
        book.availability_status = 'borrowed'
        book.save()
        barrow_book = BorrowSerializer(barrow_record)
        return Response(barrow_book.data, status=status.HTTP_201_CREATED)
    except AddBooks.DoesNotExist:
        return Response({'error':'book not found'},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def return_book(request, id):
    try:
        book = AddBooks.objects.get(id=id)
        book_record = Barrow.objects.filter(user=request.user, is_returned = False).first()
        if not book_record:
            return Response({'error':'book is not found to return'}, status=status.HTTP_404_NOT_FOUND)
        book_record.is_returned = True
        book_record.return_date = timezone.now()
        book_record.save()
        book.availability_status = 'available'
        book.save()
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)
        
    except AddBooks.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def barrow_history(request, id):
    try:
        user = User.objects.get(id=id)
        history = Barrow.objects.filter(user=user).order_by('-borrow_date').values('user__username', 'user__first_name', 'borrow_date')
        borrow_history = [
            {
                'username': item['user__username'],
                'first_name': item['user__first_name'],
                'borrow_date': item['borrow_date']
            }
            for item in history
        ]
        return Response(borrow_history, status=status.HTTP_200_OK)
    except User.DoesNotExist as e:
        print(e)
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 
    
@api_view(['GET'])
def book_availability_status(request, id):
    try:
        book = AddBooks.objects.get(id=id)
        status_message = {
            'available': 'This book is available for borrowing.',
            'borrowed': 'This book is currently borrowed.',
        }
        return Response({
            'book_id':book.id,
            'title':book.title,
            'availability_status': book.availability_status,
            'status_message':status_message.get(book.availability_status,"status not found")
        }, status=status.HTTP_200_OK)
    except book.DoesNotExist:
        return Response({'error':'book is not found'},status=status.HTTP_404_NOT_FOUND)
    
from django.shortcuts import render 
def overdue_books(request):
    overdue = Barrow.objects.filter(due_date__lt=now(), returned=False)
    return render(request, "overdue_books.html", {"overdue_books": overdue})