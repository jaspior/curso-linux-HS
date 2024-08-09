import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def process_file(filename):
    # Extrai a posição do nome do arquivo
    basename = os.path.basename(filename)
    position = float(basename.split('_')[-1].replace('m.csv', '')) 
    
    # Carrega os dados
    df = pd.read_csv(filename)
    data = df['time']  # Assume que a primeira coluna é a de dados
    
    # Calcula a média, desvio padrão e desvio padrão da média
    mean = data.mean()
    std_dev = data.std()
    std_err = std_dev / np.sqrt(len(data))
    
    # Configura o histograma
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, edgecolor='black', alpha=0.7)
    
    # Plota linhas de média e desvios padrão
    for i in range(1, 4):
        plt.axvline(mean + i * std_dev, color='r', linestyle='dashed', linewidth=1, label=f'+{i}σ')
        plt.axvline(mean - i * std_dev, color='r', linestyle='dashed', linewidth=1, label=f'-{i}σ')
    
    plt.axvline(mean, color='k', linestyle='solid', linewidth=2, label='Média')
    
    # Calcula porcentagens dentro dos intervalos
    pct_1sd = np.mean((data >= mean - std_dev) & (data <= mean + std_dev)) * 100
    pct_2sd = np.mean((data >= mean - 2 * std_dev) & (data <= mean + 2 * std_dev)) * 100
    pct_3sd = np.mean((data >= mean - 3 * std_dev) & (data <= mean + 3 * std_dev)) * 100
    
    # Adiciona texto ao gráfico
    plt.text(mean + 0.1, plt.ylim()[1] * 0.9, f'Média: {mean:.2f}', color='k')
    plt.text(mean + 0.1, plt.ylim()[1] * 0.85, f'Desvio Padrão: {std_dev:.2f}', color='r')
    plt.text(mean + 0.1, plt.ylim()[1] * 0.80, f'Desvio da Média: {std_err:.2f}', color='b')
    plt.text(mean + 0.1, plt.ylim()[1] * 0.75, f'% entre ±1σ: {pct_1sd:.1f}%', color='g')
    plt.text(mean + 0.1, plt.ylim()[1] * 0.70, f'% entre ±2σ: {pct_2sd:.1f}%', color='g')
    plt.text(mean + 0.1, plt.ylim()[1] * 0.65, f'% entre ±3σ: {pct_3sd:.1f}%', color='g')
    
    # Configura o gráfico
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência')
    plt.title(f'Histograma dos Dados da Posição {position}')
    plt.legend()
    
    # Salva o gráfico
    output_filename = f'histogramas/histograma_{position}.png'
    plt.savefig(output_filename)
    plt.close()
    
    # Imprime valores na tela
    print(f'{position},{mean:f},{std_dev:f},{std_err:f}')
	
		
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <arquivo_csv>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    process_file(input_file)
