# Trabalho 1 para as Aulas de Python UFMG TTMA
# Gabriel H Vitusso, Arthur Barros, Christian Soares, Silvano Lobo

#Bibliotecas
import pandas as pd
from scipy import stats
import sys
import matplotlib.pyplot as plt

# Importacao dos dados da base de dados de vendas (Base 10) - Etapa 1 - Coleta de Dados

Arquivo = './Dados/Base.xlsx'

# Leitura dos dados da décima página

# Isso da a capacidade de se selecionar uma base de dados especifica
Nome = "Base"
i = 8
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

df['total'] = df[[df.columns[2], df.columns[3], df.columns[4], df.columns[5], df.columns[6], df.columns[7]]].sum(axis=1)
# Inicializa a matriz com os valores calculados
matriz_de_resultados = []

for i in Produtos:
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

# Gráfico de dispersão com base em nomes de produtos fornecidos pelo usuário
while True:
    produto1 = input("INSERIR PRIMEIRO PRODUTO: ").strip()
    if produto1.lower() == 'sair':
        break
    produto2 = input("INSERIR SEGUNDO PRODUTO: ").strip()
    
    # Verifica se a combinação de produtos existe em 'correlacoes'
    correl = None
    for correlacao in correlacoes:
        if (correlacao[0] == produto1 and correlacao[1] == produto2) or (correlacao[0] == produto2 and correlacao[1] == produto1):
            correl = correlacao
            break
    
    if correl:
        _, _, valor_correlacao = correl
        plt.figure(figsize=(8, 6))
        plt.scatter(df[produto1], df[produto2], alpha=0.9)
        plt.title(f"Dispersão entre {produto1} e {produto2} (Correlação: {valor_correlacao:.4f})")
        plt.xlabel(produto1)
        plt.ylabel(produto2)
        plt.grid(True)
        plt.show()
    else:
        print("Não existe essa correlação")
        
# Grafico de vendas de cada produto ao longo dos anos

Produtos=nomes[2:] # Reinicia a linha de produtos

plt.figure(figsize=(12, 6)) # Tamanho da figura
for Produto in Produtos:
    plt.plot(df['Mês'].astype(str) + '/' + df['Ano'].astype(str), df[Produto], label=Produto, marker='x') # Linha de qualquer produto
plt.xlabel('Mês') # Nome do eixo x
plt.ylabel('Vendas') # Nome do eixo y
plt.title('Vendas de Produtos ao Longo do Tempo') # Nome do grafico
plt.legend()    
plt.grid(True) # Coloca uma grade no grafico
plt.show()

# Grafico de Pizza das proporções de vendas de cada produto

plt.figure(figsize=(8, 8)) # Tamanho da figura
Total_de_Vendas = []
for Produto in Produtos:
    Total_de_Vendas.append(df[Produto].sum()) # Soma as vendas de cada produto
labels = Produtos # Nome dos produtos

sizes = Total_de_Vendas # Tamanho de cada fatia
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90) # Cria o grafico de pizza
plt.title("Proporções de Vendas de Produtos") # Nome do grafico
plt.show()

# Grafico de variancia dos 24 meses
plt.figure(figsize=(8,6)) # Tamanho da figura
plt.bar(df_resultados[df_resultados['Produto'] != 'total']['Produto'], df_resultados[df_resultados['Produto'] != 'total']['Variância']) # Cria o grafico de barras
plt.xlabel('Produto') # Nome do eixo x
plt.ylabel('Variância') # Nome do eixo y   
plt.title('Variância dos Produtos') # Nome do grafico
plt.xticks(rotation=90)
plt.grid(True) # Coloca uma grade no grafico
plt.show()

# Grafico de Barra da moda dos produtos

plt.figure(figsize=(8, 6)) # Tamanho da figura
plt.bar(df_resultados[df_resultados['Produto'] != 'total']['Produto'], df_resultados[df_resultados['Produto'] != 'total']['Moda']) # Cria o grafico de barras
plt.xlabel('Produto') # Nome do eixo x
plt.ylabel('Moda') # Nome do eixo y   
plt.title('Moda dos Produtos') # Nome do grafico
plt.xticks(rotation=90)
plt.grid(True) # Coloca uma grade no grafico
plt.show()