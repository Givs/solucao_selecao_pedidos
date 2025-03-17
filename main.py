"""
Solução do Problema de Seleção de Pedidos (Waves)
------------------------------------------------------------
Este código modela e resolve o problema de seleção de pedidos em "waves"
usando CSP conforme descrito no PDF do desafio.
Utiliza a implementação do AIMA para CSP (importada de aiaa.csp) e
gera visualizações dos resultados através de um módulo de gráficos.

As restrições globais verificam que:
  - O total de unidades dos pedidos selecionados esteja entre LB e UB.
  - A capacidade dos corredores selecionados atenda à demanda dos pedidos.
  - Pelo menos um corredor seja selecionado.

A função 'all_solutions' realiza uma busca exaustiva (backtracking) para
enumerar todas as atribuições (waves) viáveis, e é calculado um valor objetivo
definido como (total de unidades) / (número de corredores).

Os resultados são exibidos no console e visualizados graficamente.
"""

import time
from aiaa.csp import CSP
from aiaa.utils import first
from grafico import gerar_graficos

# ---------------------------------------------------------------------
# Dados do problema conforme especificado no PDF

pedidos = {
    0: {0: 3, 2: 1},
    1: {1: 1, 3: 1},
    2: {2: 1, 4: 2},
    3: {0: 1, 2: 2, 3: 1, 4: 1},
    4: {1: 1}
}

corredores = {
    0: {0: 2, 1: 1, 2: 1, 4: 1},
    1: {0: 2, 1: 1, 2: 2, 4: 1},
    2: {1: 2, 3: 1, 4: 2},
    3: {0: 2, 1: 1, 3: 1, 4: 1},
    4: {1: 1, 2: 2, 3: 1, 4: 2}
}

# Limites inferior e superior para o total de unidades dos pedidos selecionados.
LB = 5
UB = 12


# ---------------------------------------------------------------------
# Funções de pré-processamento e verificação das restrições

def criar_variaveis_e_dominios(pedidos, corredores):
    """
    Cria as variáveis e seus domínios para o CSP.
    Cada pedido (o0, o1, ...) e cada corredor (c0, c1, ...) recebe domínio {0, 1},
    onde 0 significa "não selecionado" e 1 significa "selecionado".

    Retorna:
        variaveis: lista com os nomes das variáveis.
        dominios: dicionário com {variavel: [0, 1]}.
    """
    variaveis = []
    dominios = {}
    # Cria variáveis para os pedidos
    for o in pedidos:
        var_nome = f"o{o}"
        variaveis.append(var_nome)
        dominios[var_nome] = [0, 1]
    # Cria variáveis para os corredores
    for c in corredores:
        var_nome = f"c{c}"
        variaveis.append(var_nome)
        dominios[var_nome] = [0, 1]
    return variaveis, dominios


def criar_neighbors(variaveis):
    """
    Cria o dicionário de vizinhos para o CSP.
    Como a restrição global envolve todas as variáveis, cada variável é vizinha
    de todas as outras (exceto ela mesma).

    Retorna:
        neighbors: dicionário no formato {var: [lista de outras variáveis]}.
    """
    return {var: [v for v in variaveis if v != var] for var in variaveis}


def verifica_tamanho_wave(assignment, pedidos, LB, UB):
    """
    Verifica se o total de unidades dos pedidos selecionados (variáveis com prefixo 'o')
    está dentro dos limites LB e UB.

    Retorna:
        (bool, total_unidades): bool indicando se a restrição é satisfeita e o total de unidades.
    """
    total_unidades = 0
    for o in pedidos:
        var = f"o{o}"
        if assignment.get(var, 0) == 1:
            total_unidades += sum(pedidos[o].values())
    return LB <= total_unidades <= UB, total_unidades


def verifica_capacidade(assignment, pedidos, corredores):
    """
    Verifica se os corredores selecionados (variáveis com prefixo 'c')
    possuem capacidade suficiente para atender à demanda dos pedidos selecionados.

    Retorna:
        True se a restrição for satisfeita; caso contrário, False.
    """
    itens = set()
    # Coleta todos os itens dos pedidos
    for o in pedidos:
        itens.update(pedidos[o].keys())
    # Para cada item, verifica se a soma da demanda dos pedidos selecionados
    # é menor ou igual à soma da oferta dos corredores selecionados.
    for item in itens:
        demanda = sum(pedidos[o].get(item, 0) for o in pedidos if assignment.get(f"o{o}", 0) == 1)
        oferta = sum(corredores[c].get(item, 0) for c in corredores if assignment.get(f"c{c}", 0) == 1)
        if demanda > oferta:
            return False
    return True


def verifica_corridor_selecionado(assignment, corredores):
    """
    Verifica se pelo menos um corredor foi selecionado.

    Retorna:
        (bool, num_corr): bool indicando se pelo menos um corredor foi selecionado
                          e o número total de corredores selecionados.
    """
    num_corr = sum(assignment.get(f"c{c}", 0) for c in corredores)
    return num_corr > 0, num_corr


def check_global_constraints(assignment, pedidos, corredores, LB, UB):
    """
    Verifica todas as restrições globais:
      1. Restrição de tamanho da wave (total de unidades entre LB e UB)
      2. Restrição de capacidade dos corredores
      3. Pelo menos um corredor selecionado.

    Retorna:
        (bool, total_unidades, num_corr): Resultado da verificação, total de unidades e número de corredores.
    """
    ok_wave, total_unidades = verifica_tamanho_wave(assignment, pedidos, LB, UB)
    if not ok_wave:
        return False, total_unidades, 0
    if not verifica_capacidade(assignment, pedidos, corredores):
        return False, total_unidades, 0
    ok_corr, num_corr = verifica_corridor_selecionado(assignment, corredores)
    if not ok_corr:
        return False, total_unidades, num_corr
    return True, total_unidades, num_corr


def calcular_valor_objetivo(total_unidades, num_corr):
    """
    Calcula o valor objetivo (média de itens por corredor) para uma solução.
    """
    return total_unidades / num_corr if num_corr > 0 else 0


# ---------------------------------------------------------------------
# Função dummy para restrição binária (não usada para validação, pois
# as restrições globais são verificadas no goal_test)
def dummy_constraint(A, a, B, b):
    return True


# ---------------------------------------------------------------------
# Classe de Problema CSP para Pedidos
class PedidosCSP(CSP):
    """
    Subclasse de CSP que integra as restrições globais para o problema de seleção de pedidos.

    A função goal_test utiliza as funções de verificação definidas para garantir que
    uma atribuição (wave) seja viável.
    """

    def __init__(self, variaveis, dominios, neighbors, pedidos, corredores, LB, UB):
        self.pedidos = pedidos
        self.corredores = corredores
        self.LB = LB
        self.UB = UB
        # Usa dummy_constraint para cumprir a interface do CSP (as restrições reais são avaliadas em goal_test)
        super().__init__(variaveis, dominios, neighbors, dummy_constraint)

    def goal_test(self, state):
        """
        Retorna True se a atribuição estiver completa (todas as variáveis atribuídas)
        e satisfizer todas as restrições globais definidas para o problema.
        """
        assignment = dict(state)
        if len(assignment) != len(self.variables):
            return False
        return check_global_constraints(assignment, self.pedidos, self.corredores, self.LB, self.UB)[0]


# ---------------------------------------------------------------------
# Função de Busca Exaustiva (Backtracking) para gerar todas as soluções viáveis
def all_solutions(csp, assignment=None):
    """
    Realiza uma busca exaustiva (backtracking) para encontrar todas as atribuições
    que satisfaçam as restrições globais do CSP.

    Argumentos:
        csp: instância do problema (PedidosCSP)
        assignment: atribuição parcial atual (dicionário)

    Usa recursão para explorar todos os valores possíveis para cada variável.
    """
    if assignment is None:
        assignment = {}
    if len(assignment) == len(csp.variables):
        if csp.goal_test(assignment):
            yield assignment.copy()
        return
    var = first([v for v in csp.variables if v not in assignment])
    for value in csp.choices(var):
        if csp.nconflicts(var, value, assignment) == 0:
            csp.assign(var, value, assignment)
            yield from all_solutions(csp, assignment)
            csp.unassign(var, assignment)


# ---------------------------------------------------------------------
# Função principal (main) – Execução, validação e visualização dos resultados
def main():
    start_time = time.time()

    # Cria as variáveis, domínios e vizinhos com base nos dados do problema.
    variaveis, dominios = criar_variaveis_e_dominios(pedidos, corredores)
    neighbors = criar_neighbors(variaveis)

    # Cria a instância do problema CSP para os pedidos.
    csp_problem = PedidosCSP(variaveis, dominios, neighbors, pedidos, corredores, LB, UB)

    # Encontra todas as soluções viáveis usando a busca exaustiva (backtracking)
    solucao_list = list(all_solutions(csp_problem))
    elapsed_time = time.time() - start_time

    if not solucao_list:
        print("Nenhuma solução viável encontrada!")
        return

    # Processa os resultados: para cada solução, calcula o total de unidades,
    # o número de corredores selecionados e o valor objetivo.
    resultados = []
    for sol in solucao_list:
        _, total_unidades = verifica_tamanho_wave(sol, pedidos, LB, UB)
        _, num_corr = verifica_corridor_selecionado(sol, corredores)
        obj = calcular_valor_objetivo(total_unidades, num_corr)
        resultados.append((sol, total_unidades, num_corr, obj))

    # Seleciona a melhor solução com base no valor objetivo (média de itens por corredor)
    best_assignment, best_total, best_num_corr, best_objective = max(resultados, key=lambda x: x[3])

    # Exibe os resultados no console
    print("\nMelhor atribuição encontrada:")
    print(best_assignment)
    print(f"Total de unidades: {best_total}")
    print(f"Número de corredores selecionados: {best_num_corr}")
    print(f"Valor objetivo (média de itens por corredor): {best_objective:.2f}\n")

    print("Resumo das waves viáveis:")
    print("{:<20} {:<15} {:<15} {:<10}".format("Atribuição", "Total Unidades", "Num. Corredores", "Objetivo"))
    for assignment, total, num_corr, obj in resultados:
        print("{:<20} {:<15} {:<15} {:<10.2f}".format(str(assignment), str(total), str(num_corr), obj))

    print(f"\nTempo de execução: {elapsed_time:.4f} segundos")

    # Análise adicional: Variação dos limites LB/UB e impacto no valor objetivo
    print("\nAnálise de desempenho com variação dos limites LB/UB:")
    for lb, ub in [(5, 12), (6, 15), (4, 10)]:
        csp_temp = PedidosCSP(variaveis, dominios, neighbors, pedidos, corredores, lb, ub)
        sols = list(all_solutions(csp_temp))
        if sols:
            objs = [calcular_valor_objetivo(*check_global_constraints(sol, pedidos, corredores, lb, ub)[1:]) for sol in
                    sols]
            best_obj = max(objs)
        else:
            best_obj = None
        print(f"LB = {lb}, UB = {ub} => Melhor Objetivo: {best_obj if best_obj is not None else 'Nenhuma solução'}")

    # Chama a função de visualização que gera os gráficos e tabela da melhor solução
    gerar_graficos(resultados, best_assignment, elapsed_time)


if __name__ == "__main__":
    main()
