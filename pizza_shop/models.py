from django import db
from django.db import models, transaction

# demo static choices vs datamodel relationships

FOOD_TYPES=(
    ('any', 'Any'),   # not a meat or veg, but can be used on either veggie or meat lovers
    ('meat', 'Meat'),
    ('veg', 'Vegetable')
)

class ToppingType(models.Model):
    """ Allow types to be re-ordered by users, and most importantly, the
        compatibility is dete=rmined here.
    """
    name = models.CharField(unique=True, max_length=40)
    homogenous = models.BooleanField(default=True)
    rank = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def is_compatible(self, pizza):
        if self.homogenous:
            return self.id == pizza.pizza_type_id
        return True


class Topping(models.Model):
    name = models.CharField(unique=True, max_length=40)
    type = models.CharField(choices=FOOD_TYPES, default=FOOD_TYPES[0][0], max_length=40)
    topping_type = models.ForeignKey(ToppingType)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(unique=True, max_length=40)
    toppings = models.ManyToManyField(Topping, blank=True)

    # two ways to type the pizza: choices or foreign key
    type = models.CharField(choices=FOOD_TYPES, default=FOOD_TYPES[0][0], max_length=40)
    pizza_type = models.ForeignKey(ToppingType)

    def __str__(self):
        return self.name

    def valid_toppings(self):
        # validate choices
        for topping in self.toppings.all():
            if self.type in ('meat', 'veg'):
                # then all topping must either match, or be 'any'
                if topping.type != self.type or topping.type != 'mixed':
                    raise db.IntegrityError(
                        "cannot put {t} on {p} pizza".format(
                            t=topping, p=self.type
                        ))

        # validate relations
        for topping in self.toppings.all():
            if not topping.is_compatible(self):
                raise db.IntegrityError("cannot put {t} on {p} pizza".format(
                    t=topping, p=self.type
                ))


