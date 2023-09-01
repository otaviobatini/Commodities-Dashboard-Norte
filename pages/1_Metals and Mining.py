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


st.set_page_config(page_title="Metals and Mining",
                   page_icon=icon,
                   layout="wide",)


st.sidebar.title("**Metals and Mining**")

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

colorpallete = ["dodgerblue","midnightblue","paleturquoise","lightgray","darkseagreen","yellow","lightsteelblue"]
#------------------------------------------------------------------------------------------

DFBASE = pd.read_excel(
    io="C:/Users/otavio.batini/Desktop/Commodities_Dashboard/FullBaseDashboard.xlsx",
    engine='openpyxl',
    sheet_name='Base',
    skiprows=7,
    usecols='C:FN',
    nrows=7000,
)

#-------------------------------------------------------------------------------------------

figIOPRICES = px.line(DFBASE,
    x='Tempo1',y=['65% Fe','62% Fe','58% Fe'],
    color_discrete_sequence=colorpallete,
    title='Iron Ore Prices',
    )
figIOPRICES.update_layout(
    xaxis_title= "",
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figSTEELPRICES = px.line(DFBASE,
    x='Tempo2',y=['Long Rebar Domestic','Flat HRC Domestic','Flat HRC Export','Scrap'],
    color_discrete_sequence=colorpallete,
    title='Steel Prices',
    )
figSTEELPRICES.update_layout(
    xaxis_title= "",
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figSTEELPRODUCTION = px.area(DFBASE,
    x='Tempo5',y='Crude Steel Production (10-day Avg Mt/Day)',
    color_discrete_sequence=['dodgerblue'],
    title='Crude Steel Production 10-day avg Mt/Day(CISA)',
    )
figSTEELPRODUCTION.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    yaxis_range=[1.4,2.5],
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figSTEELINVENTORY = px.line(DFBASE,
    x='Tempo5',y='Inventory of Steel Products',
    color_discrete_sequence=['dodgerblue'],
    title='Chinese Inventory of Steel Products (Mt)',
    )
figSTEELINVENTORY.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    yaxis_range=[6,22],
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figIODEMAND = px.line(DFBASE,
    x='Tempo4',y=['Iron Ore Weekly Demand','Iron Ore Weekly Imports'],
    color_discrete_sequence=colorpallete,
    title='Chinese Iron Ore Weekly Demand',
    )
figIODEMAND.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figSTEELPRODXDEMAND = make_subplots(specs=[[{"secondary_y": True}]])
figSTEELPRODXDEMAND.add_trace(go.Line(
                  x=DFBASE['Tempo6'],y=DFBASE['Production (WSA)'],
                  name='Production(WSA)',
                  marker_color='midnightblue'),
                  secondary_y=False,
                  )
figSTEELPRODXDEMAND.add_trace(go.Line(
                  x=DFBASE['Tempo6'],y=DFBASE['Apparent Demand'],
                  name='Apparent Demand',
                  marker_color='dodgerblue'),
                  secondary_y=False,
                  )
figSTEELPRODXDEMAND.add_trace(go.Bar(x=DFBASE['Tempo6'],y=DFBASE['DeltaDemand'], 
                       marker_color="lightgray",
                       name='Gap'),
                       secondary_y=True,
                       )
figSTEELPRODXDEMAND.update_layout(
    title_text='China Steel Production and Apparent Demand',
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
    #xaxis_range=['2022-08-01','2023-08-01']
)
figSTEELPRODXDEMAND.update_yaxes(range=[-3000, 30000], secondary_y=True)

figSTEELTRADE = make_subplots(specs=[[{"secondary_y": True}]])
figSTEELTRADE.add_trace(go.Line(
                  x=DFBASE['Tempo6'],y=DFBASE['Imports'],
                  name='Imports',
                  marker_color='midnightblue'),
                  secondary_y=False,
                  )
figSTEELTRADE.add_trace(go.Line(
                  x=DFBASE['Tempo6'],y=DFBASE['Exports'],
                  name='Exports',
                  marker_color='dodgerblue'),
                  secondary_y=False,
                  )
figSTEELTRADE.add_trace(go.Bar(x=DFBASE['Tempo6'],y=DFBASE['Net Exports'], 
                       marker_color="lightgray",
                       name='Net Exports'),
                       secondary_y=False,
                       )
figSTEELTRADE.update_layout(
    title_text='China Steel Foreign Trade',
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figSTEELPRODTOTAL = make_subplots(specs=[[{"secondary_y": True}]])
figSTEELPRODTOTAL.add_trace(go.Bar(
                  x=DFBASE['Tempo6'],y=DFBASE['Production (WSA)'],
                  marker_color="lightgray",
                  name='Production(WSA)'),
                  secondary_y=False,
                  )
figSTEELPRODTOTAL.add_trace(go.Line(
                  x=DFBASE['Tempo6'],y=DFBASE['YoY Production'],
                  marker_color="dodgerblue",
                  name='YoY (%)'),
                  secondary_y=True,
                  )
figSTEELPRODTOTAL.update_layout(
    title_text='China Steel Production WSA',
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
    #xaxis_range=['2022-08-01','2023-08-01']
)
figSTEELPRODTOTAL.update_yaxes(range=[0, 100000], secondary_y=False)
figSTEELPRODTOTAL.update_yaxes(range=[-0.2, 0.4], secondary_y=True)

figINVENTORYCOUNTRIES = px.area(DFBASE,
                                x='Tempo8',
                                y=['Australia (kt)','Brazil (kt)','Others (kt)'],
                                color_discrete_sequence=colorpallete,
                                title= 'Chinese Iron Ore Inventories By Country',
)
figINVENTORYCOUNTRIES.update_layout(
    title_text='Chinese Iron Ore Inventories By Country',
    yaxis_title= "",
    xaxis_title='',
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figINVENTORYPRODUCTS = px.area(DFBASE,
                                x='Tempo8',
                                y=['Fines','Pellet','Concentrate','Lump'],
                                color_discrete_sequence=colorpallete,
                                title= 'Chinese Iron Ore Inventories By product',
)
figINVENTORYPRODUCTS.update_layout(
    title_text='Chinese Iron Ore Inventories By Product',
    yaxis_title="",
    xaxis_title='',
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
)

figIOSHIPBR = px.area(DFBASE,
                                x='Tempo3',
                                y=['Ponta Da madeira','Tubarao','Guaiba Island Terminal','CSN Terminal','CPBS','Ferroport Terminal','Porto Sudeste'],
                                color_discrete_sequence=colorpallete,
                                title= 'Brazilian Iron Ore Shipments by Port',
)
figIOSHIPBR.update_layout(
    title_text='Brazilian Iron Ore Shipments by Port',
    yaxis_title="",
    xaxis_title='',
    legend_title="",
)

figSTEELSCRAP = make_subplots(specs=[[{"secondary_y": True}]])
figSTEELSCRAP.add_trace(go.Bar(
                  x=DFBASE['Tempo9'],y=DFBASE['Daily consumption (t)'],
                  marker_color="lightgray",
                  name='Daily Consumpton (t)'),
                  secondary_y=False,
                  )
figSTEELSCRAP.add_trace(go.Line(
                  x=DFBASE['Tempo9'],y=DFBASE['y/y'],
                  marker_color="dodgerblue",
                  name='YoY (%)'),
                  secondary_y=True,
                  )
figSTEELSCRAP.update_layout(
    title_text='Chinese Daily Steel Scrap Consumption',
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.3)
    #xaxis_range=['2022-08-01','2023-08-01']
)
figSTEELSCRAP.update_yaxes(range=[0, 5000], secondary_y=False)
figSTEELSCRAP.update_yaxes(range=[-0.6, 0.8], secondary_y=True)

figFOBBR = make_subplots(specs=[[{"secondary_y": True}]])
figFOBBR.add_trace(go.Line(
                  x=DFBASE['Tempo10'],y=DFBASE['IODEX 65% Fe'],
                  name='IO 65%',
                  marker_color="midnightblue"),
                  secondary_y=False,
                  )
figFOBBR.add_trace(go.Line(
                  x=DFBASE['Tempo10'],y=DFBASE['Implied FOB Price Brazil'],
                  name='Implied FOB Price Brazil',
                  marker_color='dodgerblue'),
                  secondary_y=False,
                  )
figFOBBR.add_trace(go.Bar(
                  x=DFBASE['Tempo10'],y=DFBASE['Freight Bz-Ch'],
                  name='Freight Bz-Ch',
                  marker_color='lightgray'),
                  secondary_y=True,
                  )
figFOBBR.update_layout(
    title_text='Implied FOB Brazil',
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0.2),
    #xaxis_range=['2022-08-01','2023-09-01']
)
figFOBBR.update_yaxes(range=[0, 260], secondary_y=False)
figFOBBR.update_yaxes(range=[0, 200], secondary_y=True)

figVALEFOB = make_subplots(specs=[[{"secondary_y": True}]])
figVALEFOB.add_trace(go.Line(
                  x=DFBASE['Tempo10'],y=DFBASE['VALE Share Price 100'],
                  name='Vale Share Price',
                  marker_color='midnightblue'),
                  secondary_y=False,
                  )
figVALEFOB.add_trace(go.Line(
                  x=DFBASE['Tempo10'],y=DFBASE['Vale/FOB IO 100'],
                  name='Vale / FOB IO',
                  marker_color='dodgerblue'),
                  secondary_y=False,
                  )
figVALEFOB.add_trace(go.Line(
                  x=DFBASE['Tempo10'],y=DFBASE['IO 65% 100'],
                  name='IO 65%',
                  marker_color='paleturquoise'),
                  secondary_y=False,
                  )
figVALEFOB.add_trace(go.Line(
                  x=DFBASE['Tempo10'],y=DFBASE['FOB Brazil 100'],
                  name='FOB Brazil',
                  marker_color='lightgray'),
                  secondary_y=False,
                  )
figVALEFOB.update_layout(
    title_text='Vale / FOB IO - Base 100',
    yaxis_title= "",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0),
    #xaxis_range=['2022-08-01','2023-09-01']
)
figVALEFOB.update_yaxes(range=[0, 800], secondary_y=False)
figVALEFOB.update_yaxes(range=[-400, 3000], secondary_y=True)

figCISA = px.line(DFBASE,
    x='TempoCISA',y=['CISA 2018','CISA 2019','CISA 2020','CISA 2021','CISA 2022'],
    color_discrete_sequence=colorpallete,
    title='Crude Steel Production (10-day Avg Mt/Day)',
    )
figCISA.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)
figCISA.update_traces(line={'width': 3})
figCISA.add_trace(go.Line(x=DFBASE['TempoCISA'],y=DFBASE['CISA 2023'],
                                  marker_color='crimson',name='CISA 2023',
                                  line = dict(width= 5)))

figINVANUAL = px.line(DFBASE,
    x='TempoCISA',y=['Inv. 2018','Inv. 2019','Inv. 2020','Inv. 2021','Inv. 2022'],
    color_discrete_sequence=colorpallete,
    title='Chinese Steel Products Inventories (Mt)',
    )
figINVANUAL.update_traces(line={'width': 3})
figINVANUAL.add_trace(go.Line(x=DFBASE['TempoCISA'],y=DFBASE['Inv. 2023'],
                                  marker_color='crimson',name='Inv. 2023',
                                  line = dict(width= 5)))
figINVANUAL.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)


figDOMESTICPRICESBRL = px.line(DFBASE,
    x='Tempo11',y=['HRC Domestic Price','CRC Domestic Price','Rebar Domestic Price','Wire Rod Domestic Price'],
    color_discrete_sequence=colorpallete,
    title='Brazilian Domestic Steel Prices (BRL/t)',
    )
figDOMESTICPRICESBRL.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figDOMESTICPRICESUSD = px.line(DFBASE,
    x='Tempo11',y=['HRC Domestic Price USD','Rebar Domestic Price USD'],
    color_discrete_sequence=colorpallete,
    title='Brazilian Domestic Steel Prices (USD/t)',
    )
figDOMESTICPRICESUSD.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figEXPORTPRICES = px.line(DFBASE,
    x='Tempo11',y=['HRC Export Price BRL','CRC Export Price BRL'],
    color_discrete_sequence=colorpallete,
    title='Brazilian Export Steel Prices',
    )
figEXPORTPRICES.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSPREAD = px.line(DFBASE,
    x='Tempo11',y=['Spread HRC','Spread CRC'],
    color_discrete_sequence=colorpallete,
    title='Brazilian Steel Trade Prices: Domestic Px - Export Px',
    )
figBRSPREAD.update_layout(
    xaxis_title= "",
    yaxis_title="Domestic Px - Export Px (BRL)",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)



figIOSTOCK = make_subplots(specs=[[{"secondary_y": True}]])
figIOSTOCK.add_trace(go.Line(
                  x=DFBASE['Tempo12'],y=DFBASE['Total Imported Stock of Sintered Fines'],
                  name='Total Imported Stock of Sintered Fines',
                  marker_color='dodgerblue'),
                  secondary_y=False,
                  )
figIOSTOCK.add_trace(go.Line(
                  x=DFBASE['Tempo12'],y=DFBASE['Daily Consumption'],
                  name='Daily Consumption',
                  marker_color='midnightblue'),
                  secondary_y=True,
                  )
figIOSTOCK.add_trace(go.Bar(
                  x=DFBASE['Tempo12'],y=DFBASE['Stock in Days'],
                  name='Stock in Days',
                  marker_color='lightgray'),
                  secondary_y=True,
                  )
figIOSTOCK.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    title='Imported Stock of Sintered Fines at Mills (kt)',
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)
figIOSTOCK.update_yaxes(range=[0, 300], secondary_y=True)

figTRADERSINV = px.area(DFBASE,
                        x='Tempo13',y=['Long Steels Inventories','Flat Steels Inventories'],
                        color_discrete_sequence=colorpallete,
                        title='Chinese cities (traders) steel inventories Mt'
                        )
figTRADERSINV.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figMILLSINV = px.area(DFBASE,
                      x='Tempo14',
                      y=['Long Steels Mills Inventories','Flat Steels Mills Inventories'],
                      color_discrete_sequence=colorpallete,
                      title='Chinese Mills Steel Inventories Mt')
figMILLSINV.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figTRADERSINVANUAL = px.line(DFBASE,
                           x='TempoMills',
                           y=['TI 2018','TI 2019','TI 2020','TI 2021','TI 2022'],
                           color_discrete_sequence=colorpallete,
                           title='Chinese Steel Inventories at Traders - Anual (mt)')
figTRADERSINVANUAL.add_trace(go.Line(x=DFBASE['TempoMills'],y=DFBASE['TI 2023'],
                                     name='TI 2023',
                                     marker_color='crimson',
                                     line = dict(width= 5)))
figTRADERSINVANUAL.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figMILLSINVANUAL = px.line(DFBASE,
                           x='TempoMills',
                           y=['MI 2018','MI 2019','MI 2020','MI 2021','MI 2022'],
                           color_discrete_sequence=colorpallete,
                           title='Chinese Steel Inventories at Steel Mills - Anual (mt)')
figMILLSINVANUAL.add_trace(go.Line(x=DFBASE['TempoMills'],y=DFBASE['MI 2023'],
                                     name='MI 2023',
                                     marker_color='crimson',
                                     line = dict(width= 5)))
figMILLSINVANUAL.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figMILLSUTILIZATION = px.area(DFBASE,
                              x='Tempo15',
                              y='Tangshan Mills utilization Rate',
                              color_discrete_sequence=colorpallete,
                              title='Tangshan Mills Utilization')
figMILLSUTILIZATION.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBFCAPACITY = px.area(DFBASE,
                        x='Tempo16',
                        y='BF Capacity Utilization',
                        color_discrete_sequence=colorpallete,
                        title='Chinese Blast Furnaces Capacity Utilization')
figBFCAPACITY.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figMILLSPROFIT = px.area(DFBASE,
                         x='Tempo16',
                         y='Profitable Steel Mills',
                         color_discrete_sequence=colorpallete,
                         title='China % of Profitable Steel Mills')
figMILLSPROFIT.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figIOSTOCKANUAL = px.line(DFBASE,
                          x='tempoIOANUAL',
                          y=['SF 2018','SF 2019','SF 2020','SF 2021','SF 2022'],
                          color_discrete_sequence=colorpallete,
                          title='')
figIOSTOCKANUAL.add_trace(go.Line(x=DFBASE['tempoIOANUAL'],y=DFBASE['SF 2023'],
                                  marker_color='crimson',name='SF 2023',
                                  line = dict(width= 5)))
figIOSTOCKANUAL.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)



figBRIOEXP = make_subplots(specs=[[{"secondary_y": True}]])
figBRIOEXP.add_trace(go.Line(
                  x=DFBASE['Tempo16'],y=DFBASE['Iron Ore Exports (Kt) '],
                  name='Iron Ore Exports (Kt)'),
                  secondary_y=False,
                  )
figBRIOEXP.add_trace(go.Bar(
                  x=DFBASE['Tempo16'],y=DFBASE['Exports per day'],
                  name='Exports per Day'),
                  secondary_y=True,
                  )
figBRIOEXP.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    title='Brazil Iron Ore Exports (Kt)',
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)
figBRIOEXP.update_yaxes(range=[0, 10000], secondary_y=True)

figBRIOEXPPX = make_subplots(specs=[[{"secondary_y": True}]])
figBRIOEXPPX.add_trace(go.Line(
                  x=DFBASE['Tempo16'],y=DFBASE['Iron Ore Exports (US$ MM)'],
                  name='Iron Ore Exports (US$ MM)'),
                  secondary_y=False,
                  )
figBRIOEXPPX.add_trace(go.Bar(
                  x=DFBASE['Tempo16'],y=DFBASE['Avg. Weekly Price $/t'],
                  name='Avg. Weekly Price $/t'),
                  secondary_y=True,
                  )
figBRIOEXPPX.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    title='Brazil Iron Ore Exports Px (U$)',
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)
figBRIOEXPPX.update_yaxes(range=[0, 500], secondary_y=True)

figBRSTEELPROD = px.area(DFBASE,
                        x='Tempo17',
                        y=['Crude Steel (kt)','Laminados (kt)','Semiacabados (kt)'],
                        color_discrete_sequence=colorpallete,
                        title='Brazilian Steel Production (kt)')
figBRSTEELPROD.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSTEELSALES = px.area(DFBASE,
                        x='Tempo17',
                        y=['Domestic Sales','Foreign Trade'],
                        color_discrete_sequence=colorpallete,
                        title='Brazilian Steel Sales (kt)')
figBRSTEELSALES.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSTEELTRADE = make_subplots(specs=[[{"secondary_y": True}]])
figBRSTEELTRADE.add_trace(go.Line(
                  x=DFBASE['Tempo17'],y=DFBASE['Brazil Steel Exports (kt)'],
                  name='BR Steel Exports (kt)'),
                  secondary_y=False,
                  )
figBRSTEELTRADE.add_trace(go.Line(
                  x=DFBASE['Tempo17'],y=DFBASE['Brazil Steel Imports (kt)'],
                  name='BR Steel Imports (kt)'),
                  secondary_y=False,
                  )
figBRSTEELTRADE.add_trace(go.Bar(
                  x=DFBASE['Tempo17'],y=DFBASE['Brazil Steel Net Exports (kt)'],
                  name='Net Exports',
                  marker_color='lightsteelblue'),
                  secondary_y=False,
                  )
figBRSTEELTRADE.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    title='Brazil Steel Trade Volumes - Exports and imports (kt)',
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRTRADEPX = px.line(DFBASE,
                       x='Tempo17',
                       y=['BR Steel Exports Avg. Price','BR Steel Imports Avg. Price'],
                       color_discrete_sequence=colorpallete,
                       title='Brazil Steel Exports and Imports Average price (U$/t)')
figBRTRADEPX.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSTEELEXP = make_subplots(specs=[[{"secondary_y": True}]])
figBRSTEELEXP.add_trace(go.Line(
                  x=DFBASE['Tempo17'],y=DFBASE['Brazil Steel Exports (kt)'],
                  name='BR Steel Exports (kt)'),
                  secondary_y=False,
                  )
figBRSTEELEXP.add_trace(go.Line(
                  x=DFBASE['Tempo17'],y=DFBASE['Exp. % of Production'],
                  name='As a % of Production'),
                  secondary_y=True,
                  )
figBRSTEELEXP.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    title='Brazil Steel Exports and % of Production',
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSTEELIMP = make_subplots(specs=[[{"secondary_y": True}]])
figBRSTEELIMP.add_trace(go.Line(
                  x=DFBASE['Tempo17'],y=DFBASE['Brazil Steel Imports (kt)'],
                  name='BR Steel Imports (kt)'),
                  secondary_y=False,
                  )
figBRSTEELIMP.add_trace(go.Line(
                  x=DFBASE['Tempo17'],y=DFBASE['Imp. % of Apparent Consumption'],
                  name='As a % of Apparent Consumption'),
                  secondary_y=True,
                  )
figBRSTEELIMP.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    title='Brazil Steel Imports and % of Apparent Consumption',
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSTEELFLATLONG = px.area(DFBASE,
                             x='Tempo17',
                             y=['Flat Steel Imports (BR)','Long Steel Imports (BR)'],
                             color_discrete_sequence=colorpallete,
                             title='Flat and Long Steel Imports Brazil (kt)')
figBRSTEELFLATLONG.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)

figBRSTEELCONSUMPTION = px.area(DFBASE,
                             x='Tempo17',
                             y=['Flat Steel Consumption (BR)','Long Steel Consumption (BR)'],
                             color_discrete_sequence=colorpallete,
                             title='Flat and Long Steel Consumption Brazil (kt)')
figBRSTEELCONSUMPTION.update_layout(
    xaxis_title= "",
    yaxis_title="",
    legend_title="",
    legend=dict(orientation='h',yanchor='top',y=1.1, xanchor='left',x=0)
)



#---------------------------------------------------------------------------------------------

add_logo("C:/Users/otavio.batini/Desktop/Commodities_Dashboard/logo.png")
fig_col1, fig_col2 = st.columns(2)
#---------------------------------------------------------------------------------------------
selectmetals = st.sidebar.selectbox('Select Panel',
                       ['Geral','Prices','China Panel','Brazil Panel','Companies'],
                       )

if selectmetals == 'Geral':
    with fig_col1:
        st.plotly_chart(figIOPRICES)
        st.plotly_chart(figCISA)
    with fig_col2:
        st.plotly_chart(figSTEELPRICES)
        st.plotly_chart(figINVANUAL)

if selectmetals == 'Prices':
    with fig_col1:
        st.plotly_chart(figIOPRICES)
        st.plotly_chart(figSTEELPRICES)
        st.plotly_chart(figDOMESTICPRICESBRL)
        st.plotly_chart(figEXPORTPRICES)
    with fig_col2:
        st.plotly_chart(figFOBBR)
        st.plotly_chart(figVALEFOB)
        st.plotly_chart(figDOMESTICPRICESUSD)
        st.plotly_chart(figBRSPREAD)
#-----------------------------------------------------------------------
x1TF = '2018-08-01'
x2TF = '2023-9-01'
x3TF = '2022-07-01'
x4TF = '2023-01-01'
x5TF = '2023-12-01'


if selectmetals == 'China Panel':
    Timeframe = st.sidebar.selectbox('Select Timeframe',
                         ['All','5y','1y','YTD']) 
    if Timeframe == '5y':
        figSTEELPRODUCTION.update_layout(
            xaxis_range=[x1TF,x2TF],
            yaxis_range=[1.5,2.5])
        figSTEELPRODXDEMAND.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figSTEELINVENTORY.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figINVENTORYPRODUCTS.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figSTEELPRODTOTAL.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figINVENTORYCOUNTRIES.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figSTEELTRADE.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figIOSHIPBR.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figIODEMAND.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figIOSTOCK.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figIOSTOCK.update_yaxes(range=[0, 25000], secondary_y=False)
        figIOSTOCK.update_yaxes(range=[0, 180], secondary_y=True)
        figTRADERSINV.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figMILLSINV.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figMILLSUTILIZATION.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figBFCAPACITY.update_layout(
            xaxis_range=[x1TF,x2TF],)
        figMILLSPROFIT.update_layout(
            xaxis_range=[x1TF,x2TF],)
    if Timeframe == '1y':
        figSTEELPRODUCTION.update_layout(
            xaxis_range=[x3TF,x2TF],
            yaxis_range=[1.5,2.5])
        figSTEELPRODXDEMAND.update_layout(
            xaxis_range=[x3TF,x2TF],)
        figSTEELPRODXDEMAND.update_yaxes(range=[55000,100000], secondary_y=False)
        figSTEELPRODXDEMAND.update_yaxes(range=[0,15000], secondary_y=True)
        figSTEELINVENTORY.update_layout(
            xaxis_range=[x3TF,x2TF],
            yaxis_range=[10,20])
        figINVENTORYPRODUCTS.update_layout(
            xaxis_range=[x3TF,x2TF],
            yaxis_range=[80000,150000])
        figSTEELPRODTOTAL.update_layout(
            xaxis_range=[x3TF,x2TF])
        figSTEELPRODTOTAL.update_yaxes(range=[40000,120000], secondary_y=False)
        figSTEELPRODTOTAL.update_yaxes(range=[-0.2,0.3], secondary_y=True)
        figINVENTORYCOUNTRIES.update_layout(
            xaxis_range=[x3TF,x2TF])
        figSTEELTRADE.update_layout(
            xaxis_range=[x3TF,x2TF])
        figIOSHIPBR.update_layout(
            xaxis_range=[x3TF,x2TF])
        figIODEMAND.update_layout(
            xaxis_range=[x3TF,x2TF])
        figIOSTOCK.update_layout(
            xaxis_range=[x3TF,x2TF],)
        figIOSTOCK.update_yaxes(range=[0, 20000], secondary_y=False)
        figIOSTOCK.update_yaxes(range=[0, 180], secondary_y=True)
        figTRADERSINV.update_layout(
            xaxis_range=[x3TF,x2TF],)
        figMILLSINV.update_layout(
            xaxis_range=[x3TF,x2TF],)
        figMILLSUTILIZATION.update_layout(
            xaxis_range=[x3TF,x2TF],)
        figBFCAPACITY.update_layout(
            xaxis_range=[x3TF,x2TF],)
        figMILLSPROFIT.update_layout(
            xaxis_range=[x3TF,x2TF],)     
    if Timeframe == 'YTD':
        figSTEELPRODUCTION.update_layout(
            xaxis_range=[x4TF, x5TF],
            yaxis_range=[1.8,2.4])
        figSTEELPRODXDEMAND.update_layout(
            xaxis_range=[x4TF, x5TF],)
        figSTEELPRODXDEMAND.update_yaxes(range=[55000,100000], secondary_y=False)
        figSTEELPRODXDEMAND.update_yaxes(range=[0,15000], secondary_y=True)
        figSTEELINVENTORY.update_layout(
            xaxis_range=[x4TF, x5TF],
            yaxis_range=[12,20])
        figINVENTORYPRODUCTS.update_layout(
            xaxis_range=[x4TF, x5TF],
            yaxis_range=[80000,150000])
        figSTEELPRODTOTAL.update_layout(
            xaxis_range=[x4TF, x5TF])
        figSTEELPRODTOTAL.update_yaxes(range=[60000,100000], secondary_y=False)
        figSTEELPRODTOTAL.update_yaxes(range=[-0.2,0.3], secondary_y=True)
        figINVENTORYCOUNTRIES.update_layout(
            xaxis_range=[x4TF, x5TF])
        figSTEELTRADE.update_layout(
            xaxis_range=[x4TF, x5TF])
        figIOSHIPBR.update_layout(
            xaxis_range=[x4TF, x5TF])
        figIODEMAND.update_layout(
            xaxis_range=[x4TF, x5TF],
            yaxis_range=[18,32])
        figIOSTOCK.update_layout(
            xaxis_range=[x4TF, x5TF],)
        figIOSTOCK.update_yaxes(range=[0, 20000], secondary_y=False)
        figIOSTOCK.update_yaxes(range=[0, 180], secondary_y=True)
        figTRADERSINV.update_layout(
            xaxis_range=[x4TF, x5TF],)
        figMILLSINV.update_layout(
            xaxis_range=[x4TF, x5TF],)
        figMILLSUTILIZATION.update_layout(
            xaxis_range=[x4TF, x5TF],)
        figBFCAPACITY.update_layout(
            xaxis_range=[x4TF, x5TF],)
        figMILLSPROFIT.update_layout(
            xaxis_range=[x4TF, x5TF],)     

    with fig_col1:
        st.plotly_chart(figSTEELPRODUCTION)
        st.plotly_chart(figSTEELPRODXDEMAND)
        st.plotly_chart(figSTEELINVENTORY)
        st.plotly_chart(figINVENTORYPRODUCTS)
        st.plotly_chart(figIOSTOCK)
        st.plotly_chart(figMILLSINV)
        st.plotly_chart(figMILLSINVANUAL)
        st.plotly_chart(figSTEELSCRAP)
        st.plotly_chart(figIODEMAND)
        st.plotly_chart(figBFCAPACITY)
    with fig_col2:
        st.plotly_chart(figCISA)
        st.plotly_chart(figSTEELPRODTOTAL)
        st.plotly_chart(figINVANUAL)
        st.plotly_chart(figINVENTORYCOUNTRIES)
        st.plotly_chart(figIOSTOCKANUAL)
        st.plotly_chart(figTRADERSINV)
        st.plotly_chart(figTRADERSINVANUAL)
        st.plotly_chart(figMILLSUTILIZATION)
        st.plotly_chart(figSTEELTRADE)
        st.plotly_chart(figMILLSPROFIT)

#---------------------------------------------------------------------------------

if selectmetals == 'Brazil Panel':
    with fig_col1:
        st.plotly_chart(figBRSTEELPROD)
        st.plotly_chart(figBRSTEELTRADE)
        st.plotly_chart(figBRSTEELEXP)
        st.plotly_chart(figBRSTEELFLATLONG)
        st.plotly_chart(figFOBBR)
    with fig_col2:
        st.plotly_chart(figBRSTEELSALES)
        st.plotly_chart(figBRTRADEPX)
        st.plotly_chart(figBRSTEELIMP)
        st.plotly_chart(figBRSTEELCONSUMPTION)
        st.plotly_chart(figIOSHIPBR)


if selectmetals == 'Companies':
    with fig_col1:
        st.plotly_chart(figVALEFOB)
        
        
        
