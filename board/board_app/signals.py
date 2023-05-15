from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Responses


@receiver(post_save, sender=Responses)
def author_not(sender, instance, created, **kwargs):
    if created:
        author = instance.post.author.email
        post = instance.post.title

        html_content = render_to_string(
            'author_not.html',
            {
                'post': instance,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Отклик на объявление: {post}',
            body=instance.text,
            from_email='lion4652@yandex.ru',
            to=[author],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()

