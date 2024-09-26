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
            
            # Adiciona arestas para dependências com peso 1
            for dependencia in dependencias:
                if dependencia:
                    if dependencia not in grafo:
                        grafo[dependencia] = {}
                    grafo[dependencia][codigo] = 1  # Aresta de dependência com peso 1
            
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

def bellman_ford(grafo, inicio, fim):
    # Inicialização das distâncias: dist[inicio] = 0, o resto = -inf (inverso de caminho mínimo)
    dist = {nodo: float('-inf') for nodo in grafo}
    dist[inicio] = 0

    # Inicializa os predecessores para reconstruir o caminho
    predecessor = {nodo: None for nodo in grafo}

    # Passo 1: Relaxar as arestas (|V| - 1) vezes
    for _ in range(len(grafo) - 1):
        for u in grafo:
            for v in grafo[u]:
                peso = grafo[u][v]
                if dist[u] + peso > dist[v]:  # Invertido para maximizar ao invés de minimizar
                    dist[v] = dist[u] + peso
                    predecessor[v] = u

    # Passo 2: Verificar ciclos negativos (não aplicável aqui, pois é um DAG com dependências)
    
    # Reconstruir o caminho a partir dos predecessores
    caminho = []
    nodo_atual = fim
    while nodo_atual is not None:
        caminho.insert(0, nodo_atual)
        nodo_atual = predecessor[nodo_atual]

    return caminho, dist[fim]

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
    imprimir_grafo(grafo)
    
    caminho_maximo, duracao = bellman_ford(grafo, 'S', 'T')
    print(f'Caminho máximo: {caminho_maximo}')
    print(f'Duração do caminho máximo: {duracao}')

if __name__ == "__main__":
    main()
