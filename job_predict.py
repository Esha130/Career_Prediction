# job_model_train.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Generate dummy data
np.random.seed(42)
df = pd.DataFrame({
    "age": np.random.randint(20, 35, 500),
    "gender": np.random.choice(["Male", "Female"], 500),
    "education_level": np.random.choice(["UG", "PG", "Diploma"], 500),
    "cgpa": np.round(np.random.uniform(5, 10, 500), 2),
    "experience_years": np.random.randint(0, 5, 500),
    "num_internships": np.random.randint(0, 4, 500),
    "communication_score": np.round(np.random.uniform(5, 10, 500), 1),
    "certifications": np.random.randint(0, 5, 500),
    "resume_score": np.random.randint(4, 10, 500),
    "github_projects": np.random.randint(0, 6, 500),
    "linkedin_score": np.round(np.random.uniform(4, 10, 500), 1),
    "job_offer": np.random.choice([0, 1], 500, p=[0.4, 0.6])
})

# Encode categorical data
le_gender = LabelEncoder()
le_edu = LabelEncoder()
df['gender'] = le_gender.fit_transform(df['gender'])
df['education_level'] = le_edu.fit_transform(df['education_level'])

# Split and train
X = df.drop("job_offer", axis=1)
y = df["job_offer"]

model = RandomForestClassifier()
model.fit(X, y)

# Save model & encoders
joblib.dump(model, "job_offer_model.pkl")
joblib.dump(le_gender, "gender_encoder.pkl")
joblib.dump(le_edu, "edu_encoder.pkl")
