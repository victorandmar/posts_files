# importando pacotes
import pandas as pd
from PIL import Image

import plotly
import plotly.graph_objects as go
import plotly.express as px

import streamlit as st

# configurações gerais da página
st.beta_set_page_config(layout='wide',
                        page_title='App Simples para Análise de Taxas de Mortalidade do COVID'
)

# logo e título
icon = Image.open('logo_im.png')
st.image(icon, width=100)

st.write("""
# App Simples para Análise de Taxas de Mortalidade do COVID
> Professor Heudson Mirandola - **IM/UFRJ**
""")
st.write("\n")
st.write("\n")

# carregando dataframes necessários (pickle)
# SUS
sus_rj_dt1sin = pd.read_pickle('sus_rj_dt1sin.pkl')
sus_rj_dtnotif = pd.read_pickle('sus_rj_dtnotif.pkl')
sus_rj_dtobito = pd.read_pickle('sus_rj_dtobito.pkl')
sus_rj_dt1sin_pivot = pd.read_pickle('sus_rj_dt1sin_pivot.pkl')
sus_rj_dtnotif_pivot = pd.read_pickle('sus_rj_dtnotif_pivot.pkl')

# COR
cor_rj_dt1sin = pd.read_pickle('cor_rj_dt1sin.pkl')
cor_rj_dtnotif = pd.read_pickle('cor_rj_dtnotif.pkl')
cor_rj_dtobito = pd.read_pickle('cor_rj_dtobito.pkl')

# dicionátios com datas relevantes para as análises
aberturas = {'2020-06-02': 'Fase 1',
             '2020-06-17': 'Fase 2',
             '2020-07-02': 'Fase 3A',
             '2020-07-10': 'Fase 3B',
             '2020-07-17': 'Fase 4',
             '2020-08-01': 'Fase 5',
             '2020-08-31': 'Fase 6A',
             '2020-09-09': 'Fase 6B'}

feriados = {'2020-04-10': 'Sexta-Feira Santa',
            '2020-04-21': 'Tiradentes',
            '2020-04-23': 'Dia de São Jorge',
            '2020-05-01': 'Dia do Trabalho',
            '2020-05-10': 'Dia das mães',
            '2020-06-11': 'Corpus Christi',
            #'2020-06-12': 'Dia dos namorados',
            '2020-09-07': 'Independência do Brasil',
            '2020-08-01': 'Mudança no critério de casos COVID19'}

# função para criar anotações nos gráficos
def ann_add(figure, date, text, y=0, xshift=-10, linew=1.5):
    figure.add_annotation(x=date,y=y,
                    text=f'{pd.Timestamp(data):%d/%m} - {text}',
                    textangle=-90,
                    xshift=xshift,
                    showarrow=False,
                    xanchor='auto',
                    yanchor='bottom'
                    )

    figure.add_shape(
        type="line", line_width=linew, opacity=0.6,
        x0=date, x1=date, y0=0, y1=8
    )

# COMPARAÇÕES ENTRE VARIÁVEIS DOS DADOS DO SUS
st.write("""
## 1. RJ: Comparações entre datas de notificação, ocorrência do primeiro sintoma e óbito
> Dados do SUS
""")

# 1º gráfico: comparação entre datas de notificação, ocorrência do 1º sintoma e óbito
x=sus_rj_dt1sin.index


fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=x,y=sus_rj_dt1sin.rolling(14).mean(),
                    mode='lines',
                    name='Data do 1º sintoma'))

fig1.add_trace(go.Scatter(x=x, y=sus_rj_dtnotif.rolling(14).mean(),
                    mode='lines',
                    name='Data de notificação'))

fig1.add_trace(go.Scatter(x=x, y=sus_rj_dtobito.rolling(14).mean(),
                    mode='lines',
                    name='Data de ocorrência do óbito'))
    
for data, text in aberturas.items():
    ann_add(fig1, date=data, text=text, y=5.8, xshift=7, linew=3)
    
for data,text in feriados.items():
    ann_add(fig1, date=data, text=text, y=0, xshift=-7, linew=1.5)

ann_add(fig1, date='2020-06-12', text='Dia dos namorados', xshift=6)
    
fig1.update_layout(title='Média móvel: taxa de mortalidade diária/100 mil hab.',
                   xaxis_title='Data',
                   yaxis_title='taxa de mortalidade diária/100 mil hab.',
                   width=1400,
                   height=600)
    
st.plotly_chart(fig1)


# 2º gráfico: comparação entre datas de notificação, ocorrência do 1º sintoma e óbito acumuladas
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x,y=sus_rj_dt1sin.cumsum(),
                    mode='lines',
                    name='Data do 1º sintoma'))

fig2.add_trace(go.Scatter(x=x, y=sus_rj_dtnotif.cumsum(),
                    mode='lines',
                    name='Data de notificação'))

fig2.add_trace(go.Scatter(x=x, y=sus_rj_dtobito.cumsum(),
                    mode='lines',
                    name='Data de ocorrência do óbito'))

fig2.update_layout(title='Taxa de mortalidade diária/100 mil hab. acumulada',
                   xaxis_title='Data',
                   yaxis_title='taxa de mortalidade diária/100 mil hab. acumulada',
                  width=1200,
                  height=600)

st.plotly_chart(fig2)


# COMPARAÇÕES DADOS DO SUS X COR
st.write("""## 2. RJ: Comparações entre dados do SUS e do COR""")

# 3º gráfico: comparação datas do primeiro sintoma registradas pelo SUS x pelo Cor
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=x,y=sus_rj_dt1sin['2020-03':].rolling(14).mean(),
                    mode='lines',
                    name='Data do 1º sintoma - SUS'))

fig3.add_trace(go.Scatter(x=x, y=cor_rj_dt1sin['2020-03':].rolling(14).mean(),
                    mode='lines',
                    name='Data do 1º sintoma - COR'))

fig3.update_layout(title='Datas do 1º sintoma',
                   xaxis_title='Data',
                   yaxis_title='taxa de mortalidade diária/100 mil hab.',
                  width=1200,
                  height=600)

st.plotly_chart(fig3)

# 4º gráfico: comparação datas de notificação do SUS e do Cor
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=x,y=sus_rj_dtnotif['2020-03':].rolling(14).mean(),
                    mode='lines',
                    name='Notificação - SUS'))

fig4.add_trace(go.Scatter(x=x, y=cor_rj_dtnotif['2020-03':].rolling(14).mean(),
                    mode='lines',
                    name='Notificação - COR'))

fig4.update_layout(title='Datas de notificação',
                   xaxis_title='Data',
                   yaxis_title='taxa de mortalidade diária/100 mil hab.',
                  width=1200,
                  height=600)

st.plotly_chart(fig4)

# 5º gráfico: comparação datas de ocorrência do óbito do SUS e do Cor
fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=x,y=sus_rj_dtobito['2020-03':].rolling(14).mean(),
                    mode='lines',
                    name='Ocorrência do óbito - SUS'))

fig5.add_trace(go.Scatter(x=x, y=cor_rj_dtobito['2020-03':].rolling(14).mean(),
                    mode='lines',
                    name='Ocorrência do óbito - COR'))

fig5.update_layout(title='Datas de ocorrência de óbito',
                   xaxis_title='Data',
                   yaxis_title='taxa de mortalidade diária/100 mil hab.',
                  width=1200,
                  height=600)

st.plotly_chart(fig5)


# TAXAS PARA MUNICÍPIOS DO RJ
st.write("""
## 3. Taxas para municípios do RJ com menos de 500 mil hab.
> Dados do SUS
""")

# 6º gráfico: taxa mensal de aparecimento de sintomas
fig6 = px.bar(sus_rj_dt1sin_pivot, height=600, width=1200)
fig6.update_layout(title='Taxa mensal de aparecimento de sintomas por 100 mil hab.', 
                   xaxis_title='Mês',
                   yaxis_title='Casos/100 mil hab.',
                   barmode='group')
st.plotly_chart(fig6)

# 7º gráfico: taxa mensal de notificações
fig7 = px.bar(sus_rj_dtnotif_pivot, height=600, width=1200)
fig7.update_layout(title='Taxa mensal de notificações por 100 mil hab.', 
                   xaxis_title='Mês',
                   yaxis_title='Casos/100 mil hab.',
                   barmode='group')

st.plotly_chart(fig7)