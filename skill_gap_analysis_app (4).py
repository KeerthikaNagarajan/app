# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Page Theme Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f4f9ff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #003366;
    }
    .stButton > button {
        background-color: #004b8d;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stRadio > div > div {
        color: #003366;
    }
    .css-1cpxqw2 {
        color: #003366;
    }
    .stSelectbox, .stDataFrameContainer {
        background-color: white !important;
    }
    .css-1offfwp, .css-qrbaxs {
        background-color: #e6f0ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Synthetic TSR Skill Data ---
tsr_skills = {
    "Data Engineer": {"Python": 4, "SQL": 5, "Cloud": 4, "ETL": 3},
    "Data Analyst": {"Python": 3, "SQL": 5, "Visualization": 4},
    "ML Engineer": {"Python": 5, "ML": 4, "Deep Learning": 3}
}

# --- Synthetic Learner Profiles ---
learners = [
    {"name": "Keerthika", "role": "Data Engineer", "skills": {"Python": 3, "SQL": 4, "Cloud": 2, "ETL": 1}},
    {"name": "Arjun", "role": "Data Analyst", "skills": {"Python": 2, "SQL": 5, "Visualization": 2}},
    {"name": "Priya", "role": "Data Engineer", "skills": {"Python": 4, "SQL": 3, "Cloud": 3, "ETL": 2}},
    {"name": "Rahul", "role": "ML Engineer", "skills": {"Python": 4, "ML": 3, "Deep Learning": 1}},
    {"name": "Sneha", "role": "Data Analyst", "skills": {"Python": 3, "SQL": 4, "Visualization": 3}},
    {"name": "Vikram", "role": "ML Engineer", "skills": {"Python": 5, "ML": 4, "Deep Learning": 2}},
    {"name": "Riya", "role": "Data Engineer", "skills": {"Python": 2, "SQL": 3, "Cloud": 1, "ETL": 1}},
    {"name": "Karan", "role": "ML Engineer", "skills": {"Python": 3, "ML": 2, "Deep Learning": 1}}
]

# --- Skill Gap Calculator ---
def calculate_skill_gap(user):
    tsr = tsr_skills[user["role"]]
    gaps = {}
    for skill, expected in tsr.items():
        current = user["skills"].get(skill, 0)
        if current < expected:
            gaps[skill] = expected - current
    return gaps

# --- Quiz Simulator ---
def take_quiz(skill, user):
    st.subheader(f"📝 Quiz: {skill}")
    score = 0
    if skill == "Python":
        q1 = st.radio("What does 'def' do in Python?", ["Defines a function", "Defines a class", "Declares a variable"])
        if q1 == "Defines a function": score += 1
        q2 = st.radio("What is a list comprehension?", ["Loop", "Function", "Short syntax to create list"])
        if q2 == "Short syntax to create list": score += 1
    elif skill == "SQL":
        q1 = st.radio("What does SELECT do?", ["Deletes data", "Selects data", "Updates data"])
        if q1 == "Selects data": score += 1
        q2 = st.radio("What is a JOIN in SQL?", ["Combines rows", "Splits rows", "Deletes rows"])
        if q2 == "Combines rows": score += 1
    elif skill == "Cloud":
        q1 = st.radio("Which is a cloud provider?", ["AWS", "HTML", "NumPy"])
        if q1 == "AWS": score += 1
        q2 = st.radio("What does IaaS stand for?", ["Infrastructure as a Service", "Interface as a Service", "Internet as a Software"])
        if q2 == "Infrastructure as a Service": score += 1

    if st.button("Submit Quiz", key=f"submit_{skill}_{user['name']}"):
        st.success(f"You scored {score}/2 on the {skill} quiz.")
        if score >= 1:
            user['skills'][skill] += 1
            st.info(f"Skill level for {skill} updated to {user['skills'][skill]}")

# --- Real-Time Learning Module Simulation ---
def show_learning_module(skill):
    st.info(f"📘 You're now in the {skill} Learning Module. Complete these to upgrade.")
    videos = {
        "Python": "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "SQL": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        "Cloud": "https://www.youtube.com/watch?v=2LaAJq1lB1Q",
        "ETL": "https://www.youtube.com/watch?v=0CnY3n3EHz4",
        "ML": "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
        "Visualization": "https://www.youtube.com/watch?v=RLVb4Uchj_g",
        "Deep Learning": "https://www.youtube.com/watch?v=aircAruvnKk"
    }

    links = {
        "Python": "https://www.w3schools.com/python/",
        "SQL": "https://sqlbolt.com",
        "Cloud": "https://learn.microsoft.com/en-us/training/paths/az-900-describe-cloud-concepts/",
        "ETL": "https://www.ibm.com/cloud/learn/etl",
        "ML": "https://developers.google.com/machine-learning/crash-course",
        "Visualization": "https://learn.microsoft.com/en-us/training/modules/introduction-power-bi/",
        "Deep Learning": "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr"
    }

    st.video(videos[skill])
    st.markdown(f"[🔗 Learn more about {skill}]({links[skill]})")
    st.success("✅ Module Completed! Progress would be tracked.")

# --- Streamlit UI ---
st.set_page_config(layout="wide", page_title="Skill-Gap Analyzer", page_icon="📊")
st.title("📊 Skill-Gap Analyzer")

col1, col2 = st.columns([1, 3])
with col1:
    st.header("🔐 Login Panel")
    user_names = [l["name"] for l in learners]
    current_user_name = st.selectbox("Login as Consultant:", user_names)
    current_user = next(user for user in learners if user["name"] == current_user_name)
    view = st.radio("Select View:", ["Learner Dashboard", "Admin Console"])

if view == "Learner Dashboard":
    user = current_user
    gaps = calculate_skill_gap(user)

    col2.header("👩‍🎓 Learner Dashboard")
    col2.markdown(f"### 👤 Profile: {user['name']}")
    col2.write(f"**Role:** {user['role']}")
    col2.write("**Current Skills:**", user["skills"])

    col2.markdown("### 📉 Skill Gap")
    if gaps:
        fig, ax = plt.subplots()
        ax.bar(gaps.keys(), gaps.values(), color='tomato')
        ax.set_title("Skill Gap Levels", fontsize=14)
        ax.set_ylabel("Gap Level")
        ax.set_xlabel("Skills")
        col2.pyplot(fig)
    else:
        col2.success("No skill gaps! You're aligned with TSR expectations.")

    col2.markdown("### 🗺️ Personalized Learning Path")
    for skill, gap in gaps.items():
        col2.markdown(f"**{skill}** — Improve by {gap} level(s). Why it matters: _Critical for your role_.")
        col2.progress(1 - (gap / tsr_skills[user["role"]][skill]))
        if col2.button(f"📘 Start {skill} Module", key=f"start_{skill}_{user['name']}"):
            show_learning_module(skill)
        with col2.expander(f"📝 Take {skill} Quiz"):
            take_quiz(skill, user)

elif view == "Admin Console":
    st.subheader("🛠️ Admin Console")
    role_filter = st.selectbox("Filter by Role:", ["All"] + list(tsr_skills.keys()))
    st.markdown("### 📋 Learner Report Table")
    rows = []
    for user in learners:
        if role_filter != "All" and user["role"] != role_filter:
            continue
        gaps = calculate_skill_gap(user)
        percent = round((1 - len(gaps) / len(tsr_skills[user["role"]])) * 100)
        rows.append({
            "Name": user["name"],
            "Role": user["role"],
            "Skill Gaps": ", ".join(gaps.keys()) if gaps else "None",
            "Progress": f"{percent}%"
        })
    df = pd.DataFrame(rows)
    st.dataframe(df)
    st.download_button("📥 Download Report", df.to_csv(index=False).encode(), "report.csv")

    st.markdown("### ⚙️ Agent Status")
    st.markdown("""
    - 🤖 **Profile Agent**: ✅ Active  
    - 🧠 **Assessment Agent**: ✅ Functional  
    - 🧭 **Recommender Agent**: ✅ Live  
    - 📈 **Tracker Agent**: ⏳ Monitoring
    """)

