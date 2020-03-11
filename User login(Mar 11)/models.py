from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Article(models.Model):
	title=models.CharField("titile",max_length=50)
	Author=models.CharField("Author",max_length=50) #Change "" to author
	created_date=models.DateField("Created Date",auto_now_add=True)
	modify_date=models.DateField("Modify Date",auto_now=True)
	content=models.TextField()	
	is_show=models.BooleanField()

	class Meta:
		db_table="article"

	def __str__(self):
		return self.title

class MyUser(AbstractUser):
	
	RewardPoints=models.IntegerField('Reward Points',default=0)

	class Meta:
		db_table='MyUser'
	def __str__(self):
		return self.username

