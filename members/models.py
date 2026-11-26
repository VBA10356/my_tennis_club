from django.db import models

# Create your models here.
class Member(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    heroName = models.CharField(max_length=255, null = True)
    movie_year = models.IntegerField(null = True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"