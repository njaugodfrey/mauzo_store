from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.


PROFILE_CHOICES = [
    ('sales', 'Sales'),
    ('accounts', 'Accounts'),
]


class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #avatar = models.ImageField(upload_to='avatar', default='avatar/default.png')
    department = models.CharField(
        max_length=50, choices=PROFILE_CHOICES, default='Sales'
    )

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return 'Profile for user {}'.format(self.user.username)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
