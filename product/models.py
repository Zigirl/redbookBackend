from django.db import models


class Product(models.Model):

    groupId = models.AutoField(primary_key=True)
    userId = models.IntegerField(default=0)
    projectTitle = models.CharField(max_length=100)
    projectDesc = models.TextField()
    image = models.ImageField(upload_to="productImages")
    targetCount = models.IntegerField(default=0)
    currentCount = models.IntegerField(default=0)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    status = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)

