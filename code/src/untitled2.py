# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import google.generativeai as genai
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import openai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

accident_data = pd.read_excel('TA.xlsx', sheet_name='TA')

openai.api_key = os.getenv("OPENAI_API_KEY")

selected_columns = ['Year', 'Month', 'Day', 'Timezone', 'Weather', 'Crashtype', 'Violation', 
                    'InjNO', 'City', 'Dong_name', 'Place', 'MAX_SPD', 'LANES',"NODE_ID"]
accident_data = accident_data[selected_columns]

accident_data = accident_data.dropna()

def determine_hour(hour):
    if hour=="二쇨컙(06??17??":
        return 6
    else:
        return 18
    
def determine_time_of_day(hour):
    if 6 <= hour <= 17:
        return '二쇨컙'
    else:
        return '?쇨컙'

accident_data['Hour'] = accident_data['Timezone'].apply(determine_hour)

accident_data['TimeOfDay'] = accident_data['Hour'].apply(determine_time_of_day)

accident_data = accident_data.drop('Timezone', axis=1)

categorical_features = ['Weather', 'Crashtype', 'Violation', 'City', 'Dong_name', 'Place', 'TimeOfDay']
accident_data = pd.get_dummies(accident_data, columns=categorical_features, drop_first=True)

print(accident_data.head())

hd_map_data = pd.read_csv('hd_map_data.csv')
merged_data = pd.merge(accident_data, hd_map_data, how='left', on='NODE_ID')

merged_data = merged_data.dropna()

X = merged_data.drop(['Crashtype_?뺣㈃異⑸룎'], axis=1)  # ?寃?蹂?섏뿉 ?곕씪 議곗젙
y = merged_data['Crashtype_?뺣㈃異⑸룎']  # ?덉륫?섎젮???寃?蹂??

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('?덉륫媛?)
plt.ylabel('?ㅼ젣媛?)
plt.title('?쇰룞 ?됰젹')
plt.show()

def generate_safety_improvement_suggestion(row):
    prompt = f
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a traffic safety expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        suggestion = response.choices[0].message['content'].strip()
        return suggestion
    except Exception as e:
        print("Error generating suggestion:", e)
        return None

merged_data['Safety_Suggestion'] = merged_data.apply(generate_safety_improvement_suggestion, axis=1)

print(merged_data[['NODE_ID', 'Safety_Suggestion']].head())
