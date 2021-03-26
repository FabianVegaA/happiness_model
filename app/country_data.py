from wtforms import (
    Form, 
    StringField, 
    FloatField,
    validators
)


class CountryData(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    economy = FloatField('Economy')
    family = FloatField('Family')
    health = FloatField('Health')
    freedom = FloatField('Freedom')
    trust = FloatField('Trust')
    generosity = FloatField('Generosity')
    dystopia = FloatField('Dystopia')