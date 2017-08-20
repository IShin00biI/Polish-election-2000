from django.db import models


class County(models.Model):
    name = models.CharField(max_length=32, primary_key=True)

    def __str__(self):
        return "Województwo %s" % self.name


class Area(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return "Okręg %s" % self.id


class Commune(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    subareas = models.IntegerField('Obwody')
    people = models.IntegerField('Uprawnieni')
    cards = models.IntegerField('Karty wydane')
    invalid = models.IntegerField('Głosy nieważne')
    grabowski = models.IntegerField('Dariusz Maciej GRABOWSKI')
    ikonowicz = models.IntegerField('Piotr IKONOWICZ')
    kalinowski = models.IntegerField('Jarosław KALINOWSKI')
    korwin = models.IntegerField('Janusz KORWIN-MIKKE')
    krzaklewski = models.IntegerField('Marian KRZAKLEWSKI')
    kwasniewski = models.IntegerField('Aleksander KWAŚNIEWSKI')
    lepper = models.IntegerField('Andrzej LEPPER')
    lopuszanski = models.IntegerField('Jan ŁOPUSZAŃSKI')
    olechowski = models.IntegerField('Andrzej Marian OLECHOWSKI')
    pawlowski = models.IntegerField('Bogdan PAWŁOWSKI')
    walesa = models.IntegerField('Lech Wałęsa')
    wilecki = models.IntegerField('Tadeusz Adam WILECKI')

    def __str__(self):
        return "Gmina %s" % self.name
