from django.db import models

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Participant(models.Model):


    participant_type_options = (
        ('N', 'Notario'),
        ('A', 'Abogado'),
        ('T', 'Trabajador notarial'),
        ('E', 'Estudiante'),
        ('G', 'Publico en general'),
    )

    participant_modalities_options = (
        ('P', 'Presencial'),
        ('V', 'Virtual'),
    )

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dni = models.CharField(max_length=8, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    celphone = models.CharField(max_length=255)
    participant_type = models.CharField(max_length=1, choices=participant_type_options)
    notary = models.CharField(max_length=255, blank=True, null=True)
    ruc = models.CharField(max_length=11, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    modality = models.CharField(max_length=1, choices=participant_modalities_options)
    activities = models.ManyToManyField(Activity, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"

