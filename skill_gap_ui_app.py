# streamlit_app.py
import streamlit as st
import pandas as pd

# --- Synthetic TSR Skill Data ---
tsr_skills = {
    "Data Engineer": {"Python": 4, "SQL": 5, "Cloud": 4, "ETL": 3},
    "Data Analyst": {"Python": 3, "SQL": 5, "Visualization": 4}
}

# --- Synthetic Learner Profiles ---
learners = [
    {"name": "Keerthika", "role": "Data Engineer", "skills": {"Python": 3, "SQL": 4, "Cloud": 2, "ETL": 1}},
    {"name": "Arjun", "role": "Data Analyst", "skills": {"Python": 2, "SQL": 5, "Visualization": 2}},
    {"name": "Priya", "role": "Data Engineer", "skills": {"Python": 4, "SQL": 3, "Cloud": 3, "ETL": 2}},
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

# --- Progress Tracker ---
def get_progress_stage(user):
    gaps = calculate_skill_gap(user)
    if not gaps:
        return 5
    elif gaps:
        return 4
    return 2

# --- Streamlit Layout ---
st.set_page_config(layout="wide")
st.sidebar.title("🎯 Personalized Skill-Gap System")
view = st.sidebar.radio("Choose View:", ["Learner Dashboard", "Admin Console"])

if view == "Learner Dashboard":
    st.title("👨‍🎓 Learner Dashboard")
    learner_names = [l["name"] for l in learners]
    selected_name = st.selectbox("Select your name:", learner_names)
    user = next(l for l in learners if l["name"] == selected_name)
    gaps = calculate_skill_gap(user)
    progress_stage = get_progress_stage(user)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👤 Profile")
        st.write(f"**Name**: {user['name']}")
        st.write(f"**Role**: {user['role']}")
        st.write("**Skills:**")
        st.json(user["skills"])

    with col2:
        st.subheader("📈 Skill Gaps")
        if gaps:
            st.dataframe(pd.DataFrame(gaps.items(), columns=["Skill", "Gap"]))
        else:
            st.success("You have no skill gaps. Good job!")

    st.subheader("🛣️ Personalized Learning Path")
    if gaps:
        for skill, gap in gaps.items():
            st.info(f"📘 {skill}: You need to improve by {gap} level(s).")
            st.progress(1 - gap / tsr_skills[user["role"]][skill])
            st.button(f"Start {skill} Module")
    else:
        st.balloons()
        st.success("All skills matched. Continue learning!")

    st.subheader("🚦 Workflow Progress")
    steps = [
        "Profile Loaded", "Assessment Pending", "Assessment Completed",
        "Recommendations Generated", "Learning In Progress"
    ]
    for i, step in enumerate(steps):
        if i < progress_stage:
            st.markdown(f"✅ **{step}**")
        elif i == progress_stage:
            st.markdown(f"🟠 **{step}**")
        else:
            st.markdown(f"🔲 {step}")

elif view == "Admin Console":
    st.title("🧑‍💼 Admin Console")
    role_filter = st.selectbox("Filter by Role:", ["All"] + list(tsr_skills.keys()))

    st.subheader("📋 Learner Summary Table")
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
            "Progress": f"{percent}%",
            "Status": "Completed" if not gaps else "In Progress"
        })

    df = pd.DataFrame(rows)
    st.dataframe(df)

    st.download_button("📥 Download Report", df.to_csv(index=False).encode(), file_name="learner_report.csv")

    st.subheader("⚙️ Agent Framework Status")
    st.markdown("""
    - 🤖 **Profile Agent**: ✅ Active | Latency: 0.4s
    - 🧪 **Assessment Agent**: ✅ Stable | Last Sync: 1hr ago
    - 🎯 **Recommender Agent**: ✅ Running | 0 Errors
    - 📊 **Tracker Agent**: 🔄 Analyzing Patterns
    """)
