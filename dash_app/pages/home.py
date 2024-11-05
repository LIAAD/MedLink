import dash
import constants
import backend
from dash import html, dcc,callback, page_container,page_registry,ctx,no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import example_cards as sample_cards
from flask import request
dash.register_page(__name__, title='Página Inicial', description='Página Inicial',path='/')





def buildMainContainer(lang="pt"):

    main=[
        dbc.Row(dbc.Col(html.H1(children=[html.Span(className="beg",children="Med"),html.Span(className="ed",children="Link")],className="text-center title")),className="p-4"),
        dbc.Row(dbc.Col(html.P(constants.MAIN_PAGE_SHORT_CATCHPHRASE[lang],className="text-center catchphrase"))),
        dbc.Row(dbc.Col(dbc.Textarea(id="input-text",className="mb-6", placeholder=constants.MAIN_PAGE_TEXT_PLACEHOLDER[lang], style={'height': 300}),xs=12, sm=10, md=10, lg=9,className="mx-auto d-flex justify-content-center"), className="p-4"),
        dbc.Row(dbc.Col(dbc.Button(constants.SUBMIT_BUTTON[lang], id="submit-button",n_clicks=0,className="w-75"),className="mx-auto d-flex justify-content-center",xs=12, sm=6, md=5, lg=5)),
        dbc.Row([
            dbc.Alert(
                constants.ALERT[lang],
                id="alert-size",
                is_open=False,
                duration=5000,
                color="danger"
            )
            ]),
        dbc.Row(dbc.Col(html.H2(constants.EXAMPLE_TEXTS[lang])),className="p-4"),
        dcc.Location(id='url', refresh=True),
        sample_cards.buildCards(lang)

    ]
    return main


def layout(lang="pt"):
    print("LNAG")
    print(lang)
    return(dbc.Container(fluid=True,children=buildMainContainer(lang)))


@callback(
    [Output("stored-text", 'data'), Output("alert-size", "is_open"),  Output('url', 'pathname'),Output('submit-button',"n_clicks")],
    Input('submit-button',"n_clicks"),
#    Input('url', 'pathname'),
    State('input-text', 'value')
)
def store_text(nclicks,text):
    print("DEBUG")
    print(nclicks,text)
    if(nclicks>0):
        if(text):
            words=text.split()
            if(len(words)<50):
                return None,True,"/",0
            else:
                print("HERE")
                print(text)
                return({"text":text},False,"/results",0)
        else:
            print("CLEAR")
            return None, False, "/", 0

    return None, no_update, "/", 0

@callback(
    Output("input-text", "value"),
    [Input(f"copy-button-{i}", "n_clicks") for i in range(len(sample_cards.text_examples))],
    [State(f"text-{i}", "children") for i in range(len(sample_cards.text_examples))]
)
def copy_text_to_input(*args):
    card_texts = args[len(sample_cards.text_examples):]

    # Check which button was clicked
    triggered_id = ctx.triggered_id

    if triggered_id:
        # Extract the index from the button ID
        idx = int(triggered_id.split("-")[-1])
        return card_texts[idx]


