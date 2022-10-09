from django.db import models


# Create your models here.
class BirthdayEmailSent(models.Model):
    message_sent = models.BooleanField(default=False)
    recipient = models.CharField(max_length=48)
    date = models.DateField()

    def __str__(self):
        return f'{self.recipient} - {self.date}'
