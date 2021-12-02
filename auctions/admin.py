from django.contrib import admin

from .models import User, AuctionList, Bid, Comment

class UserAdmin(admin.ModelAdmin):
	list_display = ("id", "username", "password", "email")

class AuctionListAdmin(admin.ModelAdmin):
	list_display = ("id", "user", "title", "description", "start_bid", "category", "status", "image_url")
	list_editable = ("title", "description", "start_bid", "category", "status", "image_url")

class BidAdmin(admin.ModelAdmin):
	list_display = ("id", "item", "user", "bid", "watchlist")
	list_editable = ("bid", "watchlist")

class CommentAdmin(admin.ModelAdmin):
	list_display = ("id", "item", "user", "comment")
	list_editable = ("comment",)

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(AuctionList, AuctionListAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)