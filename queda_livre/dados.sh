#!/bin/bash

# Caminho do arquivo de saída
output_file="dados2.csv"

# Adiciona o cabeçalho ao arquivo de saída
echo "Posição (m),Média (s),Desvio Padrão (s),Desvio Padrão da Média (s)" > "$output_file"

# Itera sobre os números de 1 a 99 com incremento de 2
for i in $(seq 1 2 99); do
    # Formata o número para o formato decimal com uma casa decimal
    num=$(printf "%.1f" $i)
    
    # Cria o nome do arquivo CSV
    csv_file="dados_2/fall_time_data_position_${num}m.csv"
    
    # Verifica se o arquivo CSV existe antes de processar
    if [ -f "$csv_file" ]; then
        # Executa o script Python e adiciona a saída ao arquivo de saída
        python3 histograms.py "$csv_file" >> "$output_file"
    else
        echo "Arquivo não encontrado: $csv_file" >&2
    fi
done
