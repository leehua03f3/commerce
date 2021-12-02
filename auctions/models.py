from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    pass

class AuctionList(models.Model):
	def category_choices():
		return (
			("Others", "Others"),
	        ("Home", "Home"),
	        ("Appliances", "Appliances"),
	        ("Toys", "Toys"),
	        ("Computers", "Computers"),
	        ("Collectables", "Collectables")
    	)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_auctions", default='1')
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500, default="")
	start_bid = models.IntegerField(default=1, validators=[MinValueValidator(1)])
	image_url = models.CharField(max_length=500)
	category = models.CharField(max_length=100, choices=category_choices())
	status = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.id} | {self.title} - {self.description} - {self.start_bid} - {self.category} - {self.user}"

class Bid(models.Model):
	item = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="item_bid")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
	bid = models.IntegerField(default='0', blank=True)
	watchlist = models.BooleanField(default=False)
	
	def __str__(self):
		return f"{self.id} | {self.user} - {self.item} - {self.bid} - {self.watchlist}"

class Comment(models.Model):
	item = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="item_comment")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
	comment = models.CharField(max_length=1000, blank=True)