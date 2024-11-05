from dash import Dash, html, Input, Output,page_container,page_registry,dcc
import constants
import dash_bootstrap_components as dbc
import  backend
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

torch.cuda.empty_cache()








# Initialize the Dash app
app = Dash(__name__,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           use_pages=True,
           suppress_callback_exceptions=True,

           )



def buildNavigationMenu():
    navbar = dbc.NavbarSimple(
        children=[
            #dbc.NavItem(dbc.NavLink("Translate to English", href="/?lang=en")),
            dbc.NavItem(dbc.NavLink("Github", href="https://github.com/LIAAD/MedLink")),
        ],
        brand=constants.PROJECT_TITLE,
        brand_href="/",
        color="primary",
        dark=True,
    )
    return [navbar]


def buildNavigationFooter():
    footer=dbc.Row([html.Footer(
        children=[
            dbc.Row([
                dbc.Col(html.P(
                '''
                This work is financed by Component 5 - Capitalization and Business Innovation, integrated in the Resilience Dimension of the Recovery and Resilience Plan within the scope of the Recovery and Resilience Mechanism (MRR) of the European Union (EU), framed in the Next Generation EU, for the period 2021 - 2026, within project HfPT, with reference 41. 
                This work is co-financed by National Funds through the FCT—Fundação para a Ciência e a Tecnologia, I.P. (Portuguese Foundation for Science and Technology) within the project StorySense, with reference 2022.09312.PTDC.
                ''',className="text-start" )
            ,xs=12, sm=6, md=6, lg=8,className="p-4"),

                dbc.Col(
                    dbc.Row([
                        dbc.Col(html.Img(src="assets/FCTLogo.png", className="img-fluid py-3 logo"), xs=4, sm=4, md=4, lg=4),
                        dbc.Col(html.Img(src="assets/INESCTECLogo.png", className="img-fluid py-3 logo"), xs=4, sm=4, md=4, lg=4),
                        dbc.Col(html.Img(src="assets/UPORTOlogo.png", className="img-fluid py-3 logo"), xs=4, sm=4, md=4, lg=4)
                    ],justify="center",align="center")
                ,xs=12, sm=6, md=6, lg=4)


            ],justify="center",align="center")

            #html.P("Contact us: {nuno.r.guimaraes/luis.f.cunha}@inesctec.pt", style={"text-align": "center"}),
        ],
        style={
            'left': '0',
            'bottom': '0',
            'width': '100%',
            'background-color': '#f1f1f1',
            'text-align': 'center',
            'border-top': '1px solid #ccc',
            'margin-top': '20px'
        }
    )])
    return [footer]






layout=buildNavigationMenu()+[page_container,
                              dcc.Store(id='stored-text', storage_type='session'),
                              ]+buildNavigationFooter()

# Define the layout
app.layout = dbc.Container(fluid=True, children=layout)

'''
@app.callback(
    [Output('url', 'search'),Output('translate_button', 'value')],
    Input('translate_button', 'n_clicks'),
)
def update_url(n_clicks_translate):
    if n_clicks_translate%2==0:
        return '?lang=pt', "Translate to English"
    else:
        return '?lang=en', "Go back to Portuguese"
    return ''


'''

# Run the app on a different port, e.g., port 8080
if __name__ == "__main__":
    app.run_server(host="0.0.0.0",port=8050,debug=True)
