import streamlit as st
import pickle
import numpy as np

def load_model():
    with open(r'C:\Users\berna\ml_salary2\models\model.pk1', 'rb') as file:
        data = pickle.load(file)
    return data
    
data = load_model()

regressor = data["model"]
laben_country = data["laben_country"]
laben_edu = data["laben_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        'United States', 
        'India', 
        'Germany', 
        'Australia',
        'Russian Federation', 
        'Brazil', 'Israel', 
        'Switzerland', 
        'Spain',
        'Poland', 
        'France', 
        'Netherlands', 
        'United Kingdom', 
        'Canada',
        'Sweden', 
        'Italy', 
        'Turkey', 
        'Ukraine', 
        'Belgium'
    )

    education = (
        'Bachelor’s degree', 
        'Master’s degree', 
        'Higher Post Graduate',
        'Less than Bachelors'
    )

    country = st.selectbox('Country', countries)
    education = st.selectbox('Education level', education)

    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience]])
        X[:,0] = laben_country.transform(X[:,0])
        X[:,1] = laben_edu.transform(X[:,1])
        X = X.astype(float)
    
        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:,.2f}")