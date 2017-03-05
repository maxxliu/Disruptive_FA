from __future__ import unicode_literals

from django.db import models

# Create your models here.
class risk(models.Model):
	ANSWER_CHOICES = (
		('SD', 'Strongly Disagree'),
		('D', 'Disagree'),
		('N', 'Neutral'),
		('A', 'Agree'),
		('SA', 'Strongly Agree')
	)
	question = models.TextField()
	answer = models.CharField(
		max_length=20,
		choices=ANSWER_CHOICES,
		default='N'
	)

	def __str__(self):
		return self.question, self.answer