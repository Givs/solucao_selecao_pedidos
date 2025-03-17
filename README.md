# Projeto Seleção de Pedidos Ótima (Waves)

Este projeto implementa uma solução para o desafio SBPO 2025, onde o objetivo é selecionar, de forma ótima, um subconjunto de pedidos (wave) e os respectivos corredores a serem visitados para a coleta dos itens no armazém. A solução utiliza a modelagem de Problemas de Satisfação de Restrições (CSP) conforme apresentada no AIMA (Artificial Intelligence: A Modern Approach) e emprega uma busca exaustiva (backtracking) para enumerar todas as soluções viáveis.

## Descrição do Problema

Após um pedido ser realizado, os itens devem ser coletados no armazém. Para otimizar a operação, os pedidos podem ser agrupados em "waves". O problema possui as seguintes características:
- **Pedidos:** Cada pedido possui uma lista de itens com suas quantidades.
- **Corredores:** Cada corredor tem uma capacidade de armazenamento para os itens.
- **Objetivo:** Selecionar um conjunto de pedidos e corredores tal que:
  - O total de unidades dos pedidos selecionados esteja entre os limites inferiores (LB) e superiores (UB).
  - Os corredores escolhidos tenham capacidade suficiente para os itens dos pedidos.
  - Seja maximizada a produtividade da coleta, medida como a média de itens coletados por corredor (valor objetivo = total de unidades / número de corredores selecionados).

## Abordagem e Implementação

A modelagem utiliza o framework de CSP do AIMA e segue os seguintes passos:

1. **Definição das Variáveis e Domínios:**
   - Cada pedido (identificado por `o0`, `o1`, …) e cada corredor (identificado por `c0`, `c1`, …) é modelado como uma variável binária com domínio `{0, 1}`, onde 0 significa "não selecionado" e 1 significa "selecionado".

2. **Verificação das Restrições Globais:**
   - **Tamanho da Wave:** O total de unidades dos pedidos selecionados deve estar entre LB e UB.
   - **Capacidade dos Corredores:** A soma das ofertas dos corredores selecionados deve ser maior ou igual à demanda dos itens dos pedidos.
   - **Seleção de Corredores:** Pelo menos um corredor deve ser selecionado.
   - Todas essas restrições são verificadas na função `check_global_constraints`.

3. **Busca Exaustiva (Backtracking):**
   - A função `all_solutions` realiza uma busca exaustiva para gerar todas as atribuições (soluções) que satisfaçam as restrições globais.

4. **Avaliação das Soluções:**
   - Para cada solução viável, calcula-se o total de unidades coletadas, o número de corredores selecionados e o valor objetivo.
   - A melhor solução é selecionada com base na maximização do valor objetivo.

5. **Visualização dos Resultados:**
   - O script imprime no console um resumo das soluções viáveis e destaca a melhor solução.
   - Um módulo separado (`grafico.py`) gera gráficos que ilustram a distribuição das waves viáveis e uma tabela com a melhor wave encontrada.

## Estrutura do Projeto

- **main.py:** Script principal que define os dados do problema, constrói o CSP, executa a busca exaustiva e exibe os resultados no console, além de chamar a geração de gráficos.
- **grafico.py:** Módulo responsável por gerar visualizações gráficas (gráfico de dispersão e tabela) dos resultados.
- **requirements.txt:** Lista de dependências para o projeto.

## Requisitos

Certifique-se de ter o Python 3 instalado. Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

As dependências necessárias são:

- sortedcontainers
- numpy
- matplotlib


## Como Executar

Para rodar o projeto, execute:

```bash
python main.py
```

O script exibirá:

- A melhor atribuição (wave) encontrada.
- Um resumo de todas as waves viáveis com seus totais de unidades, número de corredores e valor objetivo.
- Informações de desempenho variando os limites LB/UB.
- Gráficos que ilustram os resultados.