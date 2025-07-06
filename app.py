import streamlit as st
import pandas as pd
import plotly.express as px

#To Load the dataset
df=pd.read_csv('pakistan_jobs_data.csv')
st.set_page_config(page_title="Pakistan Job Skills Demand",layout="wide")
st.title("📍Pakistan Job Skills Demand Heatmap ")
st.markdown("Analyze job skills demand across Pakistan using real and simulated data.")
# Displaying the dataset
with st.sidebar:
    st.header("Filter Options")
    location=st.multiselect("Select City",options=df['Location'].unique())
   # Collect all unique skills from the Skills column
all_skills = df["Skills"].dropna().str.split(",").explode().str.strip().unique()

# Create multiselect with those skills
selected_skills = st.multiselect("Select Skill", options=sorted(all_skills))

# Filtering the dataset
if location:
    df=df[df["Location"].isin(location)]
if selected_skills:
    df=df[df["Skills"].str.contains('|'.join(selected_skills),case=False)] 
# Displaying the filtered dataset
st.subheader("📊 Top In-Demand Skills") 
all_skills=df["Skills"].str.split(", ").explode().value_counts().nlargest(10) 
st.bar_chart(all_skills) 
# Displaying the heatmap
st.subheader("📍 Job Distribution by City")
city_count=df["Location"].value_counts()
st.plotly_chart(px.bar(city_count,x=city_count.index,y=city_count.values,labels={"x":"City","y":"Distribution"},title="Job Distribution per City"))
#Salary Distribution
st.subheader("💵 Salary Distribution")
st.plotly_chart(px.box(df,x="Location",y="Salary",color="Location",title="Salary by City")) 
# Simulated data for province-wise job demand
st.subheader("🗺️ Province-wise Job Demand (Simulated Data)")
heatmap_data=df["Province"].value_counts().reset_index()
heatmap_data.columns=["Province","Job Count"]

st.plotly_chart(px.choropleth(heatmap_data,locations="Province",locationmode="country names",color="Job Count",title="Simulated Heatmap by Province"))