import dash
from dash import html, dcc,callback, page_container,page_registry
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import constants
import backend

dash.register_page(__name__, title="Resultados", description='Resultados')


global model
global abstract
df, embeddings = backend.loadModelsandData_update()


def layout(lang="pt"):


    return html.Div([
        dcc.Location(id='url', refresh=True),
        dbc.Row(dbc.Col(html.H1(constants.RESULTS_HEADER[lang],className="p-4"))),
        dcc.Loading([
                        html.Div(id='result-text', style={'white-space': 'pre-wrap'})
                    ],
                    overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"},
                    fullscreen=True,type="circle",id="spinner_results")
        ])





@callback(
    Output('result-text', 'children'),
    Input('stored-text', 'data'),
    Input('url',"search")
)
def display_stored_text(stored_data,url):
    print(url)
    if(stored_data):
        print(stored_data)
        list_matches=backend.getDocumentCandidates(query_text=stored_data["text"],abstracts=df["abstract"].tolist(),embeddings=embeddings)
        #list_matches=backend.mapArticles(result_ref)
        row_cards=list()
        for l in list_matches:
            row_cards.append(createCard(l))

        inserted_card = dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader("Texto Inserido"),
            dbc.CardBody(
                [

                    html.P(stored_data["text"],
                           className="card-text",
                           ),
                ],
            style = {
            "height": "300px",  # Fixed height for the scrollable area
            "overflowY": "auto",  # Enables vertical scrolling
        }),
        ])))

        header=dbc.Row(dbc.Col(html.H2("Candidatos",className="p-4")))
        return [inserted_card,header]+[dbc.Row(row_cards)]
    else:
        return "no text provided"


def createCard(dict_l):
    print(dict_l)
    card = dbc.Col(dbc.Card([

        dbc.CardHeader([html.Span("Similaridade: "),
                        dbc.Progress(value=100 * round(dict_l["score"], 2), color="info", className="mb-3")]),
        dbc.CardBody(
            [

                html.H5(dict_l["title"], className="card-title results-card-header"),
                dbc.Row(html.P(dict_l["abstract"]),className="p-2 results-card-body"),

            ]
        , style={
                    "height": "450px",  # Fixed height for equal heights
                    "overflowY": "auto",  # Add vertical scroll for overflowing content
                }),
        dbc.CardFooter([
            dbc.Row(
                [
                dbc.Col(dbc.Button("Ver análise",href="/article?id="+str(dict_l["Unnamed: 0.1"]), color="primary"),width="auto"),
                dbc.Col(dbc.Button("Link do Artigo", href=dict_l["link"], color="secondary"),width="auto",className="ms-auto")
        ],className="d-flex align-items-center")]
            )
        ],className="d-flex justify-content-between h-100"),
            xs=12, sm=6, md=6, lg=4,className="p-4")
    return card


