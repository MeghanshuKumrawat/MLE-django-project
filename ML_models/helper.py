from .tasks import *

def invoke_model(model):
    try:
        if model.ml_algo.name == "Linear Regression":
            info = LinearRegression_task.delay(model.id)
            return info
        elif model.ml_algo.name == "Logistic Regression":
            info =LogisticRegression_task.delay(model.id)
            return info
        elif model.ml_algo.name == "Gaussian Naive Bayes":
            info = GaussianNB_task.delay(model.id)
            return info
        elif model.ml_algo.name == "Multinomial Naive Bayes":
            info = MultinomialNB_task.delay(model.id)
            return info
        elif model.ml_algo.name == "XGBoost":
            info = XgBoost_task.delay(model.id)
            return info
        elif model.ml_algo.name == "Support Vector Classifier":
            info = SVC_task.delay(model.id)
            return info

    except Exception as e:
        return e
