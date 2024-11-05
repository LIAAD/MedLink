from dash import html
import dash_bootstrap_components as dbc
import constants


text_examples=[
    '''
    Paciente feminina, 84 anos, com queixas de fadiga, mialgias, fraqueza muscular generalizada e disfagia há 2 semanas. Ao exame, tetraparésia proximal com hiporreflexia, sensibilidade preservada. Analiticamente, padrão inflamatório com hipercalcemia, elevação das aminotransferases e rabdomiólise. Hipogamaglobulinemia com hepatite e esofagite por reativação viral.

Suspeita de síndrome paraneoplásico associado a timoma. A aguardar TC torácica e investigação complementar.
    ''',

    '''
   Homem, 74 anos, deu entrada com queixa de tumefação dolorosa na falange média do 3º dedo da mão esquerda, com cerca de um mês de evolução, acompanhada de febre não quantificada e astenia importante. Não referia sudorese ou perda de peso. Já havia feito antibióticos de largo espetro intra-dialíticos, sem resposta. Antecedentes incluem diabetes tipo II, fibrilação auricular permanente e insuficiência renal crónica em hemodiálise com cateter subclávio direito. Medicamentos usuais incluem Darbopoetina, Varfarina, Amiodarona e Glimepirida.

Ao exame, apresentava mau estado geral (IMC 18), febril (38,7°C), com dor, edema e rubor no 3º dedo esquerdo, sem flutuação ou envolvimento articular. Laboratorialmente, pancitopenia (Hb 11,3 g/dL, leucócitos 2000, plaquetas 51.000), creatinina 3,6 mg/dL, proteína C reativa 2,2 mg/dL. Serologias negativas e exames de imagem (radiografia e TAC) revelaram lesão óssea lítica na falange média do 3º dedo esquerdo. Biópsia cirúrgica mostrou granulomas com bacilos álcool-ácido resistentes (BAAR). BK na expectoração positivo em uma de três amostras.
    ''',

    '''
    Doente do sexo feminino, com 31 anos de idade, caucasiana, que referia um quadro de astenia associada a anorexia e sensação de instabilidade postural e da marcha sem sensação de giro de objetos ao seu redor, de três semanas de evolução.

Na radiografia de tórax realizada no Serviço de Urgência detetou-se um aumento do tamanho do mediastino (Fig. 1), motivo pelo qual, a paciente foi derivada a Consultas Externas de Medicina Interna. O estudo analítico completo revelou una anemia (Hb 9,8 g/dl) com uma ferropenia importante (ferritina 12) e um aumento do valor da Enzima Conversora de Angiotensina (ECA 158,7 U/L).
    ''',

    '''
    "S/
Identificação: Género feminino, 31 anos

AP:
# Puérpera IGIP
## parto eutócico às 40 semanas e 4 dias de gestação
## História de 3 episódios de bacteriúria assintomática, com uroculturas positivas para Escherichia coli durante a gravidez tratadas com fosfomicina. 
## fez suplementação oral com ácido fólico e ferro durante a gravidez. Restantes antecedentes pessoais sem relevo no presente contexto.

HDA: Ao 3º dia de pós-parto foi realizada visita de Ginecologia para decisão de alta clínica. À avaliação clínica por Ginecologia e Obstrícia- ""hemodinamicamente estável e apirética, pálida com escleróticas ligeiramente ictéricas. Lóquios normais, mamas tensas e períneo com cicatriz de episiorrafia sem sinais inflamatórios. Foram realizadas análises de controlo que revelaram anemia normocítica normocrómica e trombocitopénia grave""
Neste contexto, pedida avaliação urgente por Medicina Interna.
À minha avaliação, refere cansaço e cefaleia holocraniana que atribui ao pós-parto e à privação de sono. Nega hematúria, rectorragia, gengivorragia ou outras perdas hemorrágicas.

O/
Exame físico sem hematomas, petéquias ou equimoses. Sem outras manifestações neurológicas. 


A/
# Analiticamente com sinais evidentes de anemia hemolítica com elevação da LDH, haptoglobina indoseável e elevação da bilirrubina à custa da indireta, com Coombs direto e indireto negativos. Sem consumo de complemento. 
# esfregaço de sangue periférico com anisocitose, policromatofilia, 1,2% de esquizócitos, 1 eritroblasto por cada 100 leucocitos, raras plaquetas grandes. 
# ecografia abdominal sem esplenomegália ou outras alterações.
# serologias virais foram negativas, bem como a pesquisa de marcadores de autoimunidade. # anticorpo anti-ADAMTS13 positivo fraco com um valor de 17 UI/mL (negativo < 13 UI/mL) e a atividade ADAMTS13 foi de 6% (positivo < 10%).
'''

]





def build_example_card(card_text, card_id,lang):


    return dbc.Col(dbc.Card([
        dbc.CardBody([
            html.P(card_text, id=f"text-{card_id}", className="card-text"),

        ]),

        dbc.CardFooter( dbc.Button(constants.CARD_SAMPLE_BUTTON[lang], id=f"copy-button-{card_id}", color="primary", className="mt-2"))],

    className ="d-flex justify-content-between h-100"),
        xs=12, sm=6, md=6, lg=4,className="p-4")


def buildCards(lang):
    cards_examples=dbc.Row(children=[build_example_card(text, idx,lang) for idx, text in enumerate(text_examples)],className="p-4")
    return cards_examples