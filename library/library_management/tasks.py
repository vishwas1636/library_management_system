from celery import shared_task

@shared_task(bind=True)
def add(self):
    for i in range(10):
        print(i)
    return 'Done vishwas'

@shared_task
def send_overdue_remainders():
    from django.utils.timesince import now
    from django.core.mail import send_mail
    from .models import Barrow
    overdue = Barrow.objects.filter(due_date__lt = now(), returned=False)
    for borrow in overdue:
        send_mail(
            "overdue book remainder",
            f"Dear {borrow.user.username}, \n\n"
            f"The book '{borrow.book.title}' is overdue. Please return it.",
            "library@gmail.com",
            [borrow.user.email],
        )