from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_trich_components as dtc
from Stylee import cardbody_style, card_icon, cardimg_style, card_style
from helping_components import output_card
import pandas as pd
from datar.all import case_when, f, mutate, pivot_wider

LSMS1=pd.read_csv(r'C:\Users\flavi\Downloads\data for practice\sect11b_harvestw3.csv')
LSMS1.rename(columns={'s11bq4': 'expenditure',},inplace=True)
LSMS1.dropna(subset=['expenditure'],inplace=True)

LSMS1_data_list=['KEROSENE', 'PALM KERNEL OIL', 'OTHER LIQUID COOKING FUEL', 'ELECTRICITY', 'CANDLES', 'FIREWOOD', 'CHARCOAL', 
                'PETROL','DIESEL']
LSMS1_List=LSMS1[LSMS1.item_desc.isin(LSMS1_data_list)]

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


expend_page = html.Div([
    dbc.Row(
            children=[ 
                    dbc.Col(lg=1),
                    dbc.Col(lg=2, #style={'marginRight': '2%'},
                            children=[
                                dbc.Label('Select State'),
                                dcc.Dropdown(id='state_dropdown',
                                                options=[{'label': state, 'value': state}
                                                        for state in LSMS_df['state_name'].unique()
                                                        ],
                                                placeholder='Select states'
                                                )
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
                                                                                            html.H3(id='avg_expense'
                                                                                                    ),
                                                                                            html.P('Average Expenditure')
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
                                                                    html.Br(),
                                                                    output_card(card_id='cred3',card_label='Credit 3', 
                                                                                icon='bi bi-cash-coin', style={'backgroundColor': 'green'}
                                                                                ),
                                                                   
                                                                ]
                                                        )
                                            ]
                                        ),
                                    
                                    dbc.Row([output_card(card_id='newcard', card_label='test card')]),
                                    html.Br(),
                                    dbc.Row([
                                        ]),
                                    
                                    html.Div([], id="container_to_render")
                                ]
                            )
            ]
    )
])


income_page = html.Div([
    dbc.Row(dbc.Row([dbc.Col(lg=1),
                     output_card(card_id='inc', card_label='Average income')
                    ]
                    )
            )
])

credit_page = html.Div([
    dbc.Row(dbc.Row([dbc.Col(lg=1),
                     output_card(card_id='cred', card_label='Average credit')
                    ]
                    )
            )
])

welcome_page = html.Div([
    dbc.Row(dbc.Row([dbc.Col(lg=1),
                        output_card(card_id='welcome', card_label='Welcome')
                    ]
                    )
            )
])

page_view = html.Div(
    [
        dtc.SideBar(children=[
                                dtc.SideBarItem(id='income_sidebar', label='Income', icon='far fa-money-bill-alt'),
                                dtc.SideBarItem(id='credit_sidebar', label='Credit', icon='bi bi-credit-card'),
                                dtc.SideBarItem(id='expend_sidebar', label='Expenditure', icon='bi bi-wallet-fill')
                            ]),
        html.Div([], id="content")
    ]
)