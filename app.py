import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SST-MCON",
    page_icon="🦺",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
:root{
    --fondo:#07111f;
    --panel:#101c2d;
    --borde:#263850;
    --texto:#f4f7fb;
    --sec:#c7d0dc;
    --azul:#1f8cff;
    --naranja:#ff7a21;
}
html,body,.stApp,[data-testid="stAppViewContainer"]{
    background:var(--fondo)!important;
    color:var(--texto)!important;
}
header[data-testid="stHeader"]{
    display:block!important;
    visibility:visible!important;
    height:3.25rem!important;
    background:transparent!important;
}

[data-testid="stToolbar"]{
    background:transparent!important;
}

#MainMenu, footer{
    visibility:hidden!important;
}

/* Botones nativos para cerrar y volver a abrir la barra lateral */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"]{
    display:flex!important;
    visibility:visible!important;
    opacity:1!important;
    z-index:9999999!important;
}

[data-testid="stSidebarCollapsedControl"]{
    position:fixed!important;
    top:0.55rem!important;
    left:0.55rem!important;
}

[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarCollapsedControl"] [data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebarCollapseButton"] [data-testid="stBaseButton-headerNoPadding"]{
    display:flex!important;
    visibility:visible!important;
    opacity:1!important;
    background:#ff7a21!important;
    color:white!important;
    border:1px solid #ff9a5a!important;
    border-radius:8px!important;
    min-width:2.35rem!important;
    min-height:2.35rem!important;
}

[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg{
    color:white!important;
    fill:white!important;
    stroke:white!important;
}
.block-container{
    padding-top:1rem!important;
    padding-left:1.2rem!important;
    padding-right:1.2rem!important;
}
[data-testid="stSidebar"]{
    background:#0b1727!important;
    border-right:1px solid var(--borde);
}
[data-testid="stSidebar"] *{
    color:#f3f6fa!important;
    opacity:1!important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span{
    color:#eef3f8!important;
    font-weight:600!important;
}
div[role="radiogroup"] label{
    padding:8px 10px!important;
    border-radius:8px!important;
}
div[role="radiogroup"] label:hover{background:#15253a!important;}
div[data-baseweb="select"]>div{
    background:#111d2d!important;
    border:1px solid #30445f!important;
    color:white!important;
}
div[data-baseweb="select"] span{color:white!important;}
.encabezado{
    background:#0b1727;
    border:1px solid var(--borde);
    border-left:6px solid var(--naranja);
    border-radius:10px;
    padding:18px 22px;
    margin-bottom:18px;
}
.encabezado h1{
    margin:0;
    color:white;
    font-size:30px;
    font-weight:800;
}
.encabezado p{
    margin:6px 0 0;
    color:var(--sec);
}
.card{
    background:var(--panel);
    border:1px solid var(--borde);
    border-radius:12px;
    padding:18px;
    text-align:center;
    min-height:110px;
    display:flex;
    flex-direction:column;
    justify-content:center;
}
.card h2{margin:0;color:white;font-size:30px;}
.card p{margin:10px 0 0;color:#d6deea;font-weight:700;}
div[data-testid="stVerticalBlockBorderWrapper"]{
    background:var(--panel);
    border:1px solid var(--borde);
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def crear_datos():
    np.random.seed(26)
    n = 400

    reportes = pd.DataFrame({
        "Código":[f"INC-{i+1:04d}" for i in range(n)],
        "Fecha":pd.to_datetime(np.random.choice(pd.date_range("2026-01-01","2026-05-31"),n)),
        "Sede":np.random.choice(["Línea 2 Metro","Antamina","Marcona","Aeropuerto","Puerto Paita"],n),
        "Área":np.random.choice(["Operaciones","Mantenimiento","Almacén","Túneles"],n),
        "Tipo":np.random.choice(["Condición insegura","Acto subestándar","Equipo defectuoso","Riesgo ambiental"],n),
        "Criticidad":np.random.choice(["Alto","Medio","Bajo"],n,p=[.20,.45,.35]),
        "Estado":np.random.choice(["Nuevo","Validando","En acción","Completado","Rechazado"],n,p=[.12,.18,.25,.40,.05]),
        "Tiempo respuesta":np.round(np.random.uniform(1,10,n),2)
    })

    trabajadores = pd.DataFrame({
        "Trabajador":[f"TRAB-{i+1:03d}" for i in range(90)],
        "Estado médico":np.random.choice(["Apto","No Apto","Apto con restricciones"],90,p=[.68,.12,.20]),
        "Sede":np.random.choice(reportes["Sede"].unique(),90)
    })

    epp = pd.DataFrame({
        "EPP":np.random.choice(["Casco","Guantes","Arnés","Lentes","Respirador"],120),
        "Estado":np.random.choice(["Vigente","Por renovar","Vencido","Stock crítico"],120,p=[.55,.20,.15,.10]),
        "Sede":np.random.choice(reportes["Sede"].unique(),120)
    })

    simulacros = pd.DataFrame({
        "Sede":["Línea 2 Metro","Antamina","Marcona","Aeropuerto","Puerto Paita"],
        "Tiempo objetivo":[6,7,8,6,7],
        "Tiempo real":[5.8,8.4,7.5,6.9,9.1]
    })
    simulacros["Resultado"] = np.where(
        simulacros["Tiempo real"] <= simulacros["Tiempo objetivo"],
        "Aprobado","Deficiente"
    )
    return reportes, trabajadores, epp, simulacros

reportes, trabajadores, epp, simulacros = crear_datos()

with st.sidebar:
    st.markdown("## 🦺 SST-MCON")
    modulo = st.radio("Módulo",[
        "Resumen Ejecutivo",
        "Seguridad Operacional",
        "Salud Ocupacional",
        "Gestión EPP",
        "Emergencias"
    ])
    st.divider()
    sede = st.selectbox("Sede",["Todas"]+sorted(reportes["Sede"].unique()))
    criticidad = st.selectbox("Criticidad",["Todas","Alto","Medio","Bajo"])

df = reportes.copy()
if sede != "Todas":
    df = df[df["Sede"] == sede]
if criticidad != "Todas":
    df = df[df["Criticidad"] == criticidad]

def tarjeta(valor,titulo):
    st.markdown(
        f"<div class='card'><h2>{valor}</h2><p>{titulo}</p></div>",
        unsafe_allow_html=True
    )

def estilo(fig,alto=310):
    fig.update_layout(
        height=alto,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f4f7fb"),
        title_font=dict(color="white",size=17),
        title_x=0.01,
        legend=dict(title_text="",font=dict(color="#eef3f8")),
        margin=dict(l=10,r=10,t=48,b=10)
    )
    fig.update_xaxes(
        tickfont=dict(color="#dce4ee"),
        title_font=dict(color="#dce4ee"),
        gridcolor="rgba(220,228,238,.20)",
        linecolor="#7f8fa3"
    )
    fig.update_yaxes(
        tickfont=dict(color="#dce4ee"),
        title_font=dict(color="#dce4ee"),
        gridcolor="rgba(220,228,238,.20)",
        linecolor="#7f8fa3"
    )
    return fig

st.markdown("""
<div class="encabezado">
    <h1>DASHBOARD EJECUTIVO SST - MCON</h1>
    <p>Gestión Integral de Seguridad y Salud en el Trabajo · Versión corregida</p>
</div>
""", unsafe_allow_html=True)

if modulo == "Resumen Ejecutivo":
    total = len(df)
    altos = len(df[(df["Criticidad"]=="Alto") & (df["Estado"]!="Completado")])
    tiempo = df["Tiempo respuesta"].mean() if total else 0
    no_aptos = (trabajadores["Estado médico"]=="No Apto").sum()
    alertas_epp = epp["Estado"].isin(["Vencido","Stock crítico"]).sum()

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: tarjeta(total,"REPORTES")
    with c2: tarjeta(altos,"RIESGOS ALTOS")
    with c3: tarjeta(f"{tiempo:.1f} h","TIEMPO RESPUESTA")
    with c4: tarjeta(no_aptos,"NO APTOS")
    with c5: tarjeta(alertas_epp,"ALERTAS EPP")

    a,b,c = st.columns(3)

    with a:
        x = df["Sede"].value_counts().reset_index()
        x.columns = ["Sede","Reportes"]
        fig = px.bar(
            x,x="Reportes",y="Sede",orientation="h",
            title="Reportes por sede",
            color_discrete_sequence=["#1768e5"]
        )
        st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})

    with b:
        x = df["Criticidad"].value_counts().reset_index()
        x.columns = ["Criticidad","Reportes"]
        fig = px.pie(
            x,names="Criticidad",values="Reportes",hole=.55,
            title="Reportes por criticidad",color="Criticidad",
            color_discrete_map={"Alto":"#f47a2a","Medio":"#1f8cff","Bajo":"#182a96"}
        )
        st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})

    with c:
        x = df.assign(Mes=df["Fecha"].dt.to_period("M").astype(str))
        x = x.groupby("Mes").size().reset_index(name="Reportes")
        fig = px.line(x,x="Mes",y="Reportes",markers=True,title="Evolución mensual")
        fig.update_traces(line_color="#1f8cff")
        st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})

    a,b = st.columns(2)

    with a:
        x = df["Estado"].value_counts().reset_index()
        x.columns = ["Estado","Reportes"]
        fig = px.bar(
            x,x="Estado",y="Reportes",
            title="Estado de los reportes",
            color_discrete_sequence=["#1f8cff"]
        )
        fig.update_layout(title_text="Estado de los reportes",legend_title_text="")
        st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})

    with b:
        cumplimiento = 100 - altos / max(total,1) * 100
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=cumplimiento,
            number={"suffix":"%","font":{"color":"white"}},
            title={"text":"Cumplimiento SST","font":{"color":"white"}},
            gauge={
                "axis":{"range":[0,100],"tickcolor":"white"},
                "bar":{"color":"#1768e5"},
                "threshold":{"line":{"color":"#f47a2a","width":4},"value":90}
            }
        ))
        st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})

elif modulo == "Seguridad Operacional":
    st.subheader("Reportes de peligro")
    st.dataframe(df.sort_values("Fecha",ascending=False),use_container_width=True)
    st.download_button(
        "Descargar reportes",
        df.to_csv(index=False).encode("utf-8"),
        "reportes_sst.csv",
        "text/csv"
    )

elif modulo == "Salud Ocupacional":
    st.subheader("Estado médico ocupacional")
    tabla = trabajadores.copy()
    if sede != "Todas":
        tabla = tabla[tabla["Sede"] == sede]

    x = tabla["Estado médico"].value_counts().reset_index()
    x.columns = ["Estado","Trabajadores"]
    fig = px.pie(
        x,names="Estado",values="Trabajadores",hole=.5,
        title="Trabajadores por estado médico",
        color_discrete_sequence=["#1f8cff","#f47a2a","#182a96"]
    )
    st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})
    st.dataframe(tabla,use_container_width=True)

elif modulo == "Gestión EPP":
    st.subheader("Control de EPP")
    tabla = epp.copy()
    if sede != "Todas":
        tabla = tabla[tabla["Sede"] == sede]

    x = tabla["Estado"].value_counts().reset_index()
    x.columns = ["Estado","Cantidad"]
    fig = px.bar(
        x,x="Estado",y="Cantidad",color="Estado",
        title="Vigencia y stock de EPP"
    )
    st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})
    st.dataframe(tabla,use_container_width=True)

else:
    st.subheader("Simulacros y emergencias")
    tabla = simulacros.copy()
    if sede != "Todas":
        tabla = tabla[tabla["Sede"] == sede]

    fig = px.bar(
        tabla,x="Sede",y=["Tiempo objetivo","Tiempo real"],
        barmode="group",title="Tiempo objetivo vs. tiempo real"
    )
    st.plotly_chart(estilo(fig),use_container_width=True,config={"displayModeBar":False})
    st.dataframe(tabla,use_container_width=True)
