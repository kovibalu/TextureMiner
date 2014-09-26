from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
class AnnotatedImage(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, default='')
    comp_date = models.DateTimeField('date computed')
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    ratio = models.FloatField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def was_computed_recently(self):  # __unicode__ on Python 2
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.comp_date <= now


class SubImage(models.Model):
    annotatedimage = models.ForeignKey(AnnotatedImage)
    col = models.IntegerField(default=0)
    row = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    synth_score = models.FloatField(default=0)
    gmagavg = models.FloatField(default=0)


def __str__(self):  # __unicode__ on Python 2
        return '{}: {} {} {} {}'.format(self.annotatedimage.name, self.col, self.row, self.width, self.height)

