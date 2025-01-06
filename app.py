import streamlit as st
import pandas as pd
import numpy as np  # Ajout de l'import numpy
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def generate_sample_data():
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    return {
        'nps_data': pd.DataFrame({
            'Date': dates,
            'NPS': [35 + np.random.normal(0, 5) for _ in dates],
            'Satisfaction': [4.2 + np.random.normal(0, 0.2) for _ in dates],
            'Réponses': [100 + np.random.normal(0, 10) for _ in dates]
        }),
        'design_system': pd.DataFrame({
            'Date': dates,
            'Taux_Adoption': [65 + i for i in range(len(dates))],
            'Composants_Utilisés': [25 + i for i in range(len(dates))]
        }),
        'engagement': pd.DataFrame({
            'Date': dates,
            'Score_Engagement': [7.5 + np.random.normal(0, 0.5) for _ in dates],
            'Participation': [90 + np.random.normal(0, 5) for _ in dates]
        })
    }

# Données
data = generate_sample_data()

# Titre et filtres
st.title('Dashboard KPIs UX')
periode = st.select_slider(
    'Période',
    options=data['nps_data']['Date'].dt.strftime('%B %Y').tolist(),
    value=(data['nps_data']['Date'].dt.strftime('%B %Y').iloc[0],
           data['nps_data']['Date'].dt.strftime('%B %Y').iloc[-1])
)

# 1. Satisfaction Utilisateur
st.header('1. Satisfaction Utilisateur')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("NPS", f"{data['nps_data']['NPS'].iloc[-1]:.0f}", 
              f"{data['nps_data']['NPS'].iloc[-1] - data['nps_data']['NPS'].iloc[-2]:.1f}")
with col2:
    st.metric("Satisfaction", f"{data['nps_data']['Satisfaction'].iloc[-1]:.1f}/5")
with col3:
    st.metric("Réponses", f"{data['nps_data']['Réponses'].iloc[-1]:.0f}")

fig_nps = px.line(data['nps_data'], x='Date', y=['NPS', 'Satisfaction'],
                  title='Évolution NPS et Satisfaction')
st.plotly_chart(fig_nps, use_container_width=True)

# 2. Design System
st.header('2. Adoption du Design System')
col1, col2 = st.columns(2)
with col1:
    st.metric("Taux d'adoption", 
              f"{data['design_system']['Taux_Adoption'].iloc[-1]:.0f}%",
              f"{data['design_system']['Taux_Adoption'].iloc[-1] - data['design_system']['Taux_Adoption'].iloc[-2]:.1f}%")
with col2:
    st.metric("Composants utilisés", 
              f"{data['design_system']['Composants_Utilisés'].iloc[-1]}")

fig_design = go.Figure()
fig_design.add_trace(go.Bar(x=data['design_system']['Date'],
                           y=data['design_system']['Taux_Adoption'],
                           name="Taux d'adoption"))
fig_design.update_layout(title="Évolution de l'adoption du Design System")
st.plotly_chart(fig_design, use_container_width=True)

# 3. Engagement des équipes
st.header('3. Engagement des équipes')
col1, col2 = st.columns(2)
with col1:
    st.metric("Score d'engagement", 
              f"{data['engagement']['Score_Engagement'].iloc[-1]:.1f}/10",
              f"{data['engagement']['Score_Engagement'].iloc[-1] - data['engagement']['Score_Engagement'].iloc[-2]:.1f}")
with col2:
    st.metric("Taux de participation", 
              f"{data['engagement']['Participation'].iloc[-1]:.0f}%")

fig_engagement = px.line(data['engagement'], x='Date', y='Score_Engagement',
                        title="Évolution de l'engagement")
st.plotly_chart(fig_engagement, use_container_width=True)

# Ajout d'un filtre pour télécharger les données
st.download_button(
    label="Télécharger les données",
    data=pd.concat([data['nps_data'], data['design_system'], data['engagement']], axis=1).to_csv(),
    file_name='ux_kpis_data.csv',
    mime='text/csv'
)