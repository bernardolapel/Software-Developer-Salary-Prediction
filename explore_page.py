import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categoies(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map
    
def clean_experience(value):
    if value == "Less than 1 year":
        return 0.5
    elif value == "More than 50 years":
        return 50
    else:
        return float(value)
        
def clean_education(level):
    if 'Bachelor’s degree' in level:
        return 'Bachelor’s degree'
    elif 'Master’s degree' in level:
        return 'Master’s degree'
    elif 'Other doctoral degree' in level or 'Professional degree' in level:
        return ' Higher Post Graduate'
    else:
        return 'Less than Bachelors'


@st.cache_data        
def load_data():
    df = pd.read_csv(r"C:\Users\berna\Downloads\Datasets\survey_results_public 2019.csv")
    df_1 = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedComp']]
    df_1 = df_1.rename({'ConvertedComp': 'Salary'}, axis=1)
    df_1 = df_1.dropna(subset=['Salary'])
    df_1 = df_1.dropna()
    df_1 = df_1[df_1['Employment'] == "Employed full-time"]
    df_1.drop(['Employment'], axis=1, inplace=True)
    
    country_cat = df_1.Country.value_counts()
    country_map = shorten_categoies(country_cat, 400)
    df_1['Country'] = df_1['Country'].map(country_map)
    df_1 = df_1[df_1['Salary'] <= 170000]
    df_1 = df_1[df_1['Salary'] >= 10000]
    df_1 = df_1[df_1['Country'] != 'Other']
    
    
    df_1.YearsCodePro = df_1.YearsCodePro.apply(clean_experience)
    df_1.EdLevel = df_1.EdLevel.map(clean_education)
    return df_1

df_1 = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    
    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )
    
    country_cat = df_1.Country.value_counts()
    data = country_cat
    
    fig1, ax1 = plt.subplots(figsize=(10, 10))
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=140)
    ax1.axis("equal") # Equal aspect ration ensures that pie is drawn as circle.
    
    st.write("""#### Number of Data from different countries""")
    
    st.pyplot(fig1)
    
    st.write(""" #### Mean Salary Based On Country""")
    
    data = df_1.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
    
    st.write(""" #### Mean Salary Based On Experience""")
    
    data = df_1.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
    
    st.write(""" #### Maximum Salary Based On Country""")
    
    data = df_1.groupby(["Country"])["Salary"].max().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(""" #### Minimum Salary Based On Country""")
    
    data = df_1.groupby(["Country"])["Salary"].min().sort_values(ascending=True)
    st.bar_chart(data)