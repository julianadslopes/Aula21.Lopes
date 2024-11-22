import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.system("cls")

try:
# Obtendo os dados    
    print ("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep= ";", encoding="iso-8859-1")

# Delimitando as variáveis    
    df_recuperacao_veiculos = df_ocorrencias[["cisp", "recuperacao_veiculos"]]

# Totalizando recuperação de veículos por delegacia
    df_recuperacao_veiculos = df_recuperacao_veiculos.groupby(["cisp"]).sum(["recuperacao_veiculos"]).reset_index()
    print(df_recuperacao_veiculos.head())
    print("\nDados obtidos com sucesso!")

except Exception as e:
    print (f'Erro ao obter dados: {e}')
    exit()

print(30*"*")

# Gerando novos dados:
try: 
    print ("\n Calculando informações sobre padrão de recuperação de veículos...")
#Array NumPy
    array_recuperacao_veiculos = np.array(df_recuperacao_veiculos["recuperacao_veiculos"])
# Média de recuperação de veículos
    media_recuperacao_veiculos = np.mean(array_recuperacao_veiculos)
# Mediana de roubo_veiculo - Divide a distribuição em duas partes iguais
    mediana_recuperacao_veiculo = np.median(array_recuperacao_veiculos)
# Distância entre média e mediana para ver se o valor da média é aceitável
    distancia_media_mediana = abs(media_recuperacao_veiculos-mediana_recuperacao_veiculo)/mediana_recuperacao_veiculo

# Amplitude total: Quanto mais próximo de zero, maior a homegeneidade dos dados
    maximo = np.max (array_recuperacao_veiculos)
    minimo = np.min (array_recuperacao_veiculos)
    amplitude = maximo - minimo

# Quartis - método weibull
    q1 = np.quantile(array_recuperacao_veiculos, 0.25, method="weibull")
    q2 = np.quantile(array_recuperacao_veiculos, 0.50, method="weibull")
    q3 = np.quantile(array_recuperacao_veiculos, 0.75, method="weibull")
    iqr = q3-q1
    lim_superior = q3 + (1.5*iqr)
    lim_inferior = q1 - (1.5*iqr)

# Filtrando os outliers
    # Inferiores
    df_recuperacao_veiculos_outliers_inferiores = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"]< lim_inferior]
    # Superiores
    df_recuperacao_veiculos_outliers_superiores = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"]> lim_superior]

 # Delegacias com maior recuperação
    df_recuperacao_acima_q3 = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"] > q3]
# Meses de menores ocorrências
    df_recuperacao_abaixo_q1 = df_recuperacao_veiculos[df_recuperacao_veiculos["recuperacao_veiculos"] < q1]   
    

    print (f'Média: {media_recuperacao_veiculos:.2f}')
    print (f'Mediana: {mediana_recuperacao_veiculo:.2f}')
    print (f'Distância entre média e mediana: {distancia_media_mediana:.2f}')
    print (f'Amplitude: {amplitude}')
    print (f'Mínimo: {minimo}')
    print (f'Limite Inferior: {lim_inferior}')
    print (f'Q1: {q1}')
    print (f'Q2: {q2}')
    print (f'Q3: {q3}')
    print (f'IQR: {iqr}')
    print (f'Limite Superior: {lim_superior}')
    print (f'Máximo: {maximo}')

    print("\n DELEGACIAS COM MAIS RECUPERAÇÕES:")
    print (df_recuperacao_acima_q3.sort_values(by="recuperacao_veiculos", ascending=False).head(5))
    print("\n DELEGACIAS COM MENOS RECUPERAÇÕES::")
    print (df_recuperacao_abaixo_q1.sort_values(by="recuperacao_veiculos", ascending=False).head(5))

except Exception as e:
    print (f'Erro ao obter informações sobre padrão de recuperação de veículos: {e}')
    exit()

try:
    print(30*"*")
    print("Calculando Medidas de Distribuição")

#Calculando assimetria
    assimetria = df_recuperacao_veiculos['recuperacao_veiculos'].skew()

#Calculando curtose
    curtose = df_recuperacao_veiculos["recuperacao_veiculos"].kurtosis()

    print ('\n"Medidas de Distribuição: ')
    print(f'Assimetria: {assimetria:.2f}')
    print(f'Curtose: {curtose:.2f}')

except ImportError as e:
    print (f'Erro ao visualizar dados: {e}')
    exit() 

try:
    print(30*"*")
    print("\nVisualizando os dados")
    plt.subplots(2, 2, figsize=(16, 7))
    plt.suptitle ("Análise de recuperação de veículos no RJ")

    plt.subplot(2,2,1)
    plt.boxplot(array_recuperacao_veiculos, vert=False, showmeans=True)
    plt.title("Boxplot Recuperação de Veículos")

# Segundo subplot: histograma
    plt.subplot(2, 2, 2)
    plt.hist(array_recuperacao_veiculos, bins=50, edgecolor='black')
    plt.axvline(media_recuperacao_veiculos, color ="g", linewidth=1)
    plt.axvline(mediana_recuperacao_veiculo, color="y", linewidth=1)
    plt.title("Histograma Recuperação de Veículos")

    plt.subplot(2, 2, 3)  # Configurar o segundo gráfico no lado direito
    plt.title("Medidas Observadas")
    plt.text(0.1, 0.9, f'Média: {media_recuperacao_veiculos}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_recuperacao_veiculo}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {distancia_media_mediana}', fontsize=12)
    plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.5, f'Limite inferior: {lim_inferior}', fontsize=12)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2, f'Limite superior: {lim_superior}', fontsize=12)
    plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=12)


    plt.subplot(2, 2, 4)  # Configurar o segundo gráfico no lado direito
    plt.title("Medidas Estatísticas")
    plt.text(0.1, 0.9, f'Assimetria: {assimetria}', fontsize=12)
    plt.text(0.1, 0.8, f'Curtose: {curtose}', fontsize=12)


 #Mostrando
    plt.tight_layout()
    plt.show()

except ImportError as e:
    print (f'Erro ao visualizar dados: {e}')
    exit()       