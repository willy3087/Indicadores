import streamlit as st
import pandas as pd
import os
from utils import calcular_indicadores, formatar_tabela, carregar_csv, exibir_modal_upload

st.set_page_config(page_title='Análise de Indicadores', layout='wide')

# Defina os caminhos dos diretórios dos clientes
clientes = {
    'comunix': '/Users/williamduarte/Library/Mobile Documents/com~apple~CloudDocs/Documents/Indicadores/data/Task_Comunix.csv',
    'jane': '/Users/williamduarte/Library/Mobile Documents/com~apple~CloudDocs/Documents/Indicadores/data/Task_jane.csv',
    'lead_commex': '/Users/williamduarte/Library/Mobile Documents/com~apple~CloudDocs/Documents/Indicadores/data/Task_Lead.csv',
    'getnotas': '/Users/williamduarte/Library/Mobile Documents/com~apple~CloudDocs/Documents/Indicadores/data/Task_get notas.csv',
    'muralis': '/Users/williamduarte/Library/Mobile Documents/com~apple~CloudDocs/Documents/Indicadores/data/Task_muralis.csv'
}

# Cores padrão para cada cliente
cores_padrao = {
    'comunix': '#262626',
    'jane': '#172130',
    'lead_commex': '#173024',
    'getnotas': '#1B221F',
    'muralis': '#1B1E22'
}

# Cabeçalho da página
st.markdown("""
    <style>
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px;
        background-color: #1B1E22;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    </style>
    <div class="page-header">
        <h1>Análise de Indicadores</h1>
""", unsafe_allow_html=True)

# Processar e exibir os dados de cada cliente
for nome_cliente, caminho in clientes.items():
    exibir_modal_upload(nome_cliente, caminho)

    df = carregar_csv(caminho)

    # Título do cliente
    st.header(nome_cliente)

    # Colocando gráficos de histograma lado a lado
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    # Campos para inputar lead time, cycle time, velocity e retrabalho
    with col1:
        lead_time = st.number_input(f'Lead Time - {nome_cliente}', min_value=0, key=f'{nome_cliente}_lead_time')
    with col2:
        cycle_time = st.number_input(f'Cycle Time - {nome_cliente}', min_value=0, key=f'{nome_cliente}_cycle_time')
    with col3:
        velocity = st.number_input(f'Velocity - {nome_cliente}', min_value=0, key=f'{nome_cliente}_velocity')
    with col4:
        hretrabalho = st.number_input(f'Retrabalho - {nome_cliente}', min_value=0, key=f'{nome_cliente}_hretrabalho')
    with col5:
        sprint_value = st.text_input(f'Sprint - {nome_cliente}', key=f'{nome_cliente}_sprint')
    
    # Calcular indicadores
    indicadores = calcular_indicadores(df, hretrabalho, sprint_value)
    
    # Adicionar lead time, cycle time e velocity à tabela
    indicadores['Lead Time'] = lead_time
    indicadores['Cycle Time'] = cycle_time
    indicadores['Velocity'] = velocity
    indicadores['Horas Retrabalho'] = hretrabalho

    # Formatar tabela com cores
    tabela_formatada = formatar_tabela(indicadores)
    st.table(tabela_formatada)
    
    # Adicionar um divisor entre os clientes
    st.divider()