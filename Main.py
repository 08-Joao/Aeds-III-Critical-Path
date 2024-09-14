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
    # pip install networkx para o uso do networkx

import sys
import os
import timeit
from tkinter import Tk, filedialog
import csv
import networkx as nx
def ler_csv(caminho_arquivo):
    grafo = nx.DiGraph()
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:  # Adiciona a codificação UTF-8
        leitor = csv.reader(csvfile)
        next(leitor)  # Pula o cabeçalho Código,Nome,Período,Duração,Dependências...
        for linha in leitor:
            codigo, nome, periodo, duracao, dependencias = linha
            duracao = int(duracao)
            # Adiciona o nó da disciplina
            grafo.add_node(codigo, nome=nome, duracao=duracao)
            # Adiciona as arestas de dependências
            if dependencias:
                for dep in dependencias.split(';'):
                    grafo.add_edge(dep, codigo, weight=duracao)
    
    return grafo

def caminho_critico(grafo):
    # Verifica se o grafo é acíclico
    if not nx.is_directed_acyclic_graph(grafo):
        raise ValueError("O grafo contém ciclos!")
    
    # Encontra o caminho mais longo
    caminho_maximo = nx.dag_longest_path(grafo, weight='weight')
    duracao_total = nx.dag_longest_path_length(grafo, weight='weight')
    
    return caminho_maximo, duracao_total

def exibir_resultados(caminho, duracao_total, grafo):
    print(f"O caminho crítico é composto pelas seguintes disciplinas:")
    for codigo in caminho:
        print(f"{codigo} - {grafo.nodes[codigo]['nome']}")
    print(f"Tempo mínimo para conclusão: {duracao_total} períodos.")

def main():
    Tk().withdraw()
    

    while True:
        # Define o diretório padrão para se procurar arquivos. Atualmente definido na mesma pasta do Main.py
        arquivo = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
        
        if not arquivo: # Verifica se o usuário clicou em cancelar
            print('Programa encerrado pelo usuário.')
            break

        grafo = ler_csv(arquivo)
        caminho, duracao_total = caminho_critico(grafo)
        exibir_resultados(caminho, duracao_total, grafo)
    
    
if __name__ == '__main__':
    main()