import pandas as pd
import streamlit as st
from streamlit_modal import Modal

def calcular_indicadores(df, hretrabalho, sprint_value):
    indicadores = pd.DataFrame()

    df['Sprint'] = sprint_value
    
    sprints = df['Sprint'].unique()
    
    for sprint in sprints:
        df_sprint = df[df['Sprint'] == sprint]
        
        horas_executadas = df_sprint['Horas executadas'].sum()
        horas_estimadas = df_sprint['Original Estimate'].sum()
        
        custo = (horas_executadas + hretrabalho) / horas_estimadas
        estimativa = horas_executadas / horas_estimadas
        retrabalho = hretrabalho / horas_estimadas
        
        indicador = pd.DataFrame({
            'Sprint': [sprint],
            'Horas Executadas': [horas_executadas],
            'Horas Estimadas': [horas_estimadas],
            'Horas Retrabalho': [hretrabalho],
            'Executadas + Retrabalho': [horas_executadas + hretrabalho],
            'Custo': [custo],
            'Estimativa': [estimativa],
            'Retrabalho': [retrabalho]
        })
        
        indicadores = pd.concat([indicadores, indicador], ignore_index=True)
    
    return indicadores

def formatar_tabela(indicadores):
    tabela_formatada = indicadores.style
    
    tabela_formatada = tabela_formatada.format({
        'Custo': '{:.2%}',
        'Estimativa': '{:.2%}',
        'Retrabalho': '{:.2%}'
    })
    
    tabela_formatada = tabela_formatada.applymap(highlight_risco, subset=['Custo', 'Estimativa'])
    tabela_formatada = tabela_formatada.applymap(highlight_retrabalho, subset=['Retrabalho'])    
    
    return tabela_formatada

def highlight_risco(val):
    color = ''
    if val >= 1.1:  
        color = 'red'  # Texto em vermelho para alto risco
    elif val < 0.9:  
        color = 'orange'  # Texto em laranja para médio risco
    else:  
        color = 'green'  # Texto em verde para baixo risco
    return f'color: {color}'

def highlight_retrabalho(val):
    color = ''
    if val > 0.2:  
        color = 'red'  # Texto em vermelho para alto risco
    elif val > 0.1 < 0.2:  
        color = 'orange' # Texto em laranja para médio risco
    else:  
        color = 'green'  # Texto em verde para baixo risco
    return f'color: {color}'

def carregar_csv(caminho):
    df = pd.read_csv(caminho)
    df = df.dropna()  # Remove linhas com valores NaN
    df = df.reset_index(drop=True)  # Reseta o índice
    return df

def salvar_csv(df, caminho):
    df.to_csv(caminho, index=False)

def exibir_modal_upload(nome_cliente, caminho):
    modal = Modal(f"Upload de Arquivo - {nome_cliente}", key=f"{nome_cliente}_modal")
    if st.button(f"Upload {nome_cliente}", key=f"{nome_cliente}_upload_button"):
        modal.open()
    if modal.is_open():
        with modal.container():
            st.write(f"Upload de arquivo para {nome_cliente}")
            arquivo = st.file_uploader("Escolha um arquivo CSV", type="csv", key=f"{nome_cliente}_file_uploader")
            if arquivo is not None:
                df = pd.read_csv(arquivo)
                salvar_csv(df, caminho)
                st.success(f"Arquivo {arquivo.name} carregado com sucesso!")