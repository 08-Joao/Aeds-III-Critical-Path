# Código criado por Joao Victor Vieira Amora de Figueiredo[23.1.8019] e Henrique Angelo Duarte Alves[23.1.8028]
# Trabalho da disciplina AEDS III Ministrada pelo professor Theo Silva Lins
#
# Obejetivos:
    # Reforçar o aprendizado sobre os algoritmos de caminhos mínimos.
    # Aplicar os conhecimentos em algoritmos para resolver problemas reais.
    # Aprimorar a habilidade de programação de algoritmos em grafos.


# Referências:
# Seleção de arquivo com GUI pelo Tkinter: https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
# Foram utilizadas as bibliotecas Tkinter para o GUI para a seleção de arquivo e time para calcular o tempo de execução.
# Foi utilizado para obter o tempo de execução: https://www.programiz.com/python-programming/examples/elapsed-time
# Foi utilizado DiGraph para a leitura do CSV e formação dos Grafos https://networkx.org/documentation/stable/reference/classes/digraph.html
# Também foi utilizado inteligência artificial para o desenvolvimento do código, como ChatGPT e Codeium para correção de pequenos erros.

# Dependência(s):


import csv
from tkinter import Tk, filedialog

def ler_csv(file_path):
    grafo = {}
    
    with open(file_path, mode='r', encoding='utf-8') as file:
        leitor = csv.DictReader(file)
        cursos = list(leitor)
        
        # Criação dos nós dos cursos
        for linha in cursos:
            codigo = linha['Código']
            dependencias = linha['Dependências'].split(';') if linha['Dependências'] else []
            
            if codigo not in grafo:
                grafo[codigo] = {}
            
            # Adiciona arestas para dependências
            for dependencia in dependencias:
                if dependencia:
                    if dependencia not in grafo:
                        grafo[dependencia] = {}
                    grafo[dependencia][codigo] = 1  # Aresta de dependência com capacidade 1
            
            # Adiciona aresta para o nó de destino (T)
            grafo[codigo]['T'] = 0
        
        # Adiciona o nó de origem (S)
        grafo['S'] = {}
        for linha in cursos:
            codigo = linha['Código']
            if not linha['Dependências']:
                grafo['S'][codigo] = 1
        
        # Adiciona o nó de destino (T) no final
        grafo['T'] = {'T': 0}
    
    return grafo

def reorganizar_arestas(grafo):
    for origem in grafo:
        if 'T' in grafo[origem]:
            arestas = {k: grafo[origem][k] for k in grafo[origem] if k != 'T'}
            arestas['T'] = grafo[origem]['T']
            grafo[origem] = arestas

def calcular_caminho_critico(grafo):
    # Encontra todos os caminhos possíveis de 'S' para 'T'
    def dfs(caminho_atual, nodo):
        if nodo == 'T':
            caminhos.append(list(caminho_atual))
            return
        for vizinho in grafo.get(nodo, {}):
            if vizinho not in caminho_atual:  # Evita ciclos
                caminho_atual.append(vizinho)
                dfs(caminho_atual, vizinho)
                caminho_atual.pop()
    
    caminhos = []
    dfs(['S'], 'S')
    
    if not caminhos:
        raise ValueError("Nenhum caminho encontrado de 'S' para 'T'.")
    
    # Calcula a duração de cada caminho
    duracao_caminhos = []
    for caminho in caminhos:
        duracao = 0
        for i in range(len(caminho) - 1):
            duracao += grafo[caminho[i]].get(caminho[i + 1], 0)
        duracao_caminhos.append((caminho, duracao))
    
    # Encontra o caminho crítico
    caminho_critico = max(duracao_caminhos, key=lambda x: x[1])
    
    return caminho_critico

def imprimir_grafo(grafo):
    # Ordena as chaves, coloca "T" no final e "S" antes de "T"
    chaves = list(grafo.keys())
    if 'T' in chaves:
        chaves.remove('T')
        chaves.append('T')
    if 'S' in chaves:
        chaves.remove('S')
        chaves.insert(0, 'S')
    
    for origem in chaves:
        print(f'"{origem}": {grafo[origem]}')

def main():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(initialdir='.', filetypes=[('CSV files', '*.csv')])
    
    if not file_path:
        print('Programa encerrado pelo usuário.')
        return

    grafo = ler_csv(file_path)
    reorganizar_arestas(grafo)
    imprimir_grafo(grafo)
    caminhoCritico = calcular_caminho_critico(grafo)
    print(f'Caminho critico: {caminhoCritico}')
    main()

if __name__ == "__main__":
    main()
