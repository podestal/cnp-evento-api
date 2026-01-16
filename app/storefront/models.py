from django.db import models

class Tema(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    coordinator = models.CharField(max_length=255)
    coordinator_celphone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.description}"

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Participant(models.Model):

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dni = models.CharField(max_length=8, blank=True)
    email = models.EmailField(unique=True)
    celphone = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    activities = models.ManyToManyField(Activity, blank=True)
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True, help_text='Receipt image stored in R2 bucket')
    is_active = models.BooleanField(default=True)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"

