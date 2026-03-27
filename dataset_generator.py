import random
import pandas as pd

interests = ["AI","Web","Data Science","Cybersecurity"]
skills = ["Beginner","Intermediate","Advanced"]
languages = ["Python","JavaScript","Java","C++"]
certs = ["Yes","No"]

projects = [
"Chatbot","Recommendation System","AI Assistant","Portfolio Website",
"E-commerce Website","Sales Prediction","Fraud Detection","Image Classifier",
"Network Scanner","Full Stack App","Stock Prediction","Voice Assistant"
]

data = []

for _ in range(1000):
    row = [
        random.choice(interests),
        random.choice(skills),
        random.choice(languages),
        random.choice(certs),
        random.choice(projects)
    ]
    data.append(row)

df = pd.DataFrame(data, columns=["Interest","Skill","Language","Cert","Project"])
df.to_csv("dataset.csv", index=False)

print("✅ Dataset created: dataset.csv")