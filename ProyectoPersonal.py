import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as mp 
import plotly.express as ex 

get_data='muse_dataset.csv'

@st.cache_data
def cache_data(nrows):
    data=pd.read_csv(get_data, nrows=nrows)
    return data

#--- PAGE CONFIG ---#
st.set_page_config(page_title="Proyecto: MuSe Music Sentiment Analysis", ##Estas dos lineas
                   page_icon=":headphones:")      #Modifican el folder (pagina)


st.title('MuSe Music Sentiment Analysis')
st.markdown("**Realizado por:**")
st.markdown("""Juan David Delgado Muñoz\n
    Matricula: S20006756\n
    email: ZS20006756@estudiantes.uv.mx\n
    Licenciatura en Ingenieria de Software.""")

sidebar=st.sidebar
sidebar.image("MuSe.png")
sidebar.markdown("##")

visualizar=sidebar.checkbox("**Mostrar datos cargados en cache.**")

if (visualizar):
    data_general=cache_data(500)
    count_row = data_general.shape[0]
    st.subheader("Datos cargados en cache")
    st.write(f"Total de datos cargados: {count_row}")
    st.dataframe(data_general)


sidebar.markdown("___")

tracktext_input=sidebar.text_input("**Ingresa el nombre del track**")
trackbutton=sidebar.button("**Buscar**")

def databytrack(track):
    data=cache_data(500)
    new_data=data[data['track'].str.contains(track)]
    return new_data

if (trackbutton):
    data=databytrack(tracktext_input)
    st.subheader('**Coincidencias de canciones por track**')
    st.write(f"No. de Coincidencias con '{tracktext_input}': {data.shape[0]}")
    st.dataframe(data)

sidebar.markdown('___')

artistms=sidebar.multiselect("**Filtrar canciones por artista:**",
                             options=cache_data(500)['artist'].unique())

artistselection=cache_data(500).query('artist==@artistms').sort_values(by='artist')
st.subheader('Canciones por artistas')
st.dataframe(artistselection)