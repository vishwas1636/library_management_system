from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import hello_world,add_book,get_book,get_all,book_update,delete_book,barrow_book,return_book,book_availability_status
from .views import register_user,get_user,update_user,delete_user,LoginView,LogoutView,all_users,barrow_history,overdue_books

urlpatterns = [path('hello/',hello_world,name='hello_world'),
               path('add-book/', add_book, name='add-book'),
               path('get-book/<id>', get_book, name='get-book'),
               path('get-all/',get_all,name='get-all'),
               path('book-update/<int:id>/',book_update,name="book-update"),
               path('delete-book/<int:id>/',delete_book,name='delete-book'),
               path('api/token/',TokenObtainPairView.as_view(),name='tokenobtain'),
               path('api/token/refresh/',TokenRefreshView.as_view(),name='tokenrefresh'),
               path('user/register/',register_user,name='register'),
               path('user/all-users/',all_users,name='all_users'),
               path('user/get-user/<id>/',get_user,name='get_user'),
               path('user/update-user/<id>/',update_user,name='update_user'),
               path('user/delete/<id>/',delete_user,name='delete_user'),
               path('login/', LoginView.as_view(), name='login'),
               path('logout/', LogoutView.as_view(), name='logout'), 
               path('book/<int:id>/borrow/', barrow_book, name='borrow-book'),
               path('book/<int:id>/return/', return_book, name='return-book'),
               path('book/<int:id>/barrow-history/', barrow_history, name='barrow_history'),
               path('book/<int:id>/book-availability-status',book_availability_status,name='book_availability_status'),
               path('overdue-books/', overdue_books, name='overdue_books'),
               ]