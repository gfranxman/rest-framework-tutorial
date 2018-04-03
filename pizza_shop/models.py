from django.db import models, transaction

# demo static choices vs datamodel relationships
from rest_framework.exceptions import ValidationError
from rest_framework.utils import model_meta

import logging


logger = logging.getLogger(__file__)

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
    type = models.CharField(choices=FOOD_TYPES, default=FOOD_TYPES[0][0],  max_length=40)
    topping_type = models.ForeignKey(ToppingType)

    def __str__(self):
        return self.name

class ValidatedModel(models.Model):
    class Meta:
        abstract = True

    def validate(self):
        self.full_clean()
        # this can only validate existing objects because field.all uses the db
        if hasattr(self, 'id') and self.id:
            for m2m_field in self._meta.many_to_many:
                attr = m2m_field.name
                field = getattr(self, attr)
                for val_func in m2m_field.validators:
                    # validate each item
                    for item in field.all():
                        if not val_func(self, item):
                            field.remove(item)
                            logger.warn("removing item")


    def save(self, *args, **kwargs):
        self.validate()

        return super(ValidatedModel, self).save(*args, **kwargs)


def toppings_are_compatible(pizza, field, data=None, raise_exception=False):
    """ verify the toppings are allowed for the pizza
        return False or raise exception on first invalid topping.
    """
    attr_name = field.name
    if data:
        toppings = data.get(attr_name, [])
    else:
        toppings = pizza.toppings.all()

    for topping in toppings:
        if not pizza.pizza_type.is_compatible(topping):
            if raise_exception:
                raise ValidationError("cannot put {t} on {p} pizza".format(
                    t=topping, p=pizza.pizza_type.name
                ))
            return False

    return True


def topping_is_compatible(pizza, topping, raise_exception=False):
    """ verify the topping are allowed for the pizza
        return False or raise exception on invalid topping.
    """
    if not pizza.pizza_type.is_compatible(topping):
        if raise_exception:
            raise ValidationError("cannot put {t} on {p} pizza".format(
                t=topping, p=pizza.pizza_type.name
            ))
        return False

    return True


class Pizza(ValidatedModel):
    name = models.CharField(unique=True, max_length=40)
    toppings = models.ManyToManyField(Topping, blank=True, validators=[topping_is_compatible,])  # , through='PizzaPizzaTopping')
    # toppings = models.ManyToManyField(Topping, blank=True) #, through='PizzaTopping')

    # two ways to type the pizza: choices or foreign key
    pizza_type_char = models.CharField(choices=FOOD_TYPES, default=FOOD_TYPES[0][0], max_length=40)
    pizza_type = models.ForeignKey(ToppingType)

    def __str__(self):
        return self.name

# attempts at replacing the related model manager fail because if we define
# the model, then the APIs change and you have to have a separate api
# for managin the relation ship.    If you tag the model as 'auto_created'
# to fool it, the mirgration framework will remove your table.
#
# class PizzaTopping(models.Model):
#     pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
#     topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
#
#     class Meta:
#         auto_created = True
#
#     def save(self, *args, **kwargs):
#         topping_is_compatible(self.pizza, self.topping)
#         return super(PizzaTopping, self).save(*args, **kwargs)
#



# attempts to subclass the related mgr somehow loose the meta data con the class
# def subclass_related_mgr(mgr):
#     class ValMgr( mgr.__class__):
#         def add(self, o):
#             return super(ValMgr, self).add(o)
#         def update(self, *args, **kwargs):
#             return super(ValMgr, self).update( *args, **kwargs)
#         def set(self, instance, values):
#             return super(ValMgr, self).set(instance, values)
#         pass
#     return ValMgr(mgr)
# Pizza.toppings.related_manager_cls = subclass_related_mgr(Pizza.toppings.related_manager_cls)
# Pizza.toppings = subclass_related_mgr(Pizza.toppings)

# def extend_instance(obj, cls):
#     """Apply mixins to a class instance after creation"""
#     base_cls = obj.__class__
#     base_cls_name = obj.__class__.__name__
#     obj.__class__ = type(base_cls_name, (cls, base_cls),{})


# original_add = Pizza.toppings.related_manager_cls.add
# ftype = type(original_add)
#
#def validated_add(mgr, *args):
#    global original_add
#
#    # validate before adding to mgr.instance
#    for a in args:
#        if not topping_is_compatible(mgr.instance, a):
#            raise ValueError("cant add {t} to {p}".format(t=a, p=mgr.instance))
#    return original_add(mgr, *args)


# Pizza.toppings.related_manager_cls.add = ftype(validated_add, Pizza.toppings.related_manager_cls, {})

# class PizzaPizzaTopping(models.Model):
#     pizza = models.ForeignKey(Pizza)
#     topping = models.ForeignKey(Topping)
#
#     class Meta:
#          db_table = 'pizza_shop_pizza_toppings'

