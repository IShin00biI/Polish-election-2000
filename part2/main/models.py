from django.db import models

candidates = [
    'grabowski',
    'ikonowicz',
    'kalinowski',
    'korwin',
    'krzaklewski',
    'kwasniewski',
    'lepper',
    'lopuszanski',
    'olechowski',
    'pawlowski',
    'walesa',
    'wilecki'
]


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


class Voivodeship(Area):
    name = models.CharField('Nazwa', max_length=32, primary_key=True)

    def __str__(self):
        return "Województwo %s" % self.name

    def children(self):
        return self.district_set.all()


class District(Area):
    county = models.ForeignKey(Voivodeship, verbose_name='Województwo', on_delete=models.CASCADE)

    def __str__(self):
        return "Okręg %s" % self.id

    def children(self):
        return self.commune_set.all()


class Commune(Area):
    district = models.ForeignKey(District, verbose_name='Okręg', on_delete=models.CASCADE)
    name = models.CharField('Nazwa', max_length=255)
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

    def valid(self):
        attr_sum = 0
        for candidate in candidates:
            attr_sum += getattr(self, candidate)
        return attr_sum

    def given(self):
        return self.valid() + self.invalid
