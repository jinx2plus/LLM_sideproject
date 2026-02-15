# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
from inspect import getmembers

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('??, '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

try:
    models = genai.list_models()
    print("?ъ슜 媛?ν븳 紐⑤뜽 紐⑸줉:")
    n=1
    for model in models:
        n += 1
        print(n,'踰덉?')
        print(f"- {model.name}: {model.description}")
except Exception as e:
    print("紐⑤뜽 紐⑸줉??媛?몄삤?붾뜲 ?ㅻ쪟媛 諛쒖깮?덉뒿?덈떎:", e)
    

file_path = r'TA.xlsx'
data = pd.read_excel(file_path)

high_risk_areas = data.groupby('NODE_ID').agg(
    total_deaths=('Deaths', 'sum'),
    total_serious_injuries=('SeriousInj', 'sum'),
    total_MajorInj=('MajorInj', 'sum'),
    total_MinorInj=('MinorInj', 'sum')
).reset_index()

high_risk_areas["EPDO"] = high_risk_areas['total_deaths']*12 + high_risk_areas['total_serious_injuries']*6+ high_risk_areas['total_MajorInj']*3

high_risk_areas = high_risk_areas[
    (high_risk_areas['total_deaths'] > 1) |
    (high_risk_areas['total_serious_injuries'] > 1) |
    (high_risk_areas['total_MajorInj'] > 1) |
    (high_risk_areas["EPDO"] >1)
]

high_risk_data = pd.merge(high_risk_areas, data, on='NODE_ID', how='left')

high_risk_data = high_risk_data[high_risk_data["EPDO"]<1500]

def generate_safety_improvement_suggestion(row):
    
    
    prompt = f
    
    model = genai.GenerativeModel('gemini-2.0-flash-exp')

    no=1
    try:
        response = model.generate_content(prompt)
        suggestion = response.text
        print(suggestion)
        no += 1
        print("NODEID",row['NODE_ID'],no,"踰덉옱")
        return suggestion
    except Exception as e:
        print("Error generating suggestion:", e)
        return None

    
    
    

high_risk_data2 = high_risk_data.copy()

high_risk_data2['safety_suggestion'] = high_risk_data2 .apply(generate_safety_improvement_suggestion, axis=1)

high_risk_data2[['NODE_ID',"NO", 'total_deaths', 'total_serious_injuries','Crashtype','Weather','NODE_TYPE','TURN_P', 'LINK_ID', 'LANES', 'ROAD_TYPE', 'CONNECT','MAX_SPD', 'REST_VEH', 'CURVATURE', 'SLOPE','safety_suggestion']].to_csv("safety_improvement_suggestions_END_ENGtoKOR_all_241213.csv", index=False, encoding="utf-8-sig")

print(high_risk_data2[['NODE_ID', 'safety_suggestion']].head())

    
        
        

 

    
    
    
    
    

                       
    
    

    
        
        
    
