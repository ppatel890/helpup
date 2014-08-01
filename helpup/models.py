from django.contrib.auth.models import User
from django.db import models

# Create your models here.




class Project(models.Model):
    title = models.CharField(max_length=150)
    # You should probably look at Django's `auto_now_add=True` option
    date_created = models.DateField()
    description = models.TextField()
    # Location is an IntegerField? Of what? Also why have location and lat / lon?
    location = models.IntegerField()
    # It seems unlikely to me that students would also be donors, or that you would want to save the same information
    # about both long term. You should probably have StudentProfile and DonorProfile as models related to User
    student = models.ForeignKey(User, related_name='student_projects')
    donor = models.ForeignKey(User, related_name='donor_projects', null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)
    picture = models.ImageField(upload_to='project_images', blank=True, null=True)
    amount = models.FloatField()
    donate = models.FloatField(default=0)

    def __unicode__(self):
        return "{}'s project {}".format(self.student, self.title)

    # This was a good helper method to write
    def find_remaining(self):
        return '{:20,.2f}'.format(self.amount - self.donate)


class Donation(models.Model):
    donation_amount = models.FloatField()
    project = models.ForeignKey(Project, related_name='project_donations')
    donor = models.ForeignKey(User, related_name='donor_donations')
    # You should probably look at Django's `auto_now_add=True` option
    date = models.DateField()

    def __unicode__(self):
        return "{}'s donation to {}".format(self.donor, self.project)

    # Instead of this percent encoding, you can format at the template level with Django template tags
    def format_amount(self):
        return '{:20,.2f}'.format(self.donation_amount)



