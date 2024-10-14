from django.db import models
from django.contrib.auth.models import User

class Spreadsheet(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Cell(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, related_name='cells')
    row = models.IntegerField()
    column = models.IntegerField()
    value = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('spreadsheet', 'row', 'column')
        
