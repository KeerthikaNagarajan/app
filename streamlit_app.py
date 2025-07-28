# streamlit_app.py
import streamlit as st
import pandas as pd

# --- Synthetic Data ---
learners = [
    {"name": "Keerthika", "role": "Data Engineer", "skills": {"Python": 3, "SQL": 4, "Cloud": 2}},
    {"name": "Arjun", "role": "Data Analyst", "skills": {"Python": 2, "SQL": 5, "Cloud": 1}},
    {"name": "Priya", "role": "Data Engineer", "skills": {"Python": 4, "SQL": 3, "Cloud": 2}},
]

tsr_skills = {
    "Data Engineer": {"Python": 4, "SQL": 5, "Cloud": 4, "ETL": 3},
    "Data Analyst": {"Python": 3, "SQL": 5, "Visualization": 4}
}

# --- Utility ---
def calculate_skill_gap(user, tsr):
    gaps = {}
    for skill, expected in tsr.items():
        current = user["skills"].get(skill, 0)
        if current < expected:
            gaps[skill] = expected - current
    return gaps

# --- Sidebar ---
st.sidebar.title("Navigation")
view = st.sidebar.radio("Go to:", ["Learner Dashboard", "Admin Console"])

# --- Learner Dashboard ---
if view == "Learner Dashboard":
    st.title("📘 Learner Dashboard")
    selected = st.selectbox("Select your profile:", [l["name"] for l in learners])
    learner = next(l for l in learners if l["name"] == selected)
    gaps = calculate_skill_gap(learner, tsr_skills[learner["role"]])

    st.subheader("👤 Profile Summary")
    st.write(f"**Role:** {learner['role']}")
    st.write("**Current Skills:**", learner["skills"])

    st.subheader("📊 Skill Gap Analysis")
    if gaps:
        st.write("The following skills need improvement:")
        st.table(pd.DataFrame(gaps.items(), columns=["Skill", "Gap"]))
    else:
        st.success("You meet all expected skills for your role!")

    st.subheader("🧭 Learning Path")
    for skill, gap in gaps.items():
        st.markdown(f"**{skill}**: You need to improve by {gap} level(s).")
        st.progress(1 - gap / tsr_skills[learner["role"]][skill])
        st.button(f"Start {skill} Course")

# --- Admin Console ---
else:
    st.title("🛠️ Admin Console")
    st.subheader("📋 Learner Overview")
    data = []
    for learner in learners:
        gap = calculate_skill_gap(learner, tsr_skills[learner["role"]])
        progress = round((1 - len(gap)/len(tsr_skills[learner["role"]])) * 100)
        data.append({
            "Name": learner["name"],
            "Role": learner["role"],
            "Skill Gaps": ", ".join(gap.keys()) if gap else "None",
            "Progress": f"{progress}%",
            "Status": "Completed"
        })
    st.dataframe(pd.DataFrame(data))

    st.subheader("⚙️ Agent System Monitoring")
    st.markdown("""
    - **Profile Agent**: ✅ Active  
    - **Assessment Agent**: ✅ Completed quizzes  
    - **Recommender Agent**: ✅ Generated paths  
    - **Tracker Agent**: 🔄 Tracking in-progress learners
    """)

    st.subheader("📈 Reports")
    st.download_button("Download Learner Report", pd.DataFrame(data).to_csv().encode(), "learner_report.csv")
