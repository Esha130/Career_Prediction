# career_dashboard.py
import streamlit as st
import pandas as pd
import os

# --- CONFIG ---
st.set_page_config(page_title="Career Guidance", layout="wide")
career_df = pd.read_csv("career_mappings.csv")

# --- HEADER ---
st.title("🧭 Career Guidance")
st.markdown("### Helping students choose the right career path based on interests, skills, and goals 🎯")

# --- SIDEBAR INPUT ---
st.sidebar.header("📝 Your Details")
age = st.sidebar.number_input("Age", 16, 50, 22)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
education = st.sidebar.selectbox("Highest Education", ["Diploma", "UG", "PG", "PhD"])
location = st.sidebar.selectbox("Preferred Location", ["India", "USA", "UK", "Remote"])
interest = st.sidebar.selectbox("Interest Area", sorted(career_df["Interest"].unique()))
skills = st.sidebar.text_area("Key Skills (comma-separated)", "Python, Excel, SQL")
work_style = st.sidebar.selectbox("Preferred Work Style", ["Remote", "On-site", "Hybrid"])
soft_skills = st.sidebar.multiselect("Soft Skills", ["Communication", "Leadership", "Creativity", "Teamwork", "Problem-solving"])
goal = st.sidebar.text_area("Career Goal", placeholder="I want to work in AI and solve real-world problems.")

# --- PROCESSING ---
if st.sidebar.button("🔍 Recommend Careers"):

    matched = career_df[career_df["Interest"] == interest]
    if matched.empty:
        st.error("Sorry, no careers found for that interest.")
    else:
        for _, row in matched.iterrows():
            col1, col2 = st.columns([1, 3])
            
            # --- Career Icon ---
            with col1:
                img_path = row["Image"]
                if os.path.exists(img_path):
                    st.image(img_path, width=80)
                else:
                    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135789.png", width=80)

            # --- Career Info ---
            with col2:
                st.subheader(f"🚀 Career Path: {row['Career']}")
                st.markdown(f"**Suggested Skills:** {row['Suggested Skills']}")
                st.markdown(f"**Average Salary in {location}:** ₹{int(row['Average Salary (India)']):,} / year")
                st.markdown(f"**Popular Course:** {row['Popular Courses']}")
                st.markdown("---")
        
       
        # --- Save User Input to CSV ---
        user_log = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "education": education,
            "location": location,
            "interest": interest,
            "skills": skills,
            "soft_skills": ",".join(soft_skills),
            "goal": goal
        }])
        if os.path.exists("user_logs.csv"):
            user_log.to_csv("user_logs.csv", mode='a', header=False, index=False)
        else:
            user_log.to_csv("user_logs.csv", index=False)

        st.success("✅ Your recommendation has been saved for future personalization.")
