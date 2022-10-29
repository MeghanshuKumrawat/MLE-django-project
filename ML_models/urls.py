from django.urls import path
from .views import index
from .sl_views import SL_upload_dataset, SL_training, SL_prediction, SL_edit_model, SL_delete_model

urlpatterns = [
    path('', index, name='index'),
    path('sl-dataset/<int:pk>/', SL_upload_dataset, name='sl-dataset'),
    path('sl-training/<int:pk>/', SL_training, name='sl-training'),
    path('sl-prediction/<int:pk>/', SL_prediction, name='sl-prediction'),
    path('sl-edit-dataset/<int:pk>/', SL_edit_model, name='sl-edit-dataset'),
    path('sl-delete-dataset/<int:pk>/', SL_delete_model, name='sl-delete-dataset'),
]
