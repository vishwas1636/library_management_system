from typing import Any
from django.shortcuts import redirect

class EnforceAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        restricted_pages = ['overdue-books/','book/<int:id>/return/','book/<int:id>/borrow/']
        if request.path in restricted_pages and not request.user.is_authenticated:
            return redirect('login/')
        response = self.get_response(request)
        return response