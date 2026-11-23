import pandas as pd
from sklearn.model_selection import train_test_split

# load dataset
df = pd.read_csv("data/raw/student_dropout_risk_2026.csv")

# drop person_id column and separate input and output variables
X = df.drop(columns=["person_id", "dropout"])
y = df["dropout"]

# stratified train-test split to preserve 68/32 dropout ratio
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.20, random_state=8, stratify=y
)

# split the remaining 80% to 80/20 ratio for training and validation set
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.20, random_state=8, stratify=y_train_val
)

## encoding the string values
# family_level_income is an ordinal category
# i just mapped it manually since LabelEncoder sorts alphabetically (High=0,Low=1,Middle=2), scrambling the order
income_map = {'Low': 0, 'Middle': 1, 'High': 2}
X_train['family_income_level'] = X_train['family_income_level'].map(income_map)
X_val['family_income_level'] = X_val['family_income_level'].map(income_map)
X_test['family_income_level'] = X_test['family_income_level'].map(income_map)

# one-hot encode nominal string features (since get_dummies is stateless, need to use reindex to reuse the category schema of train set)
nominal_cols = ["gender", "nationality", "course_type", "study_mode"]
X_train_encoded = pd.get_dummies(X_train, columns=nominal_cols, dtype=int)
X_val_encoded = pd.get_dummies(X_val, columns=nominal_cols, dtype=int).reindex(columns=X_train_encoded.columns, fill_value=0)
X_test_encoded = pd.get_dummies(X_test, columns=nominal_cols, dtype=int).reindex(columns=X_train_encoded.columns, fill_value=0)

# save as processed dataset csv file
# X_train_encoded.to_csv("data/processed/X_train_encoded.csv", index=False)
# y_train.to_csv("data/processed/y_train.csv", index=False)

# X_val_encoded.to_csv("data/processed/X_val_encoded.csv", index=False)
# y_val.to_csv("data/processed/y_val.csv", index=False)

# X_test_encoded.to_csv("data/processed/X_test_encoded.csv", index=False)
# y_test.to_csv("data/processed/y_test.csv", index=False)