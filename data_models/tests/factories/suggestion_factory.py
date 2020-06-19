from random import randint

import factory
from data_models.models import Suggestion


def fake(provider):
    return factory.Faker(provider, locale="dk_DK")


def _random_choice(model, field):
    choices = model._meta._get_field(field).choices
    return choices[randint(0, len(choices) - 1)][0]


class SuggestionsFactory(factory.Factory):
    class Meta:
        model = Suggestion

    komfort_value = _random_choice(Suggestion, "komfort_value")
    category = _random_choice(Suggestion, "category")
    can_be_suggested = randint(0, 5) <= 4
    internal_note = " " if randint(0, 5) >= 4 else fake()
