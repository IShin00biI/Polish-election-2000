from django.db import models

from .dictionaries import *


class Area(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return "%s %s" % (area_names[type(self).__name__.lower()], self.pk)

    def children(self):
        return []

    def sum_attr(self, attr):
        attr_sum = 0
        for child in self.children():
            value = getattr(child, attr)
            if callable(value):
                value = value()
            attr_sum += value
        return attr_sum

    def valid(self):
        return self.sum_attr("valid")

    def invalid(self):
        return self.sum_attr("invalid")

    def cards(self):
        return self.sum_attr("cards")

    def subareas(self):
        return self.sum_attr("subareas")

    def people(self):
        return self.sum_attr("people")

    def given(self):
        return self.sum_attr("given")

    def grabowski(self):
        return self.sum_attr("grabowski")

    def ikonowicz(self):
        return self.sum_attr("ikonowicz")

    def kalinowski(self):
        return self.sum_attr("kalinowski")

    def korwin(self):
        return self.sum_attr("korwin")

    def krzaklewski(self):
        return self.sum_attr("krzaklewski")

    def kwasniewski(self):
        return self.sum_attr("kwasniewski")

    def lepper(self):
        return self.sum_attr("lepper")

    def lopuszanski(self):
        return self.sum_attr("lopuszanski")

    def olechowski(self):
        return self.sum_attr("olechowski")

    def pawlowski(self):
        return self.sum_attr("pawlowski")

    def walesa(self):
        return self.sum_attr("walesa")

    def wilecki(self):
        return self.sum_attr("wilecki")


class Country(Area):
    name = models.CharField('Nazwa', max_length=32, primary_key=True)

    def __str__(self):
        return "%s" % self.pk

    def children(self):
        return self.voivodeship_set.all()


class Voivodeship(Area):
    name = models.CharField('Nazwa', max_length=32, primary_key=True)
    country = models.ForeignKey(Country,
                                verbose_name=area_names['country'],
                                on_delete=models.CASCADE)


    def children(self):
        return self.district_set.all()


class District(Area):
    voivodeship = models.ForeignKey(Voivodeship,
                                    verbose_name=area_names['voivodeship'],
                                    on_delete=models.CASCADE)

    def children(self):
        return self.commune_set.all()


class Commune(Area):
    district = models.ForeignKey(District, verbose_name='Okręg', on_delete=models.CASCADE)
    name = models.CharField('Nazwa', max_length=255)
    subareas = models.IntegerField(stat_names['subareas'])
    people = models.IntegerField(stat_names['people'])
    cards = models.IntegerField(stat_names['cards'])
    invalid = models.IntegerField(stat_names['invalid'])
    grabowski = models.IntegerField(candidate_names['grabowski'])
    ikonowicz = models.IntegerField(candidate_names['ikonowicz'])
    kalinowski = models.IntegerField(candidate_names['kalinowski'])
    korwin = models.IntegerField(candidate_names['korwin'])
    krzaklewski = models.IntegerField(candidate_names['krzaklewski'])
    kwasniewski = models.IntegerField(candidate_names['kwasniewski'])
    lepper = models.IntegerField(candidate_names['lepper'])
    lopuszanski = models.IntegerField(candidate_names['lopuszanski'])
    olechowski = models.IntegerField(candidate_names['olechowski'])
    pawlowski = models.IntegerField(candidate_names['pawlowski'])
    walesa = models.IntegerField(candidate_names['walesa'])
    wilecki = models.IntegerField(candidate_names['wilecki'])

    def __str__(self):
        return "Gmina %s" % self.name

    def valid(self):
        attr_sum = 0
        for candidate in candidates:
            attr_sum += getattr(self, candidate)
        return attr_sum

    def given(self):
        return self.valid() + self.invalid
