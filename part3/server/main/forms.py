from django.forms import ModelForm

from .models import Commune
from .dictionaries import *


class CommuneForm(ModelForm):
    class Meta:
        model = Commune
        fields = candidates
