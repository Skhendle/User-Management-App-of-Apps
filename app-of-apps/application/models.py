from django.db import models
import uuid

def generate_api_key():
    # Generates a random hexadecimal UUID string
    return uuid.uuid4().hex

class Application(models.Model):
    # The id field is automatically added by Django.
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    API_KEY = models.CharField(
        max_length=255,
        unique=True,
        default=generate_api_key,  # Call this function to generate a default value.
        editable=False  # Optionally make it uneditable in the admin.
    )
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    deleted_ts = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
