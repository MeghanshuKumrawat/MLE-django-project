from celery import shared_task
from .models import ML_model
from django.shortcuts import get_object_or_404
import pickle
import pandas as pd


# helper function
def model_dump(model_obj, model):
    pickle.dump(model, open('models/user_created_models/'+str(model_obj.id)+'.sav','wb'))
    model_obj.p_file = 'user_created_models/'+str(model_obj.id)+'.sav'
    model_obj.save()
    

@shared_task()
def LinearRegression_task(pk):
    try:
        from sklearn.linear_model import LinearRegression

        model_obj = get_object_or_404(ML_model, pk=pk)
        df = pd.read_csv(model_obj.data_file)
        x_train = df.drop(columns = model_obj.target)
        y_train = df[model_obj.target]
        print(model_obj, '------------------------shared task start')
        model = LinearRegression()
        model.fit(x_train, y_train)
        model_dump(model_obj, model)
        print(model_obj, '------------------------shared task end')
    except Exception as e:
        return str(e)

@shared_task()
def LogisticRegression_task(pk):
    try:
        from sklearn.linear_model import LogisticRegression

        model_obj = get_object_or_404(ML_model, pk=pk)
        df = pd.read_csv(model_obj.data_file)
        x_train = df.drop(columns = model_obj.target)
        y_train = df[model_obj.target]
        print(model_obj, '------------------------shared task start')
        model = LogisticRegression()
        model.fit(x_train, y_train)
        model_dump(model_obj, model)
        print(model_obj, '------------------------shared task end')
    except Exception as e:
        return str(e)

@shared_task()
def GaussianNB_task(pk):
    try:
        from sklearn.naive_bayes import GaussianNB

        model_obj = get_object_or_404(ML_model, pk=pk)
        df = pd.read_csv(model_obj.data_file)
        x_train = df.drop(columns = model_obj.target)
        y_train = df[model_obj.target]
        print(model_obj, '------------------------shared task start')
        model = GaussianNB()
        model.fit(x_train, y_train)
        model_dump(model_obj, model)
        print(model_obj, '------------------------shared task end')
    except Exception as e:
        return str(e)

@shared_task()
def MultinomialNB_task(pk):
    try:
        from sklearn.naive_bayes import MultinomialNB

        model_obj = get_object_or_404(ML_model, pk=pk)
        df = pd.read_csv(model_obj.data_file)
        x_train = df.drop(columns = model_obj.target)
        y_train = df[model_obj.target]
        print(model_obj, '------------------------shared task start')
        model = MultinomialNB()
        model.fit(x_train, y_train)
        model_dump(model_obj, model)
        print(model_obj, '------------------------shared task end')
    except Exception as e:
        return str(e)

@shared_task()
def XgBoost_task(pk):
    try:
        from xgboost import XGBRegressor

        model_obj = get_object_or_404(ML_model, pk=pk)
        df = pd.read_csv(model_obj.data_file)
        x_train = df.drop(columns = model_obj.target)
        y_train = df[model_obj.target]
        print(model_obj, '------------------------shared task start')
        model = XGBRegressor(learning_rate = .01, n_estimators = 400)
        model.fit(x_train, y_train)
        model_dump(model_obj, model)
        print(model_obj, '------------------------shared task end')
    except Exception as e:
        return str(e)

@shared_task()
def SVC_task(pk):
    try:
        from sklearn.svm import SVC

        model_obj = get_object_or_404(ML_model, pk=pk)
        df = pd.read_csv(model_obj.data_file)
        x_train = df.drop(columns = model_obj.target)
        y_train = df[model_obj.target]
        print(model_obj, '------------------------shared task start')
        model = SVC()
        model.fit(x_train, y_train)
        model_dump(model_obj, model)
        print(model_obj, '------------------------shared task end')
    except Exception as e:
        return str(e)
