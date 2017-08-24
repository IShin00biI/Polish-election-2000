from django.forms import ModelForm

from main.models import Commune
from main.dictionaries import *


class CommuneForm(ModelForm):
    class Meta:
        model = Commune
        fields = candidates + static_stats
