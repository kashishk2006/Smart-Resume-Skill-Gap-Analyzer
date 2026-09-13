import streamlit as st
from pypdf import PdfReader
import json

st.title("📄Smart Resume Skill Gap Analyzer")
st.caption("AI-powered resume analysis for your target career role")
st.write("")
st.write("Upload your resume, select a target role, and discover the skills you need to improve.")

st.divider()
st.subheader("🔎 How It Works")
st.write("1. Upload your resume")
st.write("2. Select your target job role")
st.write("3. Analyze your skills")
st.write("4. Get your skill gaps and learning recommendations")
col1, col2 = st.columns(2)
with col1:
    resume = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])
    st.caption("PDF format only • Your resume is analyzed locally")
    st.caption("🔒 Your resume is used only for analysis.")
with open("skills.json", "r") as file:
    job_skills = json.load(file)
with col2:
    job_role = st.selectbox("🎯 Select your target job role", list(job_skills.keys()))

if resume and st.button("🔍 Analyze Resume", use_container_width=True):
    reader = PdfReader(resume)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    st.success(f"Resume uploaded: {resume.name}")
    st.write("Resume text extracted successfully!")

    required_skills = job_skills.get(job_role, [])
    text_lower = text.lower()
    text_lower = text_lower.replace("/", " ")

    found_skills = []

    for skill in required_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
        elif skill == "Agile" and any(word in text_lower for word in ["scrum", "sprint", "kanban"]):
            found_skills.append(skill)
        elif skill == "Communication" and any(word in text_lower for word in ["presentation", "presented", "workshop", "leadership", "teamwork"]):
            found_skills.append(skill)
        elif skill == "Market Research" and any(word in text_lower for word in ["marketing", "market analysis", "customer research", "competitor analysis"]):
            found_skills.append(skill)
        elif skill == "Product Strategy" and any(word in text_lower for word in ["product management", "product strategy", "roadmap", "product planning"]):
            found_skills.append(skill)
        elif skill == "Data Analysis" and any(word in text_lower for word in ["data analysis", "data analytics", "data visualization"]):
            found_skills.append(skill)
        elif skill == "User Research" and any(word in text_lower for word in ["customer", "user", "survey", "feedback", "user needs"]):
            found_skills.append(skill)
    st.subheader("✅Skills Found")
    st.caption(f"{len(found_skills)} relevant skills detected")

    for skill in found_skills:
        st.write(f"✅ {skill} — Found in your resume")
    if not found_skills:
        st.info("No matching skills were detected. Try adding relevant skills to your resume.")

    missing_skills = [skill for skill in required_skills if skill not in found_skills]

    st.subheader("❌Skills Missing")
    st.caption(f"{len(missing_skills)} skills need improvement")

    for skill in missing_skills:
        st.write(f"❌ {skill} — Not found in your resume")
    if not missing_skills:
        st.success("Great! No skill gaps were detected for this role.")

    recommendations = {
        "Market Research": "Learn market research fundamentals",
        "Agile": "Learn Agile and Scrum basics",
        "Business Analysis": "Learn business analysis fundamentals",
        "Communication": "Improve presentation and communication skills",
        "Python": "Learn Python fundamentals",
        "SQL": "Learn SQL basics",
        "Excel": "Learn Excel for data analysis",
        "Power BI": "Learn Power BI and dashboard creation",
        "Statistics": "Learn basic statistics",
        "TensorFlow": "Learn TensorFlow fundamentals",
        "AI/ML": "Learn AI and Machine Learning fundamentals",
    }

    st.subheader("📚Recommended Learning")

    for skill in missing_skills:
        st.write(f"📚 {skill} → {recommendations.get(skill, 'Learn this skill')}")
    score = int((len(found_skills) / len(required_skills)) * 100)

    st.subheader("📊Resume Match Score")
    st.metric("Match Score", f"{score}%")
    st.caption("Based on the skills detected for your selected role.")
    st.progress(score / 100)
    if score >= 80:
        st.success("Great match! Your resume fits this role well.")
    elif score >= 50:
        st.warning("Good start! A few more skills can improve your match.")
    else:
        st.error("Your resume needs more skills for this role.")
    st.write(f"{len(found_skills)} / {len(required_skills)} skills matched")
    st.caption("The score is based on how many relevant skills were detected in your resume for the selected role.")
    st.subheader("📝Resume Suggestions")

    if missing_skills:
        st.write("Consider adding projects, certifications, or experience related to:")
        for skill in missing_skills:
            st.write(f"• {skill}")
    else:
        st.success("Your resume covers all the required skills!")

    if st.button("🔄 Start Over"):
        st.rerun()
    st.subheader("🚀Career Readiness")

    if score >= 80:
        st.write("🌟 You are well prepared for this role.")
    elif score >= 50:
        st.write("📈 You are on the right track. Focus on the missing skills.")
    else:
        st.write("🚀 Build the missing skills to become more prepared for this role.")
    st.divider()
    st.write("")
    st.caption("Smart Resume Skill Gap Analyzer • Built with Python & Streamlit")