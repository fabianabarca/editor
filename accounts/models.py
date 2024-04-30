from django.contrib.auth.models import User
from django.db import models


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos de Admin


class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos de Operator


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos de Manager


class Planner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos de Planner


class Regulator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos de Regulator


class Observer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos específicos de Observer
