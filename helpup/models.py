from django.contrib.auth.models import User
from django.db import models

# Create your models here.




class Project(models.Model):
    title = models.CharField(max_length=150)
    date_created = models.DateField()
    description = models.TextField()
    location = models.IntegerField()
    student = models.ForeignKey(User, related_name='student_projects')
    donor = models.ForeignKey(User, related_name='donor_projects', null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __unicode__(self):
        return "{}'s project {}".format(self.student, self.title)

