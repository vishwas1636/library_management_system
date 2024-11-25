from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class AddBooks(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    availability_status = models.CharField(
        max_length=10,
        choices=[('available', 'Available'), ('borrowed', 'Borrowed'), ('reserved', 'Reserved')],
        default='available'
    )

    def __str__(self):
        return self.title

class Barrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(AddBooks, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} is borrowes from {self.book.title}"