import streamlit as st
from extract import extract_text_from_pdf, extract_text_from_docx
from skills import extract_skills
from score import calculate_resume_score
from contact import extract_email, extract_phone
from auth import check_login, signup_user
from database import create_users_table, get_all_users
from analytics import create_candidate_dataframe, calculate_score_statistics, get_top_candidates
from ml_model import train_shortlist_model, predict_candidate_status
from dashboard import create_score_distribution_chart, create_prediction_chart, create_top_skills_chart


st.set_page_config(page_title="Resume Screening System", layout="wide")


def initialize_app():
    create_users_table()
    return train_shortlist_model()

def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = ""


create_users_table()
shortlist_model = train_shortlist_model()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = None

def admin_login():
    st.subheader("Admin Login")

    username = st.text_input("Admin Username")
    password = st.text_input("Password", type="password")

    if st.button("Login as Admin"):
        success, role = check_login(username, password)

        if success and role == "admin":
            st.session_state.logged_in = True
            st.session_state.role = "admin"
            st.success("Admin Login Successful")
            st.rerun()
        else:
            st.error("Invalid Admin Credentials")

def user_login():
    st.subheader("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login as User"):
        success, role = check_login(username, password)

        if success and role == "user":
            st.session_state.logged_in = True
            st.session_state.role = "user"
            st.session_state.current_user = username
            st.success("User Login Successful")
            st.rerun()
        else:
            st.error("Invalid User Credentials")


def signup_page():
    st.subheader("Signup")

    username = st.text_input("Create Username", key="signup_user")
    password = st.text_input("Create Password", type="password", key="signup_pass")

    if st.button("Signup"):
        success, message = signup_user(username, password)
        if success:
            st.success(message)
        else:
            st.error(message)


def extract_resume_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        return uploaded_file.read().decode("utf-8")

def process_uploaded_resumes(uploaded_files, required_skills, model):
    candidate_data = []

    for uploaded_file in uploaded_files:
        resume_text = extract_resume_text(uploaded_file)

        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text)
        score, matched = calculate_resume_score(skills, required_skills)
        prediction, probability = predict_candidate_status(model, skills, matched, score)

        candidate_record = {
            "File Name": uploaded_file.name,
            "Email": email,
            "Phone": phone,
            "Skills Found": ", ".join(skills) if skills else "No skills found",
            "Resume Score": round(score, 2),
            "Matched Skills": ", ".join(matched) if matched else "No matched skills",
            "ML Prediction": prediction,
            "Prediction Confidence": round(probability * 100, 2)
        }

        candidate_data.append(candidate_record)

    return candidate_data

def display_summary_and_dashboard(candidate_data):
    df = create_candidate_dataframe(candidate_data)

    st.subheader("Candidate Results Table")
    st.dataframe(df, use_container_width=True)

    stats = calculate_score_statistics(df)

    st.subheader("Score Summary")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average Score", round(stats["average_score"], 2))

    with col2:
        st.metric("Highest Score", round(stats["highest_score"], 2))

    with col3:
        st.metric("Lowest Score", round(stats["lowest_score"], 2))

    with col4:
        st.metric("Total Candidates", stats["total_candidates"])

    st.subheader("Top Candidates")
    top_df = get_top_candidates(df, top_n=3)
    st.dataframe(top_df, use_container_width=True)

    st.subheader("Dashboard")

    score_chart = create_score_distribution_chart(df)
    if score_chart:
        st.pyplot(score_chart)

    prediction_chart = create_prediction_chart(df)
    if prediction_chart:
        st.pyplot(prediction_chart)

    skills_chart = create_top_skills_chart(df)
    if skills_chart:
        st.pyplot(skills_chart)

def main_app(model):
    st.title("Resume Screening System")
    st.header("AI Powered Resume Screening")
    st.write(f"Welcome, {st.session_state.current_user}")

    st.sidebar.title("Navigation")

    option = st.sidebar.selectbox(
        "Select Option",
        ["Upload Resume", "Screen Candidates", "View Results"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.rerun()

    job_skills_input = st.text_input(
        "Enter Required Skills",
        "Python, SQL, Machine Learning, NLP"
    )

    required_skills = [skill.strip() for skill in job_skills_input.split(",") if skill.strip()]

    uploaded_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        candidate_data = process_uploaded_resumes(uploaded_files, required_skills, model)
        display_summary_and_dashboard(candidate_data)
    else:
        st.info("Please upload one or more resumes.")




def main_app():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.current_user = ""
        st.rerun()
    st.title("Resume Screening System")

    st.header("AI Powered Resume Screening")

    st.sidebar.title("Navigation")

    option = st.sidebar.selectbox(
        "Select Option",
        ["Upload Resume", "Screen Candidates", "View Results"]
    )

    job_skills_input = st.text_input(
        "Enter Required Skills",
        "Python, SQL, Machine Learning, NLP"
    )

    required_skills = [skill.strip() for skill in job_skills_input.split(",")]

    uploaded_files = st.file_uploader(
        "Upload Resumes",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
    candidate_data = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown("---")
            st.subheader(f"Processing Resume: {uploaded_file.name}")

            file_name = uploaded_file.name.lower()

            if file_name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            elif file_name.endswith(".docx"):
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                resume_text = uploaded_file.read().decode("utf-8")

            email = extract_email(resume_text)
            phone = extract_phone(resume_text)
            skills = extract_skills(resume_text)
            score, matched = calculate_resume_score(skills, required_skills)
            prediction, probability = predict_candidate_status(shortlist_model, skills, matched, score)

            candidate_record = {
                "File Name": uploaded_file.name,
                "Email": email,
                "Phone": phone,
                "Skills Found": ", ".join(skills) if skills else "No skills found",
                "Resume Score": score,
                "Matched Skills": ", ".join(matched) if matched else "No matched skills"
            }

            candidate_data.append(candidate_record)

            st.subheader("Candidate Details")
            st.write("Email:", email)
            st.write("Phone:", phone)

            st.subheader("Skills Found")
            if skills:
                for skill in skills:
                    st.write("-", skill)
            else:
                st.write("No matching skills found")

            st.subheader("Resume Match Score")
            st.write("Score:", f"{score:.2f}%")

            st.subheader("Matched Skills")
            if matched:
                for skill in matched:
                    st.write("-", skill)
            else:
                st.write("No matched skills found")


            st.subheader("Resume Match Score")
            st.write("Score:", round(score, 2), "%")

            st.subheader("Matched Skills")
            if matched:
                for skill in matched:
                    st.write("-", skill)
            else:
                st.write("No matched skills found")

            st.subheader("ML Prediction")
            st.write("Status:", prediction)
            st.write("Confidence:", round(probability * 100, 2), "%")

        st.markdown("---")
        st.subheader("Candidate Data Table")

        df = create_candidate_dataframe(candidate_data)
        st.dataframe(df, use_container_width=True)

        stats = calculate_score_statistics(df)

        st.subheader("Score Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Average Score", round(stats["average_score"], 2))

        with col2:
            st.metric("Highest Score", round(stats["highest_score"], 2))

        with col3:
            st.metric("Lowest Score", round(stats["lowest_score"], 2))

        with col4:
            st.metric("Total Candidates", stats["total_candidates"])

        st.subheader("Top Candidates")
        top_df = get_top_candidates(df, top_n=3)
        st.dataframe(top_df, use_container_width=True)


        st.markdown("---")
        st.subheader("Dashboard")

        score_chart = create_score_distribution_chart(df)
        if score_chart:
            st.pyplot(score_chart)

        prediction_chart = create_prediction_chart(df)
        if prediction_chart:
            st.pyplot(prediction_chart)

        skills_chart = create_top_skills_chart(df)
        if skills_chart:
            st.pyplot(skills_chart)
    st.markdown("---")
    st.write("Auto Resume Screening System made by Manthan Bhave")

menu = st.sidebar.radio("Select Option", ["Admin Login", "User Login", "Signup"])

if st.session_state.role == "admin":
    st.sidebar.subheader("Admin Panel")

    if st.sidebar.button("View All Users"):
        users = get_all_users()

        st.subheader("Registered Users")
        for user in users:
            st.write("-", user[0])

if not st.session_state.logged_in:
    if menu == "Admin Login":
        admin_login()
    elif menu == "User Login":
        user_login()
    else:
        signup_page()
else:
    main_app()