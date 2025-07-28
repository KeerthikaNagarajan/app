# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

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

# --- Dashboard Chart ---
def display_skill_gap_chart(user):
    tsr = tsr_skills[user["role"]]
    skills = list(tsr.keys())
    expected = list(tsr.values())
    actual = [user["skills"].get(skill, 0) for skill in skills]

    fig, ax = plt.subplots()
    x = range(len(skills))
    ax.bar(x, expected, width=0.4, label="Expected", align='center')
    ax.bar([p + 0.4 for p in x], actual, width=0.4, label="Current", align='center')
    ax.set_xticks([p + 0.2 for p in x])
    ax.set_xticklabels(skills)
    ax.set_ylabel("Skill Level")
    ax.set_title("Skill Gap Overview")
    ax.legend()
    st.pyplot(fig)

# --- Quiz Simulator ---
def take_quiz(skill, user):
    st.subheader(f"📝 Quiz: {skill}")
    score = 0
    if skill == "Python":
        q1 = st.radio("What does 'def' do in Python?", ["Defines a function", "Defines a class", "Declares a variable"])
        if q1 == "Defines a function": score += 1
    elif skill == "SQL":
        q1 = st.radio("What does SELECT do?", ["Deletes data", "Selects data", "Updates data"])
        if q1 == "Selects data": score += 1
    elif skill == "Cloud":
        q1 = st.radio("Which is a cloud provider?", ["AWS", "HTML", "NumPy"])
        if q1 == "AWS": score += 1

    if st.button("Submit Quiz"):
        st.success(f"You scored {score}/1 on the {skill} quiz.")
        if score == 1:
            user['skills'][skill] += 1
            st.info(f"Skill level for {skill} updated to {user['skills'][skill]}")

# --- Real-Time Learning Module Simulation ---
def show_learning_module(skill):
    st.info(f"You're now in the {skill} Learning Module. Watch videos, complete practice, and take a quiz to advance.")
    st.video("https://www.youtube.com/watch?v=kqtD5dpn9C8")
    st.markdown("[📘 External Course: W3Schools Python](https://www.w3schools.com/python/)")
    st.success("Module Completed! This would update your progress in a real system.")

# --- Streamlit UI ---
st.sidebar.title("📚 Skill-Gap System")
user_names = [l["name"] for l in learners]
current_user_name = st.sidebar.selectbox("Login as Consultant:", user_names)
current_user = next(user for user in learners if user["name"] == current_user_name)

view = st.sidebar.radio("Select View:", ["Learner Dashboard", "Admin Console"])

if view == "Learner Dashboard":
    st.title("👩‍🏫 Learner Dashboard")
    user = current_user
    gaps = calculate_skill_gap(user)

    st.markdown(f"### 👤 Profile: {user['name']}")
    st.write(f"**Role:** {user['role']}")
    st.write("**Current Skills:**", user["skills"])

    st.markdown("### 📊 Skill Gap Chart")
    display_skill_gap_chart(user)

    st.markdown("### 🧠 Skill Gap")
    if gaps:
        st.table(pd.DataFrame(gaps.items(), columns=["Skill", "Gap"]))
    else:
        st.success("No skill gaps! You're aligned with TSR expectations.")

    st.markdown("### 🗏️ Learning Path Recommendations")
    for skill, gap in gaps.items():
        st.markdown(f"**{skill}** — Improve by {gap} level(s). Why it matters: _Critical for role expectations_.")
        st.progress(1 - (gap / tsr_skills[user["role"]][skill]))
        if st.button(f"Start {skill} Module"):
            show_learning_module(skill)
        with st.expander(f"Take {skill} Quiz"):
            take_quiz(skill, user)

elif view == "Admin Console":
    st.title("🛠️ Admin Console")
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
    st.download_button("📅 Download Report", df.to_csv(index=False).encode(), "report.csv")

    st.markdown("### ⚙️ Agent Status")
    st.markdown("""
    - **Profile Agent**: ✅ Active, latency 0.5s  
    - **Assessment Agent**: ✅ Completed, no errors  
    - **Recommender Agent**: ✅ Generated paths in real-time  
    - **Tracker Agent**: 🔄 Detecting plateaus
    """)
