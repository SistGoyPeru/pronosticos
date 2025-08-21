from scraper import FootballDataScraper
from clases import liga
from scipy.stats import poisson
import streamlit as st
import matplotlib.pyplot as plt


def main():
  
  
    url = 'https://www.livefutbol.com/todos_partidos/per-primera-division-2025-clausura/'
    LigaBolivia = liga(url)
    
    
    st.sidebar.header("Encuentros")
   
    local=st.sidebar.selectbox("Equipo Local",LigaBolivia.equipos_local())
    visita=st.sidebar.selectbox("Equipo Visita",LigaBolivia.equipos_visita())
    st.markdown("## "+local+" - "+visita)
    total1,total2=st.columns(2,gap='large')
    with total1:
    
      st.metric(label="Fuerza Promedio Local",value="{:.2f}".format(LigaBolivia.fuerzaPromedioLocal(local,visita)))
    
    with total2:
    
      st.metric(label="Fuerza Promedio Visita",value="{:.2f}".format(LigaBolivia.fuerzaPromedioVisita(local,visita)))
  
   

if __name__ == "__main__":
  main()
