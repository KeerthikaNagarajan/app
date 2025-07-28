# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- TSR Skills Matrix ---
tsr_skills = {
    "Data Engineer": {"Python": 4, "SQL": 5, "Cloud": 4, "ETL": 3},
    "Data Analyst": {"Python": 3, "SQL": 5, "Visualization": 4},
    "ML Engineer": {"Python": 5, "ML": 4, "Deep Learning": 3}
}

# --- Learners Data ---
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

# --- Skill Gap Logic ---
def calculate_skill_gap(user):
    tsr = tsr_skills[user["role"]]
    return {s: tsr[s] - user["skills"].get(s, 0) for s in tsr if user["skills"].get(s, 0) < tsr[s]}

# --- Quiz Generator ---
def take_quiz(skill, user):
    st.subheader(f"📝 {skill} Quiz")
    score = 0

    questions = {
        "Python": [
            ("What does 'def' do in Python?", "Defines a function", ["Defines a class", "Declares a variable"]),
            ("What is a list comprehension?", "Short syntax to create list", ["Loop", "Function"]),
        ],
        "SQL": [
            ("What does SELECT do?", "Selects data", ["Deletes data", "Updates data"]),
            ("What is a JOIN in SQL?", "Combines rows", ["Splits rows", "Deletes rows"]),
        ],
        "Cloud": [
            ("Which is a cloud provider?", "AWS", ["HTML", "NumPy"]),
            ("What does IaaS stand for?", "Infrastructure as a Service", ["Interface as a Service", "Internet as Software"]),
        ],
        "ETL": [
            ("What does ETL stand for?", "Extract Transform Load", ["Extract Transfer Load", "Embed Transform Learn"]),
            ("Which step loads data to the destination?", "Load", ["Extract", "Transform"]),
        ],
        "ML": [
            ("What is supervised learning?", "Learning with labeled data", ["Learning without data", "Unlabeled clustering"]),
            ("Which library is used in ML?", "scikit-learn", ["Pandas", "BeautifulSoup"]),
        ],
        "Deep Learning": [
            ("What is a neural network?", "Model inspired by human brain", ["SQL operation", "Cloud service"]),
            ("Which library is used for deep learning?", "TensorFlow", ["NumPy", "Matplotlib"]),
        ],
        "Visualization": [
            ("Which tool is used for dashboards?", "Power BI", ["Pandas", "TensorFlow"]),
            ("Which chart shows data parts of a whole?", "Pie chart", ["Line chart", "Scatter plot"]),
        ]
    }

    for i, (q, correct, wrongs) in enumerate(questions.get(skill, [])):
        options = [correct] + wrongs
        answer = st.radio(f"Q{i+1}: {q}", options, key=f"{skill}_q{i}")
        if answer == correct: score += 1

    if st.button("✅ Submit Quiz", key=f"{skill}_submit_{user['name']}"):
        st.success(f"You scored {score}/{len(questions[skill])}")
        if score >= 1:
            user["skills"][skill] += 1
            st.info(f"Your {skill} level is now {user['skills'][skill]}")

# --- Learning Modules ---
def show_learning_module(skill):
    st.info(f"🎯 Complete {skill} module below")
    resources = {
        "Python": [
            "https://www.youtube.com/watch?v=kqtD5dpn9C8",
            "https://www.w3schools.com/python/"
        ],
        "SQL": [
            "https://www.youtube.com/watch?v=HXV3zeQKqGY",
            "https://sqlbolt.com"
        ],
        "Cloud": [
            "https://www.youtube.com/watch?v=2LaAJq1lB1Q",
            "https://learn.microsoft.com/en-us/training/paths/az-900-describe-cloud-concepts/"
        ],
        "ETL": [
            "https://www.youtube.com/watch?v=0CnY3n3EHz4",
            "https://www.ibm.com/cloud/learn/etl"
        ],
        "ML": [
            "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
            "https://developers.google.com/machine-learning/crash-course"
        ],
        "Deep Learning": [
            "https://www.youtube.com/watch?v=aircAruvnKk",
            "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr"
        ],
        "Visualization": [
            "https://www.youtube.com/watch?v=RLVb4Uchj_g",
            "https://learn.microsoft.com/en-us/training/modules/introduction-power-bi/"
        ]
    }

    for link in resources.get(skill, []):
        if "youtube" in link:
            st.video(link)
        else:
            st.markdown(f"[🔗 {link}]({link})")
    st.success("✅ Module completed! Continue to quiz or next skill.")

# --- App Config ---
st.set_page_config(layout="wide", page_title="Skill Gap Analyzer", page_icon="📘")
st.markdown("<h1 style='color:#6C63FF;'>🎓 Personalized Skill-Gap Analyzer</h1>", unsafe_allow_html=True)

# --- Sidebar Login + Role View Toggle ---
st.sidebar.header("🔐 Login")
user_names = [u["name"] for u in learners]
selected_name = st.sidebar.selectbox("Select Consultant:", user_names)
current_user = next(l for l in learners if l["name"] == selected_name)
view_mode = st.sidebar.radio("Mode:", ["Learner Dashboard", "Admin Console"])

# --- Learner Dashboard ---
if view_mode == "Learner Dashboard":
    st.markdown(f"### 👤 Welcome, **{current_user['name']}** ({current_user['role']})")

    gaps = calculate_skill_gap(current_user)
    st.subheader("📊 Current Skills")
    st.json(current_user["skills"])

    st.subheader("⚠️ Skill Gaps")
    if gaps:
        fig, ax = plt.subplots()
        ax.bar(gaps.keys(), gaps.values(), color="#FF6F61")
        ax.set_title("Skill Gap Levels")
        st.pyplot(fig)
    else:
        st.success("You're fully aligned with TSR expectations!")

    st.subheader("📚 Personalized Learning Modules")
    for skill in gaps:
        with st.expander(f"📘 Learn {skill}"):
            show_learning_module(skill)
        with st.expander(f"📝 Take Quiz for {skill}"):
            take_quiz(skill, current_user)

# --- Admin Console ---
elif view_mode == "Admin Console":
    st.subheader("🛠️ Admin Console: Team Skill Overview")
    role_filter = st.selectbox("Filter by Role", ["All"] + list(tsr_skills.keys()))

    report_rows = []
    for learner in learners:
        if role_filter != "All" and learner["role"] != role_filter:
            continue
        gaps = calculate_skill_gap(learner)
        total_skills = len(tsr_skills[learner["role"]])
        completed = total_skills - len(gaps)
        percent = int((completed / total_skills) * 100)
        report_rows.append({
            "Name": learner["name"],
            "Role": learner["role"],
            "Skill Gaps": ", ".join(gaps.keys()) if gaps else "None",
            "Progress": f"{percent}%"
        })

    df = pd.DataFrame(report_rows)
    st.dataframe(df)
    st.download_button("📥 Export CSV", df.to_csv(index=False).encode(), "learner_report.csv")

    st.markdown("### 🤖 AI Agent Status")
    st.markdown("- 👤 Profile Agent: ✅ Active\n- 📊 Assessment Agent: ✅ Working\n- 🧠 Recommender Agent: ✅ Online\n- 🛰️ Progress Tracker: ⏳ Updating...")

