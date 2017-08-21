from django.db import models

from .dictionaries import candidates, stats


class Area(models.Model):
    class Meta:
        abstract = True

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


class Voivodeship(Area):
    name = models.CharField('Nazwa', max_length=32, primary_key=True)

    def __str__(self):
        return "Województwo %s" % self.name

    def children(self):
        return self.district_set.all()


class District(Area):
    voivodeship = models.ForeignKey(Voivodeship, verbose_name='Województwo', on_delete=models.CASCADE)

    def __str__(self):
        return "Okręg %s" % self.id

    def children(self):
        return self.commune_set.all()


class Commune(Area):
    district = models.ForeignKey(District, verbose_name='Okręg', on_delete=models.CASCADE)
    name = models.CharField('Nazwa', max_length=255)
    subareas = models.IntegerField(stats['subareas'])
    people = models.IntegerField(stats['people'])
    cards = models.IntegerField(stats['cards'])
    invalid = models.IntegerField(stats['invalid'])
    grabowski = models.IntegerField(candidates['grabowski'])
    ikonowicz = models.IntegerField(candidates['ikonowicz'])
    kalinowski = models.IntegerField(candidates['kalinowski'])
    korwin = models.IntegerField(candidates['korwin'])
    krzaklewski = models.IntegerField(candidates['krzaklewski'])
    kwasniewski = models.IntegerField(candidates['kwasniewski'])
    lepper = models.IntegerField(candidates['lepper'])
    lopuszanski = models.IntegerField(candidates['lopuszanski'])
    olechowski = models.IntegerField(candidates['olechowski'])
    pawlowski = models.IntegerField(candidates['pawlowski'])
    walesa = models.IntegerField(candidates['walesa'])
    wilecki = models.IntegerField(candidates['wilecki'])

    def __str__(self):
        return "Gmina %s" % self.name

    def valid(self):
        attr_sum = 0
        for candidate, _ in candidates.items():
            attr_sum += getattr(self, candidate)
        return attr_sum

    def given(self):
        return self.valid() + self.invalid
