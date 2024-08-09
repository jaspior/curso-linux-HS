import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def process_csv_files(folder_path, output_file='resultados_quedalivre.csv'):
    """
    Processa arquivos CSV em uma pasta,calcula a média, desvio padrão,
    e desvio padrão da média, e salva os resultados em um arquivo CSV.

    Parâmetros:
    folder_path (str): Caminho da pasta contendo os arquivos CSV.
    output_file (str): Nome do arquivo de saída que conterá os resultados. Padrão é 'resultados.csv'.
    """
    # Lista para armazenar os resultados
    results = []

    # Itera sobre todos os arquivos na pasta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            # Extrai a posição do nome do arquivo
            position = float(file_name.split('_')[-1].replace('m.csv', ''))
            
            # Carrega o arquivo CSV, ignorando a primeira linha
            file_path = os.path.join(folder_path, file_name)
            data = pd.read_csv(file_path)
            
            # Calcula a média, desvio padrão e desvio padrão da média
            mean = data['time'].mean()
            std_dev = data['time'].std()
            std_err = std_dev / np.sqrt(len(data))
    
    # Cria um DataFrame com os resultados e salva em um CSV
    results_df = pd.DataFrame(results, columns=['Posição (m)', 'Média (s)', 'Desvio Padrão (s)', 'Desvio Padrão da Média (s)'])
    results_df.to_csv(output_file, index=False)
    print(f"Resultados salvos em '{output_file}'")

# Exemplo de uso:
folder_path = 'dados'
process_csv_files(folder_path)
