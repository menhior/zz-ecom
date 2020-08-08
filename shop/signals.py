"""from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
	if created:
		

		group = Group.objects.get(name='customer')
		instance.groups.add(group)
		Customer.objects.get_or_create(
			user=instance,
			name=instance.first_name + ' ' + instance.last_name,
			device = device,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)"""

"""from django.core.signals import request_started
from django.dispatch import receiver

@receiver(request_started)
def my_callback(sender, **kwargs):
    print("Request finished!")"""