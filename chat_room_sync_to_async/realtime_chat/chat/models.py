# chat/models.py
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255)

class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
    ]

    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.name} - {self.message_type}"
