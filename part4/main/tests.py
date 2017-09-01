from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

from .models import *


def example_data():
    c = Country(name="Polska")
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
        example_data()

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
        self.assertEquals(com.valid(), 186)
        self.assertEquals(com.given(), 236)


class ViewTests(TestCase):

    def setUp(self):
        example_data()

    def test_correct_search(self):
        response = self.client.get(reverse('main:search'), {'search': 'Gmina Testowa'})
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['results'], ['<Commune: Gmina Gmina Testowa>'])

    def test_no_arg_search(self):
        response = self.client.get(reverse('main:search'), follow=True)
        self.assertEquals(len(response.redirect_chain), 1)
        self.assertEquals(response.redirect_chain[0][0], reverse('main:index'))

    def test_failed_login(self):
        response = self.client.post(reverse('main:login'), {'username': 'test-user', 'password': 'asdasd'}, follow=True)
        self.assertEquals(len(response.redirect_chain), 0)
        self.assertEquals(response.context['username'], 'test-user')
        self.assertEquals(response.context['request'].user.is_authenticated(), False)

    def test_non_existent_district(self):
        response = self.client.get(reverse('main:district', kwargs={'pk': 9999}))
        self.assertEquals(response.status_code, 404)


class SeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        example_data()

        User.objects.create_superuser(username='admin1',
                                      password='qwerty12',
                                      email='')

        self.wd = webdriver.Firefox()

    def tearDown(self):
        self.wd.quit()

    def find_when_ready(self, target, phrase, plural=False):
        WebDriverWait(self.wd, 6) \
            .until(expected_conditions.presence_of_element_located((target, phrase)))
        if not plural:
            return self.wd.find_element(target, phrase)
        else:
            return self.wd.find_elements(target, phrase)

    def test_votes_change(self):

        # save self-contained test values
        com = Commune.objects.get(pk=7)
        com.walesa = 20
        com.full_clean()
        com.save()
        old_walesa = com.walesa
        designated_walesa = 10

        # open the site
        self.wd.get('%s%s' % (self.live_server_url, reverse('main:index')))

        # log in
        self.find_when_ready(By.LINK_TEXT, 'Zaloguj').click()
        self.find_when_ready(By.ID, 'username').send_keys('admin1')
        self.find_when_ready(By.ID, 'password').send_keys('qwerty12')
        self.find_when_ready(By.XPATH, '//input[@value="Zaloguj"]').click()

        # go to smallest area (commune)
        while self.wd.find_elements_by_id('children_section'):
            self.find_when_ready(By.CSS_SELECTOR, '#children_section a', True)[0].click()

        # check old data
        walesa_node = self.find_when_ready(By.XPATH, '//input[@name="walesa"]')
        self.assertEquals(walesa_node.get_attribute('value'), str(old_walesa))

        # insert new data
        walesa_node.clear()
        walesa_node.send_keys(str(designated_walesa))
        self.find_when_ready(By.XPATH, '//input[@value="Zapisz"]').click()

        # ensure the form is not polluted
        current_url = self.wd.current_url
        self.wd.get(current_url)

        # check new data
        new_walesa = self.find_when_ready(By.XPATH, '//input[@name="walesa"]').get_attribute('value')
        self.assertEquals(new_walesa, str(designated_walesa))
        com2 = Commune.objects.get(pk=7)
        self.assertEquals(com2.walesa, designated_walesa)
