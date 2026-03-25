import pandas as pd
import matplotlib.pyplot as plt

def create_score_distribution_chart(df):
    if df.empty or "Resume Score" not in df.columns:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["Resume Score"], bins=10, edgecolor="black")
    ax.set_title("Resume Score Distribution")
    ax.set_xlabel("Resume Score")
    ax.set_ylabel("Number of Candidates")
    plt.tight_layout()
    return fig

def create_prediction_chart(df):
    if df.empty or "ML Prediction" not in df.columns:
        return None

    prediction_counts = df["ML Prediction"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(
        prediction_counts.values,
        labels=prediction_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.set_title("ML Prediction Overview")
    plt.tight_layout()
    return fig

def create_top_skills_chart(df):
    if df.empty or "Skills Found" not in df.columns:
        return None

    all_skills = []

    for skills in df["Skills Found"]:
        if isinstance(skills, str) and skills != "No skills found":
            split_skills = [skill.strip() for skill in skills.split(",")]
            all_skills.extend(split_skills)

    if not all_skills:
        return None

    skills_series = pd.Series(all_skills).value_counts().head(10)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(skills_series.index, skills_series.values)
    ax.set_title("Top Skills Found")
    ax.set_xlabel("Skills")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig