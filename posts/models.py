from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    url = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)   # whomever creates the post has to be logged in
    votes_total = models.IntegerField(default=1) # specify default value

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')
