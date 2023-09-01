import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
pd.options.plotting.backend = "plotly"
import base64

icon = Image.open('C:/Users/otavio.batini/Desktop/Commodities_Dashboard/NorteLogo2.jpg')


st.set_page_config(page_title="Commodities Dashboard",
                   page_icon=icon,
                   layout="wide",)


st.sidebar.title("**Commodities Dashboard**")

st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def build_markup_for_logo(
    png_file,
    background_position="50% 10%",
    margin_top="10%",
    image_width="60%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string,
        background_position,
        margin_top,
        image_width,
        image_height,
    )


def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

add_logo("C:/Users/otavio.batini/Desktop/Commodities_Dashboard/logo.png")

fig_col1, fig_col2 = st.columns(2)
#------------------------------------------------------------------------------------------

DFBASE = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/FullBaseDashboard.xlsx",
    engine='openpyxl',
    sheet_name='Base',
    skiprows=7,
    usecols='C:BZ',
    nrows=7000,
)

#-------------------------------------------------------------------------------------------

figIOPRICES = px.line(DFBASE,
    x='Tempo1',y=['65% Fe','62% Fe','58% Fe'],
    title='Iron Ore Prices',
    )
figIOPRICES.update_layout(
    xaxis_title= "",
    yaxis_title= "",
    legend_title="",
)
#figIOPRICES.add_vline(x='2023', line_width=1, line_color="gray")

#-------------------------------------------------------------------------------------------







with fig_col1:
    st.write(figIOPRICES)