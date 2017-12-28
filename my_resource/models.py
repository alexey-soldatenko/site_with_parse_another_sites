from django.db import models

# Create your models here.
class URL_Parse(models.Model):
	url = models.URLField()
	minute = models.PositiveSmallIntegerField()
	second = models.PositiveSmallIntegerField()

class Parse_result(models.Model):
	url = models.URLField()
	text_encode = models.CharField(max_length=100)
	title = models.TextField()
	h1 = models.TextField()
	status = models.BooleanField(default=True)
	date = models.DateTimeField(auto_now=True)