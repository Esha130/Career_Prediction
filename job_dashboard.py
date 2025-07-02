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

# --- EDUCATION DETAIL SECTION ---
st.header("🎓 Tell us about your Education")

education_level = st.selectbox(
    "📘 What is your highest level of education?",
    ["High School", "Diploma", "Bachelor's", "Master's", "PhD"]
)

education_stream = ""
degree_focus = ""

# High School
if education_level == "High School":
    education_stream = st.selectbox(
        "🏫 What was your stream?",
        ["Science", "Commerce", "Arts", "Other"]
    )
    degree_focus = st.text_input("✍️ Optional: Add any focus subject or board")

# Diploma
elif education_level == "Diploma":
    education_stream = st.selectbox(
        "🏫 What was your diploma specialization?",
        ["Computer Engineering", "Electronics", "Business", "Mechanical", "Design", "Other"]
    )

# Bachelor's
elif education_level == "Bachelor's":
    education_stream = st.selectbox(
        "📚 What was your stream in Bachelor's?",
        ["Science", "Commerce", "Engineering", "Arts", "Computer Applications", "Other"]
    )
    if education_stream == "Science":
        degree_focus = st.selectbox("🔍 Specialization", ["BSc in Data Science", "BSc in Physics", "Other"])
    elif education_stream == "Engineering":
        degree_focus = st.selectbox("🔍 Specialization", ["Computer Science", "IT", "Mechanical", "Other"])
    elif education_stream == "Commerce":
        degree_focus = st.selectbox("🔍 Specialization", ["BCom", "BBA", "CA", "Other"])
    elif education_stream == "Arts":
        degree_focus = st.selectbox("🔍 Specialization", ["BA in Psychology", "BA in Economics", "Other"])
    else:
        degree_focus = st.text_input("✍️ Enter your Bachelor's specialization:")

# Master's
elif education_level == "Master's":
    education_stream = st.selectbox(
        "📚 What was your stream in Master's?",
        ["Science", "Engineering", "MBA", "Arts", "Computer Applications", "Other"]
    )
    if education_stream == "Science":
        degree_focus = st.selectbox("🔍 Specialization", ["MSc in Data Science", "MSc in Statistics", "Other"])
    elif education_stream == "Engineering":
        degree_focus = st.selectbox("🔍 Specialization", ["M.Tech in CS", "M.Tech in IT", "Other"])
    elif education_stream == "MBA":
        degree_focus = st.selectbox("🔍 Specialization", ["Finance", "Marketing", "Analytics", "Other"])
    elif education_stream == "Arts":
        degree_focus = st.selectbox("🔍 Specialization", ["MA in Psychology", "MA in Economics", "Other"])
    else:
        degree_focus = st.text_input("✍️ Enter your Master's specialization:")

# PhD
elif education_level == "PhD":
    education_stream = st.text_input("📚 Field of Research")
    degree_focus = st.text_input("🔍 Topic or Specialization")

# Final Education String
if degree_focus:
    full_education = f"{education_level} in {education_stream} - {degree_focus}"
else:
    full_education = f"{education_level} in {education_stream}"

location = st.sidebar.selectbox("Preferred Location", ["India", "USA", "UK", "Remote"])
interest = st.sidebar.selectbox("Interest Area", sorted(career_df["Interest Areas"].unique()))
skills = st.sidebar.text_area("Key Skills (comma-separated)", "Python, Excel, SQL")
work_style = st.sidebar.selectbox("Preferred Work Style", ["Remote", "On-site", "Hybrid"])
soft_skills = st.sidebar.multiselect("Soft Skills", ["Communication", "Leadership", "Creativity", "Teamwork", "Problem-solving"])
goal = st.sidebar.text_area("Career Goal", placeholder="I want to work in AI and solve real-world problems.")

# --- PROCESSING ---
if st.sidebar.button("🔍 Recommend Careers"):

    matched = career_df[career_df["Interest Areas"] == interest]
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
                st.markdown(f"**Suggested Skills:** {row['Required Skills']}")
                salary_column = f"Average Salary ({education_level})"
                base_salary = row.get(salary_column, "N/A")
                if str(base_salary).isdigit():
                    st.markdown(f"**Average Salary in {location} for {education_level}:** ₹{int(base_salary):,} / year")
                else:
                    st.markdown(f"**Average Salary in {location} for {education_level}:** Not Available")
                
                st.markdown(f"**Popular Course:** {row['Popular Courses']}")
                st.markdown("---")
        
       
        # --- Save User Input to CSV ---
        user_log = pd.DataFrame([{
            "age": age,
            "gender": gender,
            "education": full_education,
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
