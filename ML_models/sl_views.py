# Views for Supervised Learning

from django.shortcuts import HttpResponse, redirect, render, get_object_or_404
from .models import ML_algorithms, ML_model
from .helper import invoke_model
from django.contrib import messages
from celery.result import AsyncResult
from django.conf import settings
from .tasks import *
import pandas as pd
import pickle, os


def SL_upload_dataset(request, pk):
    algorithm = get_object_or_404(ML_algorithms, pk=pk)
    previous_models = ML_model.objects.filter(ml_algo=algorithm)
    if request.method == 'POST':
        if "title-form" in request.POST:
            obj = ML_model.objects.create(title=request.POST.get('title'), description=request.POST.get('description'), ml_algo=algorithm)
            obj.save()
            context = {"flag":"UPLOAD", "algorithm":algorithm, "obj":obj}
        elif "upload-form" in request.POST:
            obj = get_object_or_404(ML_model, pk=request.POST.get('obj'))
            if str(request.FILES.get('data_file')).split('.')[-1] == 'csv':
                obj.data_file = request.FILES.get('data_file')
                obj.save()
                dataset = pd.read_csv(obj.data_file)
                context = {"flag":"SELECT", "algorithm":algorithm, "data_columns":dataset.columns, "obj":obj}
            else:
                messages.warning(request, 'Currently, application only accepts CSV files.')
                context = {"flag":"UPLOAD", "algorithm":algorithm, "obj":obj}
        elif "training-form" in request.POST:
            obj = get_object_or_404(ML_model, pk=request.POST.get('obj'))
            obj.target = request.POST.get('target')
            obj.save()
            return redirect("sl-training", pk=obj.pk)
        return render(request, 'SL_upload_dataset.html', context)

    context = {"flag":"TITLE", "algorithm":algorithm, "previous_models":previous_models}
    return render(request, "SL_upload_dataset.html", context)

def SL_training(request, pk):
    model_obj = get_object_or_404(ML_model, pk=pk)
    if model_obj.p_file:
        return redirect("sl-prediction", pk=pk)
    else:
        model_info = invoke_model(model_obj)
        model_exception = AsyncResult(model_info.id)
        if model_exception.get() == None:
            messages.info(request, "Model training is in progress. You can confirm by going to your selected algorithm.")
            return redirect('index')
        else:
            messages.warning(request, "Model training has been interrupted. Your model information is saved.\nYou can edit and retrain your model by going to your selected algorithm.")
    context = {"model":model_obj, "error":model_exception.get()}
    return render(request, "SL_training.html", context)

def SL_prediction(request, pk):
    model_obj = get_object_or_404(ML_model, pk=pk)
    if model_obj.p_file and request.method == 'POST':
        if str(request.FILES.get('test_file')).split('.')[-1] == 'csv':
            test_file = pd.read_csv(request.FILES.get('test_file'))
            model = pickle.load(open(model_obj.p_file.path, "rb"))
            values = model.predict(test_file)
            output = pd.DataFrame(values)
            output.to_csv('prediction.csv')

            filename = 'prediction.csv'
            response = HttpResponse(open(filename, 'rb').read(),    content_type='text/csv')               
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = 'attachment; filename=%s' % 'prediction.csv'
            return response
        else:
            messages.warning(request, 'Currently, application only accepts CSV files.')
            context = {"model":model_obj}
    else:
        context = {"model":model_obj}
    return render(request, "SL_prediction.html", context)

def SL_edit_model(request, pk):
    model_obj = get_object_or_404(ML_model, pk=pk)
    if request.method == 'POST':
        if "title-form" in request.POST:
            model_obj.title = request.POST.get('title')
            model_obj.description = request.POST.get('description')
            model_obj.save()
            context = {"flag":"UPLOAD", "model_obj":model_obj, "algorithm":model_obj.ml_algo}
        elif "upload-form" in request.POST:
            if request.FILES:
                model_obj.data_file = request.FILES.get('data_file')
                model_obj.save()
                dataset = pd.read_csv(model_obj.data_file)
                context = {"flag":"SELECT", "model_obj":model_obj, "algorithm":model_obj.ml_algo, "data_columns":dataset.columns}
            else:
                dataset = pd.read_csv(model_obj.data_file)
                context = {"flag":"SELECT", "model_obj":model_obj, "algorithm":model_obj.ml_algo, "data_columns":dataset.columns}
        elif "training-form" in request.POST:
            model_obj.target = request.POST.get('target')
            model_obj.save()
            return redirect("sl-dataset", pk=model_obj.ml_algo.id)
        return render(request, 'SL_edit_model.html', context)
    context = {"flag":"TITLE", "model_obj":model_obj, "algorithm":model_obj.ml_algo}
    return render(request, "SL_edit_model.html", context)

def SL_delete_model(request, pk):
    model_obj = get_object_or_404(ML_model, pk=pk)
    model_obj.delete()
    messages.info(request, "Model deleted successfully!")
    return redirect("index")
