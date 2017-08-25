from django.test import TestCase
from django.urls import reverse

from .models import *


def exampleData():
    c = Country(name="Kraj Testowy ")
    c.full_clean()
    c.save()
    v = Voivodeship(name="Województwo-Testowe", country=c)
    v.full_clean()
    v.save()
    d = District(pk=42, voivodeship=v)
    d.full_clean()
    d.save()
    com = Commune(
        district=d,
        id=7,
        name="Gmina Testowa",
        subareas=420,
        people=1000,
        cards=900,
        invalid=50,
        grabowski=10,
        ikonowicz=11,
        kalinowski=12,
        korwin=13,
        krzaklewski=14,
        kwasniewski=15,
        lepper=16,
        lopuszanski=17,
        olechowski=18,
        pawlowski=19,
        walesa=20,
        wilecki=21
        # valid=186,
        # given=236
    )
    com.full_clean()
    com.save()


class CommuneModelTests(TestCase):

    def setUp(self):
        exampleData()

    def test_name_validation(self):
        com = Commune.objects.get(pk=7)
        com.name = "Gmina_Testowa"
        with self.assertRaises(ValidationError):
            com.full_clean()

    def test_number_validation(self):
        com = Commune.objects.get(pk=7)
        com.walesa = -1
        with self.assertRaises(ValidationError):
            com.full_clean()

    def test_integrity_validation(self):
        com = Commune.objects.get(pk=7)
        com.walesa = 100000000
        with self.assertRaises(ValidationError):
            com.clean()

    def test_dynamics_validation(self):
        com = Commune.objects.get(pk=7)
        self.assertIs(com.valid(), 186)
        self.assertIs(com.given(), 236)


class ViewTests(TestCase):

    def setUp(self):
        exampleData()

    def test_correct_search(self):
        response = self.client.get(reverse('main:search'), {'search': 'Gmina Testowa'})
        self.assertIs(response.status_code, 200)
        self.assertQuerysetEqual(response.context['results'], ['<Commune: Gmina Gmina Testowa>'])

    def test_no_arg_search(self):
        response = self.client.get(reverse('main:search'), follow=True)
        self.assertIs(len(response.redirect_chain), 1)
        self.assertEquals(response.redirect_chain[0][0], reverse('main:index'))

    def test_failed_login(self):
        response = self.client.post(reverse('main:login'), {'username': 'test-user', 'password': 'asdasd'}, follow=True)
        self.assertIs(len(response.redirect_chain), 0)
        self.assertEquals(response.context['username'], 'test-user')
        self.assertEquals(response.context['request'].user.is_authenticated(), False)
