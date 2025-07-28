# streamlit_app.py
import streamlit as st
import pandas as pd

# --- Synthetic TSR Skill Data ---
tsr_skills = {
    "Data Engineer": {"Python": 4, "SQL": 5, "Cloud": 4, "ETL": 3},
    "Data Analyst": {"Python": 3, "SQL": 5, "Visualization": 4},
    "ML Engineer": {"Python": 5, "ML": 4, "Deep Learning": 3}
}

# --- Synthetic Learner Profiles ---
learners = [
    {"name": "Keerthika", "role": "Data Engineer", "skills": {"Python": 3, "SQL": 4, "Cloud": 2}},
    {"name": "Arjun", "role": "Data Analyst", "skills": {"Python": 2, "SQL": 5, "Visualization": 2}},
    {"name": "Priya", "role": "Data Engineer", "skills": {"Python": 4, "SQL": 3, "Cloud": 3}},
    {"name": "Rahul", "role": "ML Engineer", "skills": {"Python": 4, "ML": 3, "Deep Learning": 1}},
    {"name": "Sneha", "role": "Data Analyst", "skills": {"Python": 3, "SQL": 4, "Visualization": 3}},
    {"name": "Vikram", "role": "ML Engineer", "skills": {"Python": 5, "ML": 4, "Deep Learning": 2}},
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

# --- Workflow Progress ---
def get_progress_state(user):
    gaps = calculate_skill_gap(user)
    if not gaps:
        return 5  # Learning In Progress
    return 3  # Recommendations Generated (simulated)

# --- Custom UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #f9fcff; }
    .block-container { padding: 2rem; }
    h1, h2, h3, h4 { color: #0A84FF; }
    .stButton>button {
        background-color: #0A84FF;
        color: white;
        border-radius: 10px;
        padding: 8px 16px;
    }
    .stProgress>div>div>div {
        background-color: #0A84FF;
    }
    </style>
""", unsafe_allow_html=True)

# --- Login Simulation ---
st.sidebar.title("🔐 Login Panel")
user_names = [l["name"] for l in learners]
current_user_name = st.sidebar.selectbox("Login as Consultant:", user_names)
current_user = next(user for user in learners if user["name"] == current_user_name)

# --- Sidebar Navigation ---
st.sidebar.title("📚 Skill-Gap System")
view = st.sidebar.radio("Select View:", ["Learner Dashboard", "Admin Console"])

if view == "Learner Dashboard":
    st.title("👩‍🎓 Learner Dashboard")
    user = current_user
    gaps = calculate_skill_gap(user)
    progress_stage = get_progress_state(user)

    st.markdown(f"### 👤 Profile: {user['name']}")
    st.write(f"**Role:** {user['role']}")
    st.write("**Current Skills:**", user["skills"])

    st.markdown("### 🧠 Skill Gap")
    if gaps:
        st.table(pd.DataFrame(gaps.items(), columns=["Skill", "Gap"]))
    else:
        st.success("No skill gaps! You're aligned with TSR expectations.")

    st.markdown("### 🗺️ Learning Path Recommendations")
    for skill, gap in gaps.items():
        st.markdown(f"**{skill}** — Improve by {gap} level(s). Why it matters: _Critical for role expectations_.")
        st.progress(1 - (gap / tsr_skills[user["role"]][skill]))
        st.button(f"Start {skill} Module")

    st.markdown("### 🚦 Workflow Progress")
    progress_steps = [
        "Profile Loaded", "Assessment Pending", "Assessment Completed",
        "Recommendations Generated", "Learning In Progress"
    ]
    for i, step in enumerate(progress_steps):
        if i < progress_stage:
            st.markdown(f"✅ {step}")
        elif i == progress_stage:
            st.markdown(f"🔄 {step}")
        else:
            st.markdown(f"⏳ {step}")

elif view == "Admin Console":
    st.title("🛠️ Admin Console")
    st.markdown("### 🔍 Filter Learners")
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
    - **Profile Agent**: ✅ Active, latency 0.5s  
    - **Assessment Agent**: ✅ Completed, no errors  
    - **Recommender Agent**: ✅ Generated paths in real-time  
    - **Tracker Agent**: 🔄 Detecting plateaus
    """)
