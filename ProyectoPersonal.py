import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as mp 
import plotly.express as px 
import numpy as np

get_data='muse_dataset.csv'

#--- FUNCIÓN CACHE ---#
@st.cache_data
def cache_data(nrows):
    data=pd.read_csv(get_data, nrows=nrows)
    return data

#--- PAGE CONFIG ---#
st.set_page_config(page_title="Proyecto: MuSe Music Sentiment Analysis", ##Estas dos lineas
                   page_icon=":headphones:")      #Modifican el folder (pagina)

#--- PRESENTACION ---#
st.title('MuSe Music Sentiment Analysis')
st.markdown("**Realizado por:**")
st.markdown("""Juan David Delgado Muñoz\n
    Matricula: S20006756\n
    email: ZS20006756@estudiantes.uv.mx\n
    Licenciatura en Ingenieria de Software.""")

sidebar=st.sidebar
sidebar.image("MuSe.png")
sidebar.markdown("##")

#--- CHECHKBOX ---#
visualizar=sidebar.checkbox("**Mostrar datos cargados en cache.**")
st.subheader("Datos cargados en cache")
if (visualizar):
    data_general=cache_data(500)
    count_row = data_general.shape[0]
    st.write(f"Total de datos cargados: {count_row}")
    st.dataframe(data_general)

st.markdown("___")
sidebar.markdown("___")

#--- FILTRADO MEIANTE ENTRADA DE TEXTO Y BOTON ---#
tracktext_input=sidebar.text_input("**Ingresa el nombre del track**")
trackbutton=sidebar.button("**Buscar**")

def databytrack(track):
    data=cache_data(500)
    new_data=data[data['track'].str.match(track, case=False)]
    return new_data

#--- HISTOGRAMA: TAGS EN CADA CANCIÓN ---#
def graphicbytrackhisto(trackselected):
    if(len(trackselected)!=0):
        tags=["valence_tags", "arousal_tags", "dominance_tags"]
        histotrack=px.histogram(trackselected,
            x='track',
            y=tags,
            barmode='group',
            title="Comparación de los tags presentes por canción",
            labels=dict(track="Musica"),
            template="plotly_white"
        )
        histotrack.update_layout(yaxis_title="Valor del tag",plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(histotrack)


st.subheader('**Coincidencias de canciones por track**')

if (trackbutton):
    if(len(tracktext_input)!=0):
        data=databytrack(tracktext_input)
        st.write(f"No. de Coincidencias con '{tracktext_input}': {data.shape[0]}")
        st.dataframe(data)
        st.subheader('Histograma:')
        st.write("El siguiente histograma presenta por agrupación el valor de los tags contenidos en cada canción seleccionda (según la coincidencia).")
        graphicbytrackhisto(data)

st.markdown("___")
sidebar.markdown('___')

#--- MULTISELECT: FILTRADO DE CANCIONES POR ARTISTA ---#
artistms=sidebar.multiselect("**Filtrar canciones por artista:**",
                             options=cache_data(500)['artist'].unique())

artistselection=cache_data(500).query('artist==@artistms').sort_values(by='artist')
st.subheader('Canciones por artistas')
st.dataframe(artistselection)
graphicbyartistbutton=sidebar.button('Graficar artistas seleccionados.')

#--- GRAFICA SCATTER POR ARTISTA SELECCIONADO---#
def graphicbyartistscatter(artistselection):
    if(len(artistselection)!=0):
        st.subheader("Grafica de Scartter")
        st.write("La siguiente gráfica de scartter muestra el promedio obtenido en los diferentes tipos de tags con respecto a las canciones registradas por artista.")
        artistselection2=artistselection.groupby(by=['artist']).mean()[["valence_tags","arousal_tags","dominance_tags"]]
        tags=["valence_tags", "arousal_tags", "dominance_tags"]
        scarttertags=px.scatter(artistselection2,
                        x=artistselection2.index,
                         y=tags,
                         title="Promedio de tags en musica creada por artista",
                         labels=dict(artist="Artistas", value="Promedio de tags"),
                         template="plotly_white")
        scarttertags.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(scarttertags)
        st.dataframe(artistselection2)

if (graphicbyartistbutton):
    graphicbyartistscatter(artistselection)

st.markdown("___")
sidebar.markdown("___")

#--- NO. CANCINES REGISTRADAS POR ARTISTA ---#
#--- GRAFICA DE BARRAS --#
notracksbyartist=cache_data(500)['artist'].value_counts()
optionals = sidebar.expander("configuración de rango.", True)
optionals.subheader("Control para la grafica de barras.")
Notracks_min = optionals.slider(
    "No. Canciones minimo",
    min_value=int(notracksbyartist.values.min()),
    max_value=int(notracksbyartist.values.max())
)
Notracks_max = optionals.slider(
    "No. Canciones maximo",
    min_value=int(notracksbyartist.values.min()),
    max_value=int(notracksbyartist.values.max())
)
subset_notracks = notracksbyartist[(notracksbyartist.values <= Notracks_max) & (Notracks_min <= notracksbyartist.values)]

st.subheader("Grafica de barras")
st.write("La siguiente grafica de barras presenta el número de canciones por artista registradas en el dataset.")
if(len(subset_notracks)!=0):
    notracksbyartistbar=px.bar(subset_notracks,
                            x=subset_notracks.index,
                            y=subset_notracks.values,
                            title="No. canciones por artista",
                            template="plotly_white"
                            )
    notracksbyartistbar.update_layout(xaxis_title="Artista", yaxis_title="No.Canciones", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(notracksbyartistbar)
else:
    optionals.write("El val. min debe ser menor o igual al val.maximo.")
st.write(f'No. total de artistas: {subset_notracks.shape[0]}')