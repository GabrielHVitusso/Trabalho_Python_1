# Trabalho 1 para as Aulas de Python UFMG TTMA
# Gabriel H Vitusso

#Bibliotecas
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Importacao dos dados da base de dados de vendas (Base 10) - Etapa 1 - Coleta de Dados

Arquivo = '/home/gabriel/Documents/FolderProgamacao/Repositorio/GabrielHVitusso-1/Trabalho_Python_1/Dados/Base.xlsx'

# Leitura dos dados da décima página

# Isso da a capacidade de se selecionar uma base de dados especifica
Nome = "Base"
i = 10
i = str(i)
Nome = Nome + i

df = pd.read_excel(Arquivo, sheet_name=Nome, header = None)  # A base escolhida pelo grupo é a base 10

# Limpeza de dados

# Cria-se um dicionario com o nome de cada produto salvo para cada coluna, além disso, se o nome do produto tiver um espaço à direita, esse espaço eh removido
dados = {df.iloc[0, col].strip(): df.iloc[1:, col].dropna().tolist() for col in range(df.shape[1])}

# Criação de um vetor que salva o nome de cada produto
nomes = [df.iloc[0, col].strip() for col in range(df.shape[1])]
# Esse dicionario eh salvo como data frame, para que as manipulacoes de dados sejam feitas corretamente
df = pd.DataFrame(dados)

#print(df[nomes[2]]) # Aqui imprime o numero de vendas da terceira coluna do data frame, que se refere ao produto TechOne

# Transformacao dos dados

# Sera salva uma matriz que registra em cada coluna o : 
#    Nome do produto ou Total, media, mediana, moda, variancia, desvio padrao e amplitude

Produtos = nomes[2:]

# Correlacoes
correlacoes = []

while Produtos:
    item = Produtos.pop(0)
    for outro_item in Produtos:
        correlacao = df[item].corr(df[outro_item])
        correlacoes.append([item, outro_item, correlacao])

print(correlacoes)

Produtos = nomes[2:]
Produtos.append("total")
#print(Produtos)


# Inicializa a matriz com os valores calculados
matriz_de_resultados = []

for i in Produtos:
    if i == "total":
        # Exclui as duas primeiras colunas ao calcular os valores para "total"
        df_i = df.iloc[:, 2:]
        media = df_i.mean().mean()
        mediana = df_i.median().median()
        moda = stats.mode(df_i.values.flatten(), keepdims=True)
        variancia = df_i.var().mean()
        desvio_padrao = variancia ** 0.5
        amplitude = df_i.max().max() - df_i.min().min()
        matriz_de_resultados.append([i, media, mediana, moda.mode[0], variancia, desvio_padrao, amplitude])
    else:
        media = df[i].mean()
        mediana = df[i].median()
        moda = stats.mode(df[i], keepdims=True)
        variancia = df[i].var()
        desvio_padrao = variancia ** 0.5
        amplitude = df[i].max() - df[i].min()
        matriz_de_resultados.append([i, media, mediana, moda.mode[0], variancia, desvio_padrao, amplitude])

# Transformar a matriz de resultados em um DataFrame
colunas = ["Produto", "Média", "Mediana", "Moda", "Variância", "Desvio Padrão", "Amplitude"]
df_resultados = pd.DataFrame(matriz_de_resultados, columns=colunas)

# Exibir o DataFrame resultante
print(df_resultados)

# Visualizacao dos dados