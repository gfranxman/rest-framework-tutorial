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
    homogenous = models.BooleanField(default=False)
    universal = models.BooleanField(default=True)  # proof the bools are bad,
                                                   # there's always a 3rd state
    rank = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    def is_compatible(self, topping):
        if self.homogenous:
            return self.id == topping.topping_type.id or topping.topping_type.universal
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
    pizza_type_char = models.CharField(choices=FOOD_TYPES, default=FOOD_TYPES[0][0], max_length=40)
    pizza_type = models.ForeignKey(ToppingType)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        self.valid_toppings()
        super(Pizza,self).save(*args, **kwargs)

    def valid_toppings(self):
        # validate choices
        # for topping in self.toppings.all():
        #     if self.pizza_type_char in ('meat', 'veg'):
        #         then all topping must either match, or be 'any'
        #       if topping.type != self.pizza_type_char or topping.type != 'mixed':
        #           raise db.IntegrityError(
        #               "cannot put {t} on {p} pizza".format(
        #                   t=topping, p=self.pizza_type_char
        #               ))

        # validate relations
        for topping in self.toppings.all():
            if not self.pizza_type.is_compatible(topping):
                raise db.IntegrityError("cannot put {t} on {p} pizza".format(
                    t=topping, p=self.pizza_type.name
                ))


