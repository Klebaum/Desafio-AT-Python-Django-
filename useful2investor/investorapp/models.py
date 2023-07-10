from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    """Model representing a user.
    
    Attributes:
        name (CharField): The name of the user.
    """
    name = models.CharField(max_length=100)


class Email(models.Model):
    """Model representing an email.
    
    Attributes:
        address (EmailField): The email address.
        user (ForeignKey): The user that owns the email.
    """
    address = models.EmailField(default="example@example.com")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Asset(models.Model):
    """Model representing an asset.
    
    Attributes:
        name (CharField): The name of the asset.
        verification_time (PositiveIntegerField): The time interval between verifications.
        superior_limit (DecimalField): The superior limit of the asset.
        inferior_limit (DecimalField): The inferior limit of the asset.
        user (ForeignKey): The user that owns the asset.
        updated_at (DateTimeField): The date and time of the last update.
    """
    name = models.CharField(max_length=100)
    verification_time = models.PositiveIntegerField()
    superior_limit = models.DecimalField(max_digits=10, decimal_places=2)
    inferior_limit = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Override the save method to update the updated_at field.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
