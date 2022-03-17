from main.models import String
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(signal=post_save, sender=String)
def add_weight(instance, sender, created, **kwargs):
    letter_weight = {chr(num):num for num in range(ord("A"), ord("Z")+1)}
    letter_weight.update({chr(num):num for num in range(ord("a"), ord("z")+1)})
    
    if created:
        weight = 0
        for char in instance.string:
            weight += letter_weight.get(char, 0)
        instance.weight = weight
        instance.save()