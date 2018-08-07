from django.db import models
from jiuchai.models import Projects
# Create your models here.


class Audit(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


class Advice(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    batch_choices = ((0, '第一批次'),
                     (1, '第二批次'))
    batch = models.SmallIntegerField(choices=batch_choices)
    advice = models.TextField()
    user = models.ForeignKey(Audit, on_delete=models.CASCADE)

