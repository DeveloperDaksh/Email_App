from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_default = models.EmailField(max_length=255)
    email_host_user = models.EmailField(max_length=225)
    email_host_password = models.CharField(max_length=225)
    email_host = models.CharField(max_length=225)
    email_port = models.CharField(max_length=225)
    email_server = models.CharField(max_length=225)
    email_backend = models.CharField(max_length=225)
    email_default_text = models.TextField()

    def __str__(self):
        return self.user

    class Meta:
        db_table = "EmailUsers"


class PhoneBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=225)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "PhoneBook"
