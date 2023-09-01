import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
pd.options.plotting.backend = "plotly"

icon = Image.open('C:/Users/otavio.batini/Desktop/Commodities_Dashboard/NorteLogo2.jpg')
icon2 = Image.open('C:/Users/otavio.batini/Desktop/Commodities_Dashboard/NorteLogo.jpg')


st.set_page_config(page_title="Commodities Dashboard",
                   page_icon=icon,
                   layout="wide",)

st.sidebar.image(icon2, width=300)
st.sidebar.title("**Dashboard**")

DefaultColors=['rgb(78, 103, 200)', 'rgb(94, 204, 243)','rgb(167, 234, 82)', 'rgb(217, 217, 217)']
########################################################################################################

MonthDate = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/Performance_Aço_Mensal.xlsx",
    engine='openpyxl',
    sheet_name='DataToDashboard',
    skiprows=3,
    usecols='C',
    nrows=126,
)

#
DFSP = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/Performance_Aço_Mensal.xlsx",
    engine='openpyxl',
    sheet_name='DataToDashboard',
    skiprows=3,
    usecols='C:F',
    nrows=126,
)
figDFSP = px.bar(DFSP,
    x='Month',y=['Crude Steel (kt)','Laminados (kt)','Semiacabados (kt)'],
    title='Brazil Steel Production (kt)',
    barmode='stack',
    )
figDFSP.update_layout(
    yaxis_title= "Volumes Produced (kt)",
    legend_title="",
)

#
DFFT = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/Performance_Aço_Mensal.xlsx",
    engine='openpyxl',
    sheet_name='DataToDashboard',
    skiprows=3,
    usecols=['Exports (000t)','Imports (000t)','Month'],
    nrows=126,
)
figDFFT = px.line(DFFT,
                  x='Month',y=['Exports (000t)','Imports (000t)'],
                  title='Foreign Trade - Brazilian Steel'
                  )
figDFFT.update_layout(
    yaxis_title= "Volumes Traded (kt)",
    legend_title="",
)
#
DFSS = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/Performance_Aço_Mensal.xlsx",
    engine='openpyxl',
    sheet_name='DataToDashboard',
    skiprows=3,
    usecols=['Domestic Sales','Foreign Market','Month'],
    nrows=126,
)
figDFSS = px.bar(DFSS,
    x='Month',y=['Domestic Sales','Foreign Market'],
    title='Brazil Steel Sales (kt)',
    barmode='stack',
    )
figDFSS.update_layout(
    yaxis_title= "Volumes Sold (kt)",
    legend_title="",
)
#
DFAVGT = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/Performance_Aço_Mensal.xlsx",
    engine='openpyxl',
    sheet_name='DataToDashboard',
    skiprows=3,
    usecols=['Exports Avg. Ticket','Imports Avg. Ticket','Month'],
    nrows=126,
)
figDFAVGT = px.bar(DFAVGT,
                  x='Month',y=['Exports Avg. Ticket','Imports Avg. Ticket'],
                  title='Average Ticket (Foreign Trade)'
                  )
figDFAVGT.update_layout(
    yaxis_title= "Volumes/Revenues",
    legend_title="",
)
#
DFEXPBR = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/Performance_Aço_Mensal.xlsx",
    engine='openpyxl',
    sheet_name='DataToDashboard',
    skiprows=3,
    usecols=['Exports (000t)','Month','Percentage of Production'],
    nrows=126,
)
figDFEXPBR = make_subplots(specs=[[{"secondary_y": True}]])
figDFEXPBR.add_trace(go.Bar(
                  x=DFEXPBR['Month'],y=DFEXPBR['Exports (000t)'],
                  name='Exports (kt)'),
                  secondary_y=False,
                  )
figDFEXPBR.add_scatter(x=DFEXPBR['Month'],y=DFEXPBR['Percentage of Production'],
                       name='Percentage of Production',
                       secondary_y=True,)
figDFEXPBR.update_layout(
    title_text='Brazil Steel Exports (kt)',
    yaxis_title= "Volumes Exported (kt)",
    legend_title="",
)
#




####################################################################################################


st.sidebar.header("Commodities Dashboard")
fig_col1, fig_col2 = st.columns(2)


category = st.sidebar.selectbox('Select Category', ("Home","Brazil Steel Industry","China Real Estate"))


if category == "Home":
    with fig_col1:
        st.header(':blue[**Commodities Dashboard**]')






if category == "Brazil Steel Industry":
    selected = st.sidebar.selectbox('Select Statistics', ("General Panel","Steel Production","Foreign Trade"), index=st.session_state['selection'])
    if selected == "Steel Production":
        st.write(selected)
        st.plotly_chart(figDFSP)
    if selected == "Foreign Trade":
        st.write(selected)
        st.plotly_chart(figDFFT)
    if selected == "General Panel":
        with fig_col1:
            st.plotly_chart(figDFSP)
            st.plotly_chart(figDFSS)
            st.plotly_chart(figDFEXPBR)
        with fig_col2:     
            st.plotly_chart(figDFFT)
            st.plotly_chart(figDFAVGT)






    # Use widgets' returned values in variables
##>>> for i in range(int(st.number_input('Num:'))): foo()
##>>> if st.sidebar.selectbox('I:',['f']) == 'f': b()
##>>> my_slider_val = st.slider('Quinn Mallory', 1, 88)
##>>> st.write(slider_val)