from django.db import models

class Commune(models.Model):
    county = models.CharField(max_length=32)
    area = models.IntegerField()
    name = models.CharField(max_length=255)
    subareas = models.IntegerField()
    people = models.IntegerField()
    cards = models.IntegerField()
    invalid = models.IntegerField()
    grabowski = models.IntegerField()
    ikonowicz = models.IntegerField()
    kalinowski = models.IntegerField()
    korwin = models.IntegerField()
    krzaklewski = models.IntegerField()
    kwasniewski = models.IntegerField()
    lepper = models.IntegerField()
    lopuszanski = models.IntegerField()
    olechowski = models.IntegerField()
    pawlowski = models.IntegerField()
    walesa = models.IntegerField()
    wilecki = models.IntegerField()

    def __str__(self):
        return "Commune %s" % self.name
