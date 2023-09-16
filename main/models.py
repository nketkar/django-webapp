from django.db import models
from django.conf import settings

from geoposition.fields import GeopositionField


class UserProfile(models.Model):
    '''
    Store additional user information. Linked to the user model.
    '''

    company = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )


class Question(models.Model):
    '''Store secret question'''

    question = models.CharField(max_length=500)

    def __str__(self):
        return self.question


class Answer(models.Model):
    '''
    Stores users' answers provided in the activation process.
    '''

    answer = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    class Meta:
        unique_together = ('answer', 'question')


class UserGeoKey(models.Model):
    '''
    Store user searched locations.
    '''

    created = models.DateTimeField(auto_now_add=True)
    position = GeopositionField()
    address = models.CharField(blank=True, max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='geokeys'
    )
    geokey = models.CharField(max_length=500)
    nickname = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ('-created', 'address')
