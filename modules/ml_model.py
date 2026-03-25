import numpy as np
from sklearn.linear_model import LogisticRegression

def train_shortlist_model():
    X = np.array([
        [2, 1, 25],
        [3, 1, 30],
        [4, 2, 50],
        [5, 2, 55],
        [6, 3, 65],
        [7, 4, 80],
        [8, 5, 90],
        [1, 0, 10],
        [2, 0, 15],
        [3, 1, 35],
        [5, 3, 70],
        [6, 4, 85]
    ])

    y = np.array([
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1
    ])

    model = LogisticRegression()
    model.fit(X, y)
    return model

def predict_candidate_status(model, skills, matched, score):
    total_skills = len(skills)
    matched_skills = len(matched)

    features = np.array([[total_skills, matched_skills, score]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    status = "Shortlisted" if prediction == 1 else "Not Shortlisted"
    return status, float(probability)
