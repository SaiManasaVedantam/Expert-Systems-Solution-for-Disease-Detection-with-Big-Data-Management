from django.db import models


class Symptoms(models.Model):
    Name = models.CharField(max_length=25)
    # pub_date = models.DateTimeField('date published')
    def __str__(self):
		    return (str(self.Name))


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)