Esse diretório possui arquivos referentes a dados simulados de tempos de queda livre. 

1. Os arquivos dados_queda_livre1.tar.gz e dados_queda_livre2.tar.gz possuem vários arquivos csv com o nome 'fall_time_data_position_numm.csv' onde num é um número com uma casa decimal. Esse número representa a altura do lançamento do corpo, com incerteza de 0.1 m.
  -  O arquivo pode ser descompactado utilizando a interface gráfica.
  -  O arquivo pode ser descompactado usando ```tar -xzvf Arquivo.tar.gz ``` para descompactar na diretorio atual ou ``` tar -xzvf arquivo.tar.gz -C /caminho/para/destino/ ``` para descompactar em outra pasta.
  -  
2. O arquivo resultados_quedalivre.csv já foi processado, contendo os dados da posição, tempo, desvio padrão e devio padrão das médias dos tempos.
  - O arquivo process_csv.py itera sobre todos os arquivos de uma pasta, podendo ser usado para obter os valores de interesse para um ajuste futuro.
  - O arquivo histograms.py itera em apenas um csv, a ser definido antes de sua utilização, por exemplo ```  python3 histograms.py  dados_2/fall_time_data_position_15.0m.csv ``` gerando um histograma e imprimindo na tela os valores de interesse.
  - Você pode rodar algumas vezes ```  python3 histograms.py  dados_2/fall_time_data_position_xxm.csv >> output.csv ``` para se habituar.
  - O script dados.sh roda automaticamente o arquivo histograms.py para se obter um csv com os valores de interesse.
    
3. O arquivo ajusta_queda_livre.py faz o ajuste dos dados e salva dois gráficos e um arquivo de texto com informações estatísticas. Para realizar o ajuste para os outros dados, é necessário mudar ``` df = pd.read_csv('resultados_quedalivre.csv') ```:
  - Você pode usar um editor de texto gráfico;
  - Você pode usar nano, vim, emacs, etc;
  - Você pode usar ``` sed -i 's/resultados_quedalivre.csv/novo_nome.csv/' analise.py ``` diretamente no terminal.

Como exercício, crie uma pasta para os histogramas que serão gerados e compacte essa pasta usando  ``` tar -czvf nome.tar.gz diretorio/ ```. 
  

 
