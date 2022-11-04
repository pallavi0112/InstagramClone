from distutils.command.upload import upload
from email import message
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(
        User, related_name="followers", blank="True")
    following = models.ManyToManyField(
        User, related_name="following", blank="True")
    profile_picture = models.ImageField(upload_to='ProfileImages', null=True)
    

class POST(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    Image = models.ImageField(upload_to='POST', null=True)
    post_address = models.CharField(default=" ", max_length=1024 , null=True)
    caption = models.CharField(default=" ", max_length=1024, null=True)
    likes = models.ManyToManyField(User, blank=True)
    is_like = models.BooleanField(default=False)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile")


class Reels(models.Model):
    profile = models.ForeignKey(Profile,null=False, on_delete=models.CASCADE)
    reels = models.FileField(upload_to='Reels')
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

class Story(models.Model):
    story = models.ImageField(upload_to='Story')
    story2 = models.FileField(upload_to='Story', default="")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        # Sender Message Function
        sender_message = Message(
            user=from_user,
            sender=from_user,
            reciepient=to_user,
            body=body,
            is_read=True
        )
        sender_message.save( )
        
        # Reciepient Message Function
        reciepient_message = Message(
            user=to_user,
            sender=from_user,
            reciepient=from_user,
            body=body,
            is_read=True
        )
        reciepient_message.save( )
        return sender_message
    
    def get_message(user):
        users = []
        messages =  Message.objects.filter(user=user).values("reciepient").annotate(last=Max('date')).order_by("-last")
        for message in messages:
          users.append(
            {
                'user' : User.objects.get(pk=message['reciepient']),
                'last' : message['last'],
                'unread' : Message.objects.filter(user=user, reciepient_pk=message['reciepient'], is_read=False).count()
            }
          )
        return users