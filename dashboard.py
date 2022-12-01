import time  # to simulate a real time data, time loop

import numpy as np  
import pandas as pd 
import plotly.express as px  
import plotly.graph_objects as go 
import streamlit as st  

st.set_page_config(
    page_title="Programas Internacionales",
    page_icon="👻",
    layout="wide"
)

# read csv from a URL
@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv('a_usar.csv')

df = get_data()

# dashboard title
st.title("Dashboard Programas Internacionales ✈️")

# top-level filters
filtro_nivel = st.selectbox("Selecciona el Nivel", pd.unique(df["Nivel"]))
# dataframe filter
df = df[df["Nivel"] == filtro_nivel]

# ------------------------------------------------------------------------------------------------------------------------------------------
# PRIMEROS KPIS

# create three columns
kpi1, kpi2 = st.columns(2)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Estudiantes Asignados en su Op. 1️⃣ ",
    value=f"{(((df[df['PrimeraOp'] == 1]['PrimeraOp'].sum())/len(df['PrimeraOp']))*100).round(2)}%",
    # delta=round(avg_age) - 10,
)

kpi2.metric(
    label="Intercambios Totales 👤",
    value= f"{((df[df['TipoOportunidad'] == 'Intercambio']['TipoOportunidad'].count()/len(df['TipoOportunidad']))*100).round(2)}%",
    # delta=-10 + count_married,
)

# ------------------------------------------------------------------------------------------------------------------------------------------
# PRIMERAS DOS GRÁFICAS

# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### Solicitudes a través del Tiempo ⌛️")

    data = pd.DataFrame(df.groupby(['Año','TipoOportunidad'])['Matricula'].count())
    data.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Line(x= data[data['TipoOportunidad']=='Intercambio']['Año'], 
                            y= data[data['TipoOportunidad']=='Intercambio']['Matricula'],
                            line= dict(color='rgb(127,188,223)'),
                            name= 'Intercambio'))

    fig.add_trace(go.Line(x= data[data['TipoOportunidad']=='StudyAbroad']['Año'], 
                            y= data[data['TipoOportunidad']=='StudyAbroad']['Matricula'],
                            line= dict(color='rgb(0,102,204)'),
                            name= 'StudyAbroad'))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(0,102,204)',
            linewidth=2,
            ticks='outside'),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False)
    )

    fig.update_traces(mode="markers+lines", 
                        hovertemplate=None)

    fig.update_layout(
                    xaxis_title='Año',
                    yaxis_title='Cantidad',
                    )

    fig.update_layout(hovermode="x")
    # fig.show()

    st.write(fig)
   
with fig_col2:
    # top-level filters
    
    rango = pd.unique(df["Año"])
    filtro_nivel = st.slider("Selecciona el Año", int(rango.min()), int(rango.max()), int(rango.max()))
    # dataframe filter
    df2= df[df["Año"] == filtro_nivel]

    st.markdown("### Tipo de Intercambio 🗺")
    
    fig2 = go.Figure(data=[go.Pie(labels= df2['TipoOportunidad'].unique(),
                             values= df2['TipoOportunidad'].value_counts(),
                             hole=.3,
                             insidetextorientation='radial')]
                            )

    fig2.update_traces(textposition='inside', hoverinfo='label+value', textinfo='percent', 
                textfont_size=13, marker=dict(colors=['rgb(0,102,204)','rgb(8,48,107)'], 
                line=dict(color='rgb(0,102,204)')))

    # fig.update_layout(title = f'Tipo de Intercambio en {dropdown}')
    st.write(fig2)

# ------------------------------------------------------------------------------------------------------------------------------------------

# SEGUNDAS DOS GRÁFICAS

fig_col3, fig_col4 = st.columns(2)

# SUNBURST
with fig_col3:
    st.markdown("### Gráfica Sunburst")
    fig3 = px.sunburst(df, path=['TipoOportunidad','Escuela','Programa'], 
                    branchvalues='total',
                    # width=750, height=750,
                    color= df['Escuela'],
                    color_discrete_map={'StudyAbroad':'rgb(255,75,75)', 'Intercambio':'rgb(255,75,75)',
                    'Ingeniería y Ciencias':'rgb(0,69,138)', 'Negocios':'rgb(0,80,159)',
                    'Ciencias Sociales':'rgb(0,89,178)', 'Humanidades':'rgb(0,103,206)',
                    'Prepa Tec':'rgb(76,140,203)', 'Arquitectura':'rgb(77,150,223)', 
                    'Salud':'rgb(98,170,242)', 'No Aplica':'rgb(38,39,48'},
                    hover_name='TipoOportunidad')
    
    st.write(fig3)

# SANKEY
with fig_col4:
    st.markdown("### Gráfica Sankey")
    paises = df['Pais'].value_counts().where(df['Pais'].value_counts() > 3000).head(6)
    paises = pd.DataFrame(paises)
    val = list(paises.index)

    top_paises = df[df['Pais'].isin(val)] # nuevo dataframe

    fig4 = px.parallel_categories(top_paises,
                                dimensions = ['Escuela','Pais','TipoOportunidad'],
                                color = top_paises['NumPais'],
                                color_continuous_scale = px.colors.sequential.PuBu,
                                labels = {'Escuela':'Escuela', 'Pais':'Destino', 'TipoOportunidad':'Tipo Oportunidad'})

    # fig.update_layout(width=8000, height=1000)

    st.write(fig4)

# ------------------------------------------------------------------------------------------------------------------------------------------

st.write("Elaborado por Sofía Gutiérrez | A00827191")