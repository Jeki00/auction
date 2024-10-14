from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=256)

    def __str__(self):
        return self.category_name


class Bid(models.Model):
    user = models.ForeignKey(User, related_name='bids', on_delete=models.CASCADE)
    bid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True, blank=True)


class Listing(models.Model):
    user = models.ForeignKey(User, related_name='owns', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=18)
    description = models.CharField(max_length=64)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='bidPrice', null=True)
    status = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    watchlist = models.ManyToManyField(User, blank=True, related_name='listingWatchlist')
    img_url = models.CharField(max_length=1000)



class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments',on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listingComment')
    comment = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now_add=True, blank=True)




