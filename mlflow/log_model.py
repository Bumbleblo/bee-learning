import mlflow.pyfunc
import mlflow
from mlflow.sklearn import log_model, save_model
from sklearn.svm import LinearSVC


model = LinearSVC()

path = 'linear_svc'

log_model(model, artifact_path=path)
