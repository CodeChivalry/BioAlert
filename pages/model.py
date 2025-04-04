import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 📌 Step 1: Load Dataset
df = pd.read_csv("mefar_dataset.csv")  # Change filename if needed

# 📌 Step 2: Balance the Data (3000 rows for class 1, 3000 rows for class 0)
class_1_data = df[df['class'] == 1].sample(n=3000, random_state=42)
class_0_data = df[df['class'] == 0].sample(n=3000, random_state=42)

# Combine and shuffle
balanced_df = pd.concat([class_1_data, class_0_data]).sample(frac=1, random_state=42).reset_index(drop=True)

# Save the balanced dataset (optional)
balanced_df.to_csv("balanced_mefar_dataset.csv", index=False)
balanced_df.columns = balanced_df.columns.str.strip()  # Remove extra spaces from column names
X = balanced_df.drop(columns=['class'])  
y = balanced_df['class']
# 📌 Step 4: Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 📌 Step 5: Normalize Features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 📌 Step 6: Train a Random Forest Model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📌 Step 7: Make Predictions
y_pred = model.predict(X_test)

# 📌 Step 8: Evaluate Performance
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.4f}")
print("\n📌 Classification Report:\n", classification_report(y_test, y_pred))

# 📌 Step 9: Save the Model & Scaler for Future Use
joblib.dump(model, "stress_model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("✅ Model and scaler saved successfully!")
