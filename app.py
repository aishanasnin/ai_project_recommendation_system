from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


df = pd.read_csv("dataset.csv")

encoders = {}

for col in ["Interest", "Skill", "Language", "Cert"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df[["Interest", "Skill", "Language", "Cert"]]
y = df["Project"]

# =========================
# MODEL TRAINING
# =========================
model = DecisionTreeClassifier()
model.fit(X, y)

# =========================
# NORMALIZATION FUNCTION
# =========================
def normalize_input(interest, skill, language, cert):

    interest = interest.lower().strip()
    skill = skill.lower().strip()
    language = language.lower().strip()
    cert = cert.lower().strip()

    if "ai" in interest or "ml" in interest:
        interest = "AI"
    elif "web" in interest:
        interest = "Web"
    elif "data" in interest:
        interest = "Data Science"
    elif "cyber" in interest:
        interest = "Cybersecurity"
    else:
        interest = "AI"

    if skill in ["beginner"]:
        skill = "Beginner"
    elif skill in ["intermediate", "medium", "normal"]:
        skill = "Intermediate"
    else:
        skill = "Advanced"

    if "python" in language:
        language = "Python"
    elif "javascript" in language:
        language = "JavaScript"
    elif "java" in language:
        language = "Java"
    elif "c++" in language:
        language = "C++"
    else:
        language = "Python"

    if cert in ["yes", "y", "yeah"]:
        cert = "Yes"
    else:
        cert = "No"

    return interest, skill, language, cert

def generate_features(interest, skill, language, prediction):

    # 🎯 Reason
    reason = f"This project is recommended because you are interested in {interest} and have {skill} level skills in {language}."

    # 📊 Confidence Score (simple logic)
    if skill == "Advanced":
        confidence = "90%"
    elif skill == "Intermediate":
        confidence = "75%"
    else:
        confidence = "60%"

    # 📉 Skill Gap
    if skill == "Beginner":
        gap = "You need to improve core programming and basic concepts."
    elif skill == "Intermediate":
        gap = "You should strengthen problem solving and frameworks."
    else:
        gap = "Focus on optimization and advanced system design."

    # 📚 Learning Path
    learning = f"Start with {language} basics → Build mini projects → Develop {prediction}"

    # 🔁 Multi Recommendation
    extra_projects = ["Portfolio Website", "Chatbot", "AI Assistant"]

    # 🎯 Difficulty
    if skill == "Beginner":
        difficulty = "Easy"
    elif skill == "Intermediate":
        difficulty = "Medium"
    else:
        difficulty = "Hard"

    return reason, confidence, gap, learning, extra_projects, difficulty

# =========================
# ROUTE
# =========================
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # =========================
        # GET FORM DATA
        # =========================
        interest = request.form.get("interest", "")
        skill = request.form.get("skill", "")
        language = request.form.get("language", "")
        cert = request.form.get("cert", "")

        # =========================
        # NORMALIZE INPUT
        # =========================
        interest, skill, language, cert = normalize_input(
            interest, skill, language, cert
        )

        # =========================
        # FILE UPLOAD
        # =========================
        resume = request.files.get("resume")
        certificate = request.files.get("certificate")

        resume_name = ""
        certificate_name = ""

        if resume and resume.filename != "":
            resume_name = secure_filename(resume.filename)
            resume.save(os.path.join(app.config["UPLOAD_FOLDER"], resume_name))

        if certificate and certificate.filename != "":
            certificate_name = secure_filename(certificate.filename)
            certificate.save(os.path.join(app.config["UPLOAD_FOLDER"], certificate_name))

        # =========================
        # ENCODE INPUT
        # =========================
        user_input = []

        for col, val in zip(
            ["Interest", "Skill", "Language", "Cert"],
            [interest, skill, language, cert],
        ):
            if val in encoders[col].classes_:
                encoded_val = encoders[col].transform([val])[0]
            else:
                encoded_val = 0
            user_input.append(encoded_val)

        # =========================
        # PREDICTION
        # =========================
        prediction = model.predict([user_input])[0]

        # =========================
        # EXTRA FEATURES
        # =========================
        reason, confidence, gap, learning, extra_projects, difficulty = generate_features(
            interest, skill, language, prediction
        )

        # =========================
        # SEND TO RESULT PAGE
        # =========================
        return render_template(
            "result.html",
            result=prediction,
            reason=reason,
            confidence=confidence,
            gap=gap,
            learning=learning,
            extra_projects=extra_projects,
            difficulty=difficulty,
            resume=resume_name,
            certificate=certificate_name
        )

    # =========================
    # GET REQUEST
    # =========================
    return render_template("index.html")

# ✅ OUTSIDE FUNCTION
if __name__ == "__main__":
    app.run(debug=True)