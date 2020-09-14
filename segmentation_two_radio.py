### three graphs, works well
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# impor data for metrics
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
df=pd.read_excel('C://Users//Alcides//Desktop//My_Django_stuff//plotly//raw.xlsx', sheet_name='Sheet1', index_col=0)
df=df.T
df=df[['  65 years and over %','Female lone-parent family household %',
'Household has at least one person with activity limitations %',
'Above housing standards %', 'Median STIR before taxes (%)']]
df=df.rename(columns={'  65 years and over %': 'aged 65+','Female lone-parent family household %': "single mother",
                  'Household has at least one person with activity limitations %':'Have disabilities',
                  'Above housing standards %': 'not in CHN','Median STIR before taxes (%)':'Median STIR'})
df['%CHN']=100-df['not in CHN']
df.drop('not in CHN', axis=1, inplace=True)
df=df.unstack().reset_index()
df=df.rename(columns={'level_0': 'Metric','level_1':'CMA',0:'%'})

#import data for income
df1=pd.read_excel('C://Users//Alcides//Desktop//My_Django_stuff//plotly//raw.xlsx', sheet_name='Sheet1', index_col=0)
df1=df1.T
df1=df1[['Less than $20,000 before taxes %', '$20,000 to $39,999 before taxes %',
       '$40,000 to $59,999 before taxes %',
       '$60,000 to $79,999 before taxes %',
       '$80,000 to $99,999 before taxes %', '$100,000 and over before taxes %',]]

df1=df1.rename(columns={'Less than $20,000 before taxes %': 'Less than $20,000','$20,000 to $39,999 before taxes %': '$20,000 to $39,999',
                 '$40,000 to $59,999 before taxes %':'$40,000 to $59,999',
                  '$60,000 to $79,999 before taxes %': '$60,000 to $79,999',
                  '$80,000 to $99,999 before taxes %':'$80,000 to $99,999',
                  '$100,000 and over before taxes %':'$100,000 and over'})
df1=df1.unstack().reset_index()
df1=df1.rename(columns={'level_0': 'Metric','level_1':'CMA',0:'%'})
#####################################

# import data for dwelling type
df2=pd.read_excel('C://Users//Alcides//Desktop//My_Django_stuff//plotly//raw.xlsx', sheet_name='Sheet1', index_col=0)
df2=df2.T
df2=df2[[ 'Single-detached house %', 'Semi-detached or double house %',
       'Row house %', 'Apartment, duplex %',
       'Apartment in a building that has fewer than five storeys %',
       'Apartment in a building that has five or more storeys %',
       'Other dwelling type %']]

df2=df2.rename(columns={'Single-detached house %':'Single-detached','Semi-detached or double house %':'Semi-detached',
        'Row house %':'Row house','Apartment, duplex %':'Apartment, duplex',
        'Apartment in a building that has fewer than five storeys %':'Apartment, <5 storeys',
        'Apartment in a building that has five or more storeys %':'Apartment >5 storeys %',
        'Other dwelling type %':'Other dwelling type'})
df2=df2.unstack().reset_index()
df2=df2.rename(columns={'level_0': 'Metric','level_1':'CMA',0:'%'})

###############

# import scatter data


df_new=pd.read_csv('scatter1.csv', encoding='latin-1')
df_new.loc[df_new['label']=='red', 'label']='Tier 2: affordable supply'
df_new.loc[df_new['label']=='yellow', 'label']='Tier 3: adequate supply'
df_new.loc[df_new['label']=='green', 'label']='Tier1: unaffordable supply'
df_new.rename(columns={'ratio_cost_GST':'income/rent'}, inplace=True)





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

available_indicators = df['CMA'].unique()
available_indicators1 = df1['CMA'].unique()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
html.H1('CMA Clustering by the Factors Determining Housing Needs.', style={
    'textAlign': 'center',
    'color': colors['text']
}),
html.H3('Source: Census 2016', style={
    'textAlign': 'center',
    'color': colors['text']
}),
 html.Div([
    dcc.Graph(id='graph-with-slider2'),

# =============================================================================
#      dcc.Dropdown(
#          id='xaxis-column2',
#          options=[{'label': i, 'value': i} for i in ['2019 VR', 'Mean VR']],
#          value=['2019 VR'],
#          multi=True
#  
#      ),
# =============================================================================
     dcc.RadioItems(
                'xaxis-column2',
                options=[{'label': i, 'value': i} for i in ['2019 VR', '3_year_VR','5_year_VR']],
                value='2019 VR',
                labelStyle={'display': 'inline-block'}
            ),
     dcc.RadioItems(
                'xaxis-column3',
                options=[{'label': i, 'value': i} for i in ['income/rent', 'rent/income']],
                value='income/rent',
                labelStyle={'display': 'inline-block'}
            ),

], style = {'display': 'inline-block', 'width': '100%'}),


html.Div([

 html.Div([
#  html.Div([
#     dcc.Graph(id='graph-with-slider'),
#     dcc.Dropdown(
#         id='xaxis-column',
#         options=[{'label': i, 'value': i} for i in available_indicators],
#         value=['Toronto'],
#         multi=True
#
#     ),
# ]),

html.Div([
    dcc.Graph(id='graph-with-slider1'),
    dcc.Dropdown(
        id='xaxis-column1',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value=['Toronto'],
        multi=True

    ),
]),

html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in available_indicators],
        value=['Toronto'],
        multi=True

    ),
# =============================================================================
#     dcc.Dropdown(
#         id='xaxis-column2',
#         options=[{'label': i, 'value': i} for i in available_indicators],
#         value=['Toronto'],
#         multi=True
# 
#     ),
# =============================================================================
    
])


])

], style = { 'columnCount': 2})
])


#####################


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('xaxis-column', 'value')])
def update_figure(cont='Toronto'):
    # filtered_df = df[(df.continent == cont) & (df.year == 1952)]
    # filtered_df = df[df.continent == cont]

    # filtered_df=df[df['CMA']== cont]
    filtered_df=df[df['CMA'].isin(cont)]

    fig = px.bar(filtered_df, x="Metric", y="%", color="CMA", barmode="group")
    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})


    return fig

@app.callback(
    Output('graph-with-slider1', 'figure'),
    [Input('xaxis-column1', 'value')])
def update_figure1(cont='Toronto'):
    # filtered_df = df[(df.continent == cont) & (df.year == 1952)]
    # filtered_df = df[df.continent == cont]

    # filtered_df=df[df['CMA']== cont]
    filtered_df1=df1[df1['CMA'].isin(cont)]

    fig1 = px.bar(filtered_df1, x="Metric", y="%", color="CMA", barmode="group")
    fig1.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig1






@app.callback(
     Output('graph-with-slider2', 'figure'),
     [Input('xaxis-column2', 'value'),
      Input('xaxis-column3','value')])
def update_figure2(cont, cont1):
    fig_scat=px.scatter(df_new[[cont1,'CMA','label',cont]], 
                        x=cont1, y=cont,
                             color='label', 
                             size_max=60,
                             hover_name="CMA",
                              #text='CMA',
                              )
# =============================================================================
#     fig_scat=px.scatter(df_dict[cont], x='Income/Rent', y='2019 VR',
#                              color='label', size_max=60,hover_name="CMA")
# =============================================================================
# =============================================================================
# =============================================================================
#     if cont=='Mean VR':
#      
#         fig_scat=px.scatter(df3, x='Income/Rent', y='2019 VR',
#                              color='label', size_max=60,hover_name="CMA")
#     elif cont=='2019 VR':
#         fig_scat=px.scatter(df4, x='Income/Rent', y='2019 VR',
#                              color='label', size_max=60,hover_name="CMA")
# =============================================================================

   
    #fig_scat.update_traces(textposition='top center')
    fig_scat.update_layout(height=300, margin={'l': 200, 'b': 30, 'r': 100, 't': 10})
 
    return fig_scat



app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=False)




