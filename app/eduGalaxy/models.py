from django.db import models
from django.utils import timezone


class EduGalaxyUser(models.Model):

    user_email = models.EmailField(max_length=50)
    user_pwd = models.CharField(max_length=15)
    user_nickname = models.CharField(max_length=15)
    user_age = models.IntegerField()
    user_job = models.CharField(max_length=30)
    user_sex = models.BooleanField()
    user_address1 = models.CharField(max_length=100)
    user_address2 = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=15)
    # user_post = models.ForeignKey('', on_delete=models.CASCADE)
    user_receive_email = models.BooleanField()
    user_confirm = models.BooleanField()
    user_created_date = models.DateTimeField(default=timezone.now)
    user_signup_ip = models.CharField(max_length=100)

    # published_date = models.DateTimeField(blank=True, null=True)
    #
    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()
    #
    def __str__(self):
        return self.user_email + ' ' + self.user_nickname

