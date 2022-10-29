from pyexpat import model
from django.db import models
from sqlalchemy import null
from traitlets import default

algo_types = (("SL", "Supervised"), ("UL", "Unsupervised"), ("RL", "Reinforcement"))

class ML_algorithms(models.Model):
    """ for storing available models"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    algo_type = models.CharField(max_length=2,choices=algo_types)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.algo_type +" - "+ self.name

class ML_model(models.Model):
    """ for models created by user """
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ml_algo = models.ForeignKey(ML_algorithms, on_delete=models.CASCADE)
    data_file = models.FileField(upload_to='models_data', blank=True, null=True)
    target = models.CharField(max_length=200, blank=True, null=True)
    p_file = models.FileField(upload_to='user_created_models', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title +" - "+ self.ml_algo.name
