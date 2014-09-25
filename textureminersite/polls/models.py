from django.db import models

# Create your models here.
class AnnotatedImage(models.Model):
    name = models.CharField(max_length=200)
    comp_date = models.DateTimeField('date computed')


class SubImage(models.Model):
    annotatedimage = models.ForeignKey(AnnotatedImage)
    col = models.IntegerField(default=0)
    row = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    synth_score = models.FloatField(default=0)


