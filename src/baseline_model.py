import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from matplotlib import pyplot

#Training data
X_train = pd.read_csv("data/processed/X_train_encoded.csv")
y_train = pd.read_csv("data/processed/y_train.csv").squeeze("columns")

#Validation data
X_val = pd.read_csv("data/processed/X_val_encoded.csv")
y_val = pd.read_csv("data/processed/y_val.csv").squeeze("columns")

print("Training features:", X_train.shape)
print("Training labels:", y_train.shape)

print("Validation features:", X_val.shape)
print("Validation labels:", y_val.shape)

print("\nTraining Class Distribution:")
print(y_train.value_counts())

print("\nValidation Class Distribution:")
print(y_val.value_counts())

#Class percentages
print("\nTraining Class Percentage:")
print(y_train.value_counts(normalize=True) * 100)

print("\nValidation Class Percentage:")
print(y_val.value_counts(normalize=True) * 100)


#Baseline XGBoost model
model = XGBClassifier(
    eval_metric=["error", "logloss"],
    early_stopping_rounds=10
)

eval_set = [
    (X_train, y_train),
    (X_val, y_val)
]

#Train baseline XGBoost model
model.fit(
    X_train,
    y_train,
    eval_set=eval_set,
    verbose=True
)

#Predictions using validation data
predictions = model.predict(X_val)

#Evaluate predictions
accuracy = accuracy_score(y_val, predictions)

print("\nBaseline XGBoost Results")
print("Accuracy: %.2f%%" % (accuracy * 100.0))
print("Best Iteration:", model.best_iteration)
print("Best Validation Log Loss:", model.best_score)

results = model.evals_result()
epochs = len(results["validation_0"]["error"])
x_axis = range(0, epochs)

#Plot log loss
fig, ax = pyplot.subplots()

ax.plot(
    x_axis,
    results["validation_0"]["logloss"],
    label="Train"
)

ax.plot(
    x_axis,
    results["validation_1"]["logloss"],
    label="Validation"
)

ax.legend()

pyplot.xlabel("Boosting Iteration")
pyplot.ylabel("Log Loss")
pyplot.title("XGBoost Log Loss")

pyplot.savefig("performances/xgboost_logloss.png")
pyplot.show()

#Plot classification error
fig, ax = pyplot.subplots()

ax.plot(
    x_axis,
    results["validation_0"]["error"],
    label="Train"
)

ax.plot(
    x_axis,
    results["validation_1"]["error"],
    label="Validation"
)

ax.legend()

pyplot.xlabel("Boosting Iteration")
pyplot.ylabel("Classification Error")
pyplot.title("XGBoost Classification Error")

pyplot.savefig("performances/xgboost_error.png")
pyplot.show()

#Save model to file
joblib.dump(model, "models/xgboost_baseline.joblib")

print("\nSaved model to: models/xgboost_baseline.joblib")

#Load model from file
loaded_model = joblib.load("models/xgboost_baseline.joblib")

print("Loaded model from: models/xgboost_baseline.joblib")


loaded_predictions = loaded_model.predict(X_val)

#Evaluate 
loaded_accuracy = accuracy_score(y_val, loaded_predictions)

print("Loaded Model Accuracy: %.2f%%" % (loaded_accuracy * 100.0))

#Verify predictions
assert (predictions == loaded_predictions).all()

print("Model serialization verification successful!")

#Additional for saving history
history = pd.DataFrame({
    "iteration": x_axis,
    "training_error": results["validation_0"]["error"],
    "validation_error": results["validation_1"]["error"],
    "training_logloss": results["validation_0"]["logloss"],
    "validation_logloss": results["validation_1"]["logloss"]
})

history.to_csv(
    "performances/xgboost_training_history.csv",
    index=False
)

print("Training history saved successfully!")

summary = pd.DataFrame({
    "model": ["Baseline XGBoost"],
    "training_records": [len(X_train)],
    "validation_records": [len(X_val)],
    "number_of_features": [X_train.shape[1]],
    "validation_accuracy": [accuracy],
    "best_validation_logloss": [model.best_score],
    "best_iteration": [model.best_iteration],
    "stopping_iteration": [epochs - 1],
    "early_stopping_rounds": [10],
    "loaded_model_accuracy": [loaded_accuracy]
})

summary.to_csv(
    "performances/xgboost_baseline_results.csv",
    index=False
)

print("Baseline results saved successfully!")