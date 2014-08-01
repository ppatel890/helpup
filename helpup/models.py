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
    picture = models.ImageField(upload_to='project_images', blank=True, null=True)
    amount = models.FloatField()
    donate = models.FloatField(default=0)

    def __unicode__(self):
        return "{}'s project {}".format(self.student, self.title)

    def find_remaining(self):
        return '{:20,.2f}'.format(self.amount - self.donate)


class Donation(models.Model):
    donation_amount = models.FloatField()
    project = models.ForeignKey(Project, related_name='project_donations')
    donor = models.ForeignKey(User, related_name='donor_donations')
    date = models.DateField()

    def __unicode__(self):
        return "{}'s donation to {}".format(self.donor, self.project)

    def format_amount(self):
        return '{:20,.2f}'.format(self.donation_amount)



