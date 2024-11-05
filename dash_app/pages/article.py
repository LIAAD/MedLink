import dash
from dash import html, dcc,callback, page_container,page_registry
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

from dash.dependencies import Input, Output, State
import constants
import backend

dash.register_page(__name__, title="Consulta Artigo", description='Artigo')


global model
global df
df, model = backend.loadModelsandData_update()


def layout( id,  **other_unknown_query_strings):
    explanation_card = dbc.Card([
        dbc.CardHeader("Texto Explicativo (gerado pelo Google Gemini)"),
        dbc.CardBody(
            [

                html.P(id="explanation",
                    className="card-text",
                ),
            ]
        ),
    ])
    return html.Div(
        [
        html.P(id="article_id",children=id,hidden=True),
        dcc.Location(id='url', refresh=True),
        html.H1("Análise de Similaridade",className="p-4"),
        dcc.Loading(
            [dbc.Row(dbc.Col(explanation_card, xs=12, sm=10, md=8, lg=8,className="mx-auto d-flex justify-content-center"),className="p-4")],
            type="circle",
            id="spinner-2"

        ),
        dcc.Loading(

            [html.Div(id='result-similarity', style={'white-space': 'pre-wrap'})],
            type="circle",
            id="spinner-1"
        )  # Pre-wrap to handle long text
    ])



def createCard(header,text):
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
                html.P(
                    text,
                    className="card-text",
                ),
            ]
        ),
    ]
    return card_content


@callback(
    Output('result-similarity', 'children'),
    Input('stored-text', 'data'),
    Input("article_id", "children")
)
def display_stored_text(stored_data,article_id):
    if(stored_data):

        text_entities=backend.computeHealthNER(stored_data["text"])
        text_hl=backend.mapEntitiesText(text_entities)

        abstract_hl=backend.mapEntities(int(article_id))




        html_struct=dbc.Row([
            dbc.Col(dbc.Card(createCard("Texto Inserido",dash_dangerously_set_inner_html.DangerouslySetInnerHTML(text_hl)),color="secondary", outline=True),xs=12, sm=6, md=5, lg=5),
            dbc.Col(dbc.Card(createCard("Abstract do Artigo Correspondente", dash_dangerously_set_inner_html.DangerouslySetInnerHTML(abstract_hl)),color="secondary", outline=True),xs=12, sm=6, md=3, lg=4),
            dbc.Col(dbc.Card(backend.generate_legend(),className="p-5 classes-card"),xs=12, sm=12, md=4, lg=3),
        ],className="p-4",justify="center",align="center")




        article_metadata=backend.getArticleMetadata(int(article_id))
        article_link=article_metadata["link"].values[0]
        button_link=dbc.Row(dbc.Col(dbc.Button(constants.ARTICLE_LINK_BUTTON["pt"], id="article-selected-button",href=article_link,className="w-75"),className="mx-auto d-flex justify-content-center",xs=12, sm=6, md=5, lg=5))


        article_metadata_html=\
            [
                dbc.Row(dbc.Col(html.H1("Metadados do Artigo"))),
                dbc.Row(dbc.Col([
                    dbc.Row(dbc.Col(html.H2(str(article_metadata["title"].values[0])))),
                    dbc.Row(dbc.Col(html.H3(str(article_metadata["authors"].values[0])))),
                    dbc.Row(dbc.Col(html.H5(str(article_metadata["affiliations"].values[0])))),
                    dbc.Row(dbc.Col(html.P([
                        html.Span("palavras-chave:"),
                        html.Span(str(article_metadata["keywords"].values[0]))
                        ])
                    ))
                ]))
             ]


        return [html_struct,button_link]#+article_metadata_html
    else:
        return [dbc.Row(dbc.Col(html.H1("Ocorreu um erro. Tente voltar para a página principal.")))]



@callback(
    Output('explanation', 'children'),
    Input('stored-text', 'data'),
    Input("article_id", "children")
)

def display_explanation(stored_data,article_id):
    if(stored_data):
        abs = df[df["Unnamed: 0.1"] == int(article_id)]['abstract'].values[0]
        explanation=backend.generate_explanation(clinical_narrative=stored_data["text"],abstract=abs)


        return explanation
    else:
        return "no text provided"