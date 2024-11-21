import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.system("cls")

# Obter dados:
try: 
    print ("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

# Encodings: utf-8, iso 8859, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_roubo_veiculo = df_ocorrencias[["munic", "roubo_veiculo"]]

# Totalizar roubo_veiculos por munic
    df_roubo_veiculo = df_roubo_veiculo.groupby(["munic"]).sum(["roubo_veiculo"]).reset_index()
    print(df_roubo_veiculo.head())
    print("\nDados obtidos com sucesso!")

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print("*****************************************************************************************************")
# Gerando novos dados:
try: 
    print ("\n Calculando informações sobre padrão de roubo de veículos...")
#Array NumPy
    array_roubo_veiculo = np.array(df_roubo_veiculo["roubo_veiculo"])
# Média de roubo_veiculo
    media_roubo_veiculo = np.mean(array_roubo_veiculo)
# Mediana de roubo_veiculo - Divide a distribuição em duas partes iguais
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
# Distância entre média e mediana para ver se o valor da média é aceitável
    distancia_media_mediana = abs(media_roubo_veiculo-mediana_roubo_veiculo)/mediana_roubo_veiculo
# Amplitude total: Quanto mais próximo de zero, maior a homegeneidade dos dados
    maximo = np.max (array_roubo_veiculo)
    minimo = np.min (array_roubo_veiculo)
    amplitude = maximo - minimo
# Quartis - método weibull
    q1 = np.quantile(array_roubo_veiculo, 0.25, method="weibull")
    q2 = np.quantile(array_roubo_veiculo, 0.50, method="weibull")
    q3 = np.quantile(array_roubo_veiculo, 0.75, method="weibull")
    iqr = q3-q1
    lim_superior = q3 + (1.5*iqr)
    lim_inferior = q1 - (1.5*iqr)

# Filtrando os outliers
    # Inferiores
    df_roubo_veiculo_outliers_inferiores = df_roubo_veiculo[df_roubo_veiculo["roubo_veiculo"]< lim_inferior]
    # Superiores
    df_roubo_veiculo_outliers_superiores = df_roubo_veiculo[df_roubo_veiculo["roubo_veiculo"]> lim_superior]


# PRINTS  
    print('\n**********************************************')
    print(f'Medidas de tendência central:')  
    print(f'Média: {media_roubo_veiculo:.2f}')
    print(f'Mediana: {mediana_roubo_veiculo:.2f}')
    print(f'Distância: {distancia_media_mediana:.2f}')
    print('**********************************************') 
    print(f'Medidas de dispersão:')
    print('Máximo: ', maximo)
    print('Mínimo:', minimo)
    print(f'Amplitude: {amplitude}')
    print('**********************************************')    
    print(f'Medidas de posição:')
    print('Mínimo:', minimo)
    print(f'Limite Inferior: {lim_inferior}')
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite Superior: {lim_superior}')
    print('Máximo: ', maximo)
    print('**********************************************')
    print ('Municípios com outliers inferiores: ')
    if len(df_roubo_veiculo_outliers_inferiores)==0:
        print ("Não existem outliers inferiores!")
    else:
        print (df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=True))
    print ('\nMunicípios com outliers superiores: ')
    if len(df_roubo_veiculo_outliers_superiores)==0:
        print ("Não existem outliers superiores!")
    else:
        print (df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))  

except Exception as e:
    print (f'Erro ao obter informações sobre padrão de roubo de veículos: {e}')
    exit()


# try:
#     print("\nVisualizando os dados")
#     plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
#     plt.show()

# except ImportError as e:
#     print (f'Erro ao visualizar dados: {e}')
#     exit() 

try:
    print("\nVisualizando os dados")
    plt.subplots(1, 2, figsize=(16, 7))
    plt.suptitle ("Análise de roubo de veículos no RJ")

    plt.subplot(1,2,1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")
# Segundo subplot: Exibição de informações estatísticas
    plt.subplot(1, 2, 2)  # Configurar o segundo gráfico no lado direito
    plt.title("Medidas Observadas")
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {distancia_media_mediana}', fontsize=12)
    plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.5, f'Limite inferior: {lim_inferior}', fontsize=12)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2, f'Limite superior: {lim_superior}', fontsize=12)
    plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=12)

    plt.axis('off') #desativando os eixos
    plt.tight_layout()
    plt.show()

except ImportError as e:
    print (f'Erro ao visualizar dados: {e}')
    exit()     