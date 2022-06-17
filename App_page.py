#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import plotly.express as px
from datar.all import case_when, f, mutate, pivot_wider
from urllib.parse import unquote


# In[7]:


#uploading dataset
LSMS1=pd.read_csv(r'C:\Users\flavi\Downloads\data for practice\sect11b_harvestw3.csv')
LSMS1.head()
LSMS1.rename(columns={'s11bq4': 'expenditure',},inplace=True)
LSMS1
LSMS1.dropna(subset=['expenditure'],inplace=True)
LSMS1.isna().sum()
LSMS1.item_desc.unique()


# In[8]:


#from datar import dplyr
#import plotly.io as pio
#from plotly.offline import init_notebook_mode, plot
#init_notebook_mode()


#%%
alink = "http://127.0.0.1:8012/ml"
alink
unquote(alink)
alink.split('/')[-1]

blink = "http://127.0.0.1:8012/analytics"

blink.split('/')[-1]


#%%
#Filtering out the required items for analysis
LSMS1_data_list=['KEROSENE', 'PALM KERNEL OIL', 'OTHER LIQUID COOKING FUEL', 'ELECTRICITY', 'CANDLES', 'FIREWOOD', 'CHARCOAL', 
                'PETROL','DIESEL']
LSMS1_List=LSMS1[LSMS1.item_desc.isin(LSMS1_data_list)]
#LSMS1_List

# %%
#Assigning names to states
LSMS_df=mutate(LSMS1_List,state_name=case_when(f.state==1,'Abia', f.state==2,'Adamawa',f.state==3,'Akwa Ibom',
                                                         f.state==4,'Anambra',f.state==5,'Bauchi',f.state==6,'Bayelsa',
                                                          f.state==7,'Benue',f.state==8,'Borno',f.state==9,'Cross River',
                                                       f.state==10,'Delta', f.state==11,'Ebonyi',f.state==12,'Edo', 
                                                        f.state==13,'Ekiti', f.state==14,'Enugu',f.state==15,'Gombe',
                                                        f.state==16,'Imo',f.state==17,'Jigawa',f.state==18,'Kaduna',
                                                          f.state==19,'Kano',f.state==20,'Katsina',f.state==21,'Kebbi',
                                                         f.state==22,'Kogi',f.state==23,'Kwara',f.state==24,'Lagos',
                                                         f.state==25,'Nasarawa',f.state==26,'Niger',f.state==27,'Ogun',
                                                         f.state==28,'Ondo',f.state==29,'Osun',f.state==30,'Oyo',
                                                         f.state==31,'Plateau',f.state==32,'Rivers',f.state==33,'Sokoto',
                                                        f.state==34,'Taraba',f.state==35,'Yobe',f.state==36,'Zamfara',
                                                         f.state==37,'FCT Abuja')
                                        .drop(columns='state'))

#LSMS_df

# %%
#Average expenditure by states
LSMS_df.groupby(
    ['item_desc','state_name',])['expenditure'].agg([np.mean])
LSMS1_List.head(10)


# In[10]:


#Dash imports
import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from jupyter_dash import JupyterDash
import dash_trich_components as dtc


# In[11]:


app = JupyterDash(__name__, external_stylesheets=[dbc.themes.SUPERHERO]) 

app.layout = html.Div([
    html.H1('Average expenditure per state',
            style={'color': 'blue',
                   'fontSize': '40px'}),
    html.H2('Visualization of Average expenditure by states'),
    dbc.Tabs([
       dbc.Tab([
           html.Ul([
               html.Br(),
               html.Li('Number of states in Nigeria:37'),
               html.Li('Number of lga:774'),
               html.Li('Currency:Naira'),
               html.Li('Population:175 million:2014 estimate'),
               html.Li([
                   'Source:',
                   html.A('https://nigerianfinder.com/facts-about-nigeria/',
                        href='https://nigerianfinder.com/facts-about-nigeria/' )
               ])
           ])

       ], label='Key Facts'),
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('General Household Survey, Panel 2015-2016,'),
                html.Li('Analyzing and visualizing average expenditure of selected items by States'),
                html.Li('Dash presentation pracice'),
                html.Li([
                    'Source:',
                         html.A('https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary',
                               href='https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary'),
                               
                         ])
            ])
        ], label='Project Info')
    ]),
    
     html.Div([('Expenditure: Visualization of average expenditure of selected items per state'),
     dcc.Dropdown(LSMS_df.state_name.unique(), id='state_name',placeholder='Select a city'),
     html.Div(id='output_container',children=[]),
     html.Br(),
     dcc.Graph(id='state_graph'),
    
])
    
])
@app.callback(Output(component_id='state_graph', component_property='figure'),
              Input(component_id='state_name', component_property='value')
              )
def create_graph(state_selected):
    df = LSMS_df[LSMS_df['state_name']==state_selected]
    
    fig=px.bar(data_frame=df,
                x='item_desc',
                y='expenditure',
                color='state_name',
                opacity=0.9,
                orientation='v',
                barmode='relative',
                hover_name='expenditure',
                template='plotly_dark',
                animation_frame='state_name',
                title=f'Graph of {state_selected}'
                )
    
    return fig
if __name__ == '__main__':
    app.run_server(port=8056, mode='inline')


# In[12]:


app = dash.Dash(__name__, external_stylesheets= [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME])

cardimg_style = {'width': '100%', 'height': '100%', 
              "opacity": 0.2, "objectFit": "cover"
              }
cardbody_style = {"margin": "2%"}

card_style = {"width": "20rem", "height": "20rem"}
card_icon = {
    "color": "blue",
    "textAlign": "center",
    "fontSize": "4em",
    "margin": "auto"
}

img2 = './Img/stephen-dawson-qwtCeJ5cLYs-unsplash.jpeg'


start_page = html.Div(
    children=[     
        dcc.Location(id='location_url'),
        dbc.Row(html.Div(id="page_location"))
        ],
)

homepage = html.Div(children=[
    
    dbc.Container(children=[       
        dbc.Row([
                    html.H3('Analysis on Living Standard Measurement Survey')                    
                ]
            ),
        html.Br(),
        dbc.Row(
                children=[
                    dbc.Tabs(
                        children=[
                                    dbc.Tab(
                                            children=[
                                                        html.Ul(
                                                            [
                                                                html.Br(),
                                                                html.Li('Number of states in Nigeria:37'),
                                                                html.Li('Number of lga:774'),
                                                                html.Li('Currency:Naira'),
                                                                html.Li('Population:175 million:2014 estimate'),
                                                                html.Li([
                                                                        'Source:',
                                                                        html.A('https://nigerianfinder.com/facts-about-nigeria/',
                                                                                href='https://nigerianfinder.com/facts-about-nigeria/'
                                                                                )
                                                                        ]
                                                                    )
                                                            ]
                                                        )
                                                    ], 
                                            label='Key Facts'
                                        ),
                                    dbc.Tab([
                                        html.Ul([
                                            html.Br(),
                                            html.Li('General Household Survey, Panel 2015-2016,'),
                                            html.Li('Analyzing and visualizing average expenditure of selected items by States'),
                                            html.Li('Dash presentation pracice'),
                                            html.Li([
                                                'Source:',
                                                    html.A('https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary',
                                                        href='https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary'),
                                                        
                                                    ])
                                        ])
                                    ], label='Project Info')
                                ]
                            ),
    
                        ]
                    ),
                html.Br(),
        dbc.Row([
                 dbc.Col([
                         dbc.Card(
                            [
                                dbc.CardImg(
                                    src='./Img/firmbee-com-jrh5lAq-mIs-unsplash.jpeg',
                                
                                    style=cardimg_style,
                                ),
                                dbc.CardLink(id="analytics_link",
                                    children=[
                                        dbc.CardImgOverlay(
                                            [
                                                dbc.CardBody(
                                                    html.H3(
                                                        "Analytics",
                                                        style=cardbody_style,
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    href="analytics",
                                ),
                            ],
                            style=card_style,
                        )
                     
                     ]),
                 html.Br(),
                 dbc.Col([
                        dbc.Card(
                            dbc.Card(
                                [
                                    dbc.CardImg(
                                        src=img2,
                                        style=cardimg_style,
                                    ),
                                    dbc.CardLink(id="ml_link",
                                        children=[
                                            dbc.CardImgOverlay(
                                                [
                                                    dbc.CardBody(
                                                        html.H3(
                                                            "Machine leARNING",
                                                            style=cardbody_style,
                                                        )
                                                    )
                                                ]
                                            )
                                        ],
                                        href="ml",
                                    ),
                                ],
                                style=card_style,
                            )
                        )
                    ])   
        ])
                ],
                  
            ),
    
        
        
    ])
#])

analytic_page = html.Div([
    dbc.Row(
            children=[
                    dbc.Label('Select Indicator'),
                    dbc.Col(lg=3,
                        children=[
                            
                            html.Br(), html.Br(),
                            dtc.SideBar(children=[
                                dtc.SideBarItem(id='id_1', label='Income', icon='far fa-money-bill-alt'),
                                dtc.SideBarItem(id='credit_siderbar', label='Credit', icon='bi bi-credit-card'),
                                dtc.SideBarItem(id='expen_sidebar', label='Expenditure', icon='bi bi-wallet-fill')
                            ])
                            
                        ]
                        ),
                    dbc.Col(lg=9,
                            children=[
                                    dbc.Row(
                                            children=[
                                                        dbc.Row(
                                                                children=[
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg_income',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Average income')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg2',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Average income')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                        ),
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg3',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Average 3')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    )
                                                                    
                                                                ]
                                                            ),
                                                        #html.Br(), html.Br(), html.Br(),
                                                        html.Hr(),
                                                        dbc.Row(
                                                                children=[
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='cred1',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Credit 1')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                        ),
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='cred2',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Credit 2')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                        ),
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='cred3',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Credit 3')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    )
                                                                ]
                                                        )
                                            ]
                                        ),
                                    
                                    dbc.Row()
                                ]
                            )
            ]
    )
])

ml_page = html.Div([])

app.layout = start_page
app.validation_layout = html.Div([homepage, analytic_page, ml_page])

######## callback  ######
@app.callback(Output(component_id="page_location", component_property="children"),
              Input(component_id="location_url", component_property="href")
              )
def render_page_selected(page_link):
    page_selected = page_link.split('/')[-1]
    
    if page_selected == 'ml':
        return ml_page
    elif page_selected == 'analytics':
        return analytic_page
    else:
        return homepage
    
##################################
#App layout
# analytics_page = html.Div([
#     html.H1('Average Expenditure per state',style={'text-align':'center','color': 'blue','fontSize': '40px'}),
#     html.H2('All States rep by names'),
#     dcc.Dropdown(LSMS_df.state_name.unique(), id='state_name',placeholder='Select a city'),
#     html.Div(id='output_container',children=[]),
#     html.Br(),
#     dcc.Graph(id='state_graph'),
# ])

#%%
#Visualization of average expenditure per state
# fig=px.bar(LSMS_df,
#     x='item_desc',
#     y='expenditure',
#     color='state_name',
#     opacity=0.9,
#     orientation='v',
#     barmode='relative',
#     hover_name='expenditure',
#     template='plotly_dark',
#     animation_frame='state_name',
#     )
# fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration']=5000

if __name__ == '__main__':
    app.run_server(debug=False,use_reloader=False, port='8055')
   


# In[14]:


from Stylee import cardbody_style, card_icon, cardimg_style, card_style


# In[15]:


from helping_components import output_card


# In[16]:


import Analytics_page


# In[17]:


app = dash.Dash(__name__, external_stylesheets= [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME])

img2 = './Img/stephen-dawson-qwtCeJ5cLYs-unsplash.jpeg'


start_page = html.Div(
    children=[     
        dcc.Location(id='location_url'),
        dbc.Row(html.Div(id="page_location"))
        ],
)

homepage = html.Div(children=[
    
    dbc.Container(children=[       
        dbc.Row([
                    html.H3('Analysis on Living Standard Measurement Survey')                    
                ]
            ),
        html.Br(),
        dbc.Row(
                children=[
                    dbc.Tabs(
                        children=[
                                    dbc.Tab(
                                            children=[
                                                        html.Ul(
                                                            [
                                                                html.Br(),
                                                                html.Li('Number of states in Nigeria:37'),
                                                                html.Li('Number of lga:774'),
                                                                html.Li('Currency:Naira'),
                                                                html.Li('Population:175 million:2014 estimate'),
                                                                html.Li([
                                                                        'Source:',
                                                                        html.A('https://nigerianfinder.com/facts-about-nigeria/',
                                                                                href='https://nigerianfinder.com/facts-about-nigeria/'
                                                                                )
                                                                        ]
                                                                    )
                                                            ]
                                                        )
                                                    ], 
                                            label='Key Facts'
                                        ),
                                    dbc.Tab([
                                        html.Ul([
                                            html.Br(),
                                            html.Li('General Household Survey, Panel 2015-2016,'),
                                            html.Li('Analyzing and visualizing average expenditure of selected items by States'),
                                            html.Li('Dash presentation pracice'),
                                            html.Li([
                                                'Source:',
                                                    html.A('https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary',
                                                        href='https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary'),
                                                        
                                                    ])
                                        ])
                                    ], label='Project Info')
                                ]
                            ),
    
                        ]
                    ),
                html.Br(),
        dbc.Row([
                 dbc.Col([
                         dbc.Card(
                            [
                                dbc.CardImg(
                                    src='./Img/firmbee-com-jrh5lAq-mIs-unsplash.jpeg',
                                
                                    style=cardimg_style,
                                ),
                                dbc.CardLink(id="analytics_link",
                                    children=[
                                        dbc.CardImgOverlay(
                                            [
                                                dbc.CardBody(
                                                    html.H3(
                                                        "Analytics",
                                                        style=cardbody_style,
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    href="analytics",
                                ),
                            ],
                            style=card_style,
                        )
                     #])
                     ]),
                 html.Br(),
                 dbc.Col([
                        dbc.Card(
                            dbc.Card(
                                [
                                    dbc.CardImg(
                                        src=img2,
                                        style=cardimg_style,
                                    ),
                                    dbc.CardLink(id="ml_link",
                                        children=[
                                            dbc.CardImgOverlay(
                                                [
                                                    dbc.CardBody(
                                                        html.H3(
                                                            "Machine leARNING",
                                                            style=cardbody_style,
                                                        )
                                                    )
                                                ]
                                            )
                                        ],
                                        href="ml",
                                    ),
                                ],
                                style=card_style,
                            )
                        )
                    ])   
        ])
                ],
                  
            ),
    
        
        
    ])
#])


ml_page = html.Div([])

app.layout = start_page
app.validation_layout = html.Div([homepage, Analytics_page.page_view, ml_page])

######## callback  ######
@app.callback(Output(component_id="page_location", component_property="children"),
              Input(component_id="location_url", component_property="href")
              )
def render_page_selected(page_link):
    page_selected = page_link.split('/')[-1]
    
    if page_selected == 'ml':
        return ml_page
    elif page_selected == 'analytics':
        return Analytics_page.page_view
    else:
        return homepage
    
@app.callback(Output(component_id='avg_expense', component_property='children'),
              Input(component_id='state_dropdown', component_property='value'))
def render_state_avg_income(state_selected):
    state_df = LSMS_df[LSMS_df['state_name'] == state_selected] 
    state_avg_expd = state_df['expenditure'].mean()  
    return f'{round(state_avg_expd, 2)}'


@app.callback(
    Output("content", "children"),
    Input("income_sidebar", "n_clicks_timestamp"),
    Input("credit_sidebar", "n_clicks_timestamp"),
    Input("expend_sidebar", "n_clicks_timestamp")
)
def show_sidebar_content(income_sidebar: str, credit_sidebar: str, expend_sidebar: str):
    ctx = dash.callback_context
    button_clicked = ctx.triggered[0]["prop_id"].split(".")[0]

    if not ctx.triggered:
        button_clicked = "None"
    elif button_clicked == "income_sidebar":
        return Analytics_page.income_page
    elif button_clicked == "credit_sidebar":
        return Analytics_page.credit_page
    elif button_clicked == "expend_sidebar":
        return Analytics_page.expend_page
    else:
        return Analytics_page.welcome_page

##################################
#App layout
# analytics_page = html.Div([
#     html.H1('Average Expenditure per state',style={'text-align':'center','color': 'blue','fontSize': '40px'}),
#     html.H2('All States rep by names'),
#     dcc.Dropdown(LSMS_df.state_name.unique(), id='state_name',placeholder='Select a city'),
#     html.Div(id='output_container',children=[]),
#     html.Br(),
#     dcc.Graph(id='state_graph'),
# ])

#%%
#Visualization of average expenditure per state
# fig=px.bar(LSMS_df,
#     x='item_desc',
#     y='expenditure',
#     color='state_name',
#     opacity=0.9,
#     orientation='v',
#     barmode='relative',
#     hover_name='expenditure',
#     template='plotly_dark',
#     animation_frame='state_name',
#     )
# fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration']=5000

if __name__ == '__main__':
    app.run_server(debug=False,use_reloader=False, port='8055')
   
# %%


# In[18]:


app = dash.Dash(__name__, external_stylesheets= [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP, dbc.icons.FONT_AWESOME])

cardimg_style = {'width': '100%', 'height': '100%', 
              "opacity": 0.2, "objectFit": "cover"
              }
cardbody_style = {"margin": "2%"}

card_style = {"width": "20rem", "height": "20rem"}
card_icon = {
    "color": "blue",
    "textAlign": "center",
    "fontSize": "4em",
    "margin": "auto"
}

img2 = './Img/stephen-dawson-qwtCeJ5cLYs-unsplash.jpeg'
homepage = html.Div(children=[
    dbc.Container(children=[
        dcc.Location(id='location_url'),
        dbc.Row([
                    html.H3('Analysis on Living Standard Measurement Survey')
                    
                ]
            ),
        html.Br(),
        dbc.Row(
                children=[
                    dbc.Tabs(
                        children=[
                                    dbc.Tab(
                                            children=[
                                                        html.Ul(
                                                            [
                                                                html.Br(),
                                                                html.Li('Number of states in Nigeria:37'),
                                                                html.Li('Number of lga:774'),
                                                                html.Li('Currency:Naira'),
                                                                html.Li('Population:175 million:2014 estimate'),
                                                                html.Li([
                                                                        'Source:',
                                                                        html.A('https://nigerianfinder.com/facts-about-nigeria/',
                                                                                href='https://nigerianfinder.com/facts-about-nigeria/'
                                                                                )
                                                                        ]
                                                                    )
                                                            ]
                                                        )
                                                    ], 
                                            label='Key Facts'
                                        ),
                                    dbc.Tab([
                                        html.Ul([
                                            html.Br(),
                                            html.Li('General Household Survey, Panel 2015-2016,'),
                                            html.Li('Analyzing and visualizing average expenditure of selected items by States'),
                                            html.Li('Dash presentation pracice'),
                                            html.Li([
                                                'Source:',
                                                    html.A('https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary',
                                                        href='https://microdata.worldbank.org/index.php/catalog/2734/data-dictionary'),
                                                        
                                                    ])
                                        ])
                                    ], label='Project Info')
                                ]
                            ),
    
                        ]
                    ),
                html.Br(),
        dbc.Row([
                 dbc.Col([
                         dbc.Card(
                            [
                                dbc.CardImg(
                                    src='./Img/firmbee-com-jrh5lAq-mIs-unsplash.jpeg',
                                
                                    style=cardimg_style,
                                ),
                                dbc.CardLink(
                                    children=[
                                        dbc.CardImgOverlay(
                                            [
                                                dbc.CardBody(
                                                    html.H3(
                                                        "Analytics",
                                                        style=cardbody_style,
                                                    )
                                                )
                                            ]
                                        )
                                    ],
                                    href="analytics",
                                ),
                            ],
                            style=card_style,
                        )
                     #])
                     ]),
                 html.Br(),
                 dbc.Col([
                        dbc.Card(
                            dbc.Card(
                                [
                                    dbc.CardImg(
                                        src=img2,
                                        style=cardimg_style,
                                    ),
                                    dbc.CardLink(
                                        children=[
                                            dbc.CardImgOverlay(
                                                [
                                                    dbc.CardBody(
                                                        html.H3(
                                                            "Machine leARNING",
                                                            style=cardbody_style,
                                                        )
                                                    )
                                                ]
                                            )
                                        ],
                                        href="ml",
                                    ),
                                ],
                                style=card_style,
                            )
                        )
                    ])   
        ])
                ],
                  
            ),
    
        
        
    ])
#])

analytic_page = html.Div([
    dbc.Row(
            children=[
                    dbc.Label('Select Indicator'),
                    dbc.Col(
                        children=[
                            
                            html.Br(), html.Br(),
                            dtc.SideBar(children=[
                                dtc.SideBarItem(id='id_1', label='Income', icon='far fa-money-bill-alt'),
                                dtc.SideBarItem(id='credit_siderbar', label='Credit', icon='bi bi-credit-card'),
                                dtc.SideBarItem(id='expen_sidebar', label='Expenditure', icon='bi bi-wallet-fill')
                            ])
                            
                                 ]
                            )
                     ]
                        ),
                    dbc.Col(
                                [
                                    dbc.Row(
                                            children=[
                                                        dbc.Row(
                                                                children=[
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg_income',
                                                                                                    children='50'
                                                                                                    ),
                                                                                            html.P('Average income')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg_income2',
                                                                                                    children='100'
                                                                                                    ),
                                                                                            html.P('Average income')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-euro',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )),
                                                                    dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg_income3',
                                                                                                    children='499'
                                                                                                    ),
                                                                                            html.P('Average income')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-piggy-bank',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        ))
                                                                    
                                                                ]
                                                            ),
                                                        dbc.Row(
                                                                children=[
                                                                    dbc.Col(dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg_credit',
                                                                                                    children='1000'
                                                                                                    ),
                                                                                            html.P('credit')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-stack',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'blue'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),),
                                                                    dbc.Col(dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='Avg_credit2',
                                                                                                    children='500'
                                                                                                    ),
                                                                                            html.P('credit')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-cash-coin',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'blue'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),),
                                                                    dbc.Col(dbc.Col(
                                                                        dbc.CardGroup(
                                                                            children=[
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.H3(id='avg_credit3',
                                                                                                    children='*8'
                                                                                                    ),
                                                                                            html.P('credit')
                                                                                        ]
                                                                                    ),
                                                                                dbc.Card(
                                                                                        children=[
                                                                                            html.Div(
                                                                                                className='bi bi-credit-card-fill',
                                                                                                style=card_icon
                                                                                            )
                                                                                        ],
                                                                                        style={"backgroundColor": 'yellow'}
                                                                                )
                                                                            ]
                                                                        )
                                                                    ),)
                                                                ]
                                                        )
                                            ]
                                        ),
                                    
                                    dbc.Row(
                                            children=[ 
                                                dcc.Dropdown(LSMS_df.state_name.unique(), id='state_name',placeholder='Select a city'),
                                            ]
                                                ),
                                    dbc.Row( 
                                           children=[
                                                    html.Div(id='output_container',children=[]),
                                                    html.Br(),
                                                    dcc.Graph(id='state_graph'),
                                           ]
            )                                                       
               ])
                                                
                                
                            ])
            
    #)
#])

ml_page = html.Div([])
#analytic_page = html.Div([])
app.layout = homepage
if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False, port='8055')


# In[ ]:




