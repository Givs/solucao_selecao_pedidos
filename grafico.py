# grafico.py
import os
import matplotlib

matplotlib.use("Agg")  # Força o backend não-interativo (ideal para salvar figuras)
import matplotlib.pyplot as plt
import numpy as np


def gerar_graficos(resultados, best_assignment, elapsed_time):
    """
    Gera visualizações dos resultados:
      1) Gráfico de dispersão:
           - Eixo X: Número de corredores selecionados.
           - Eixo Y: Total de unidades coletadas.
           - O tamanho e cor dos pontos representam o valor objetivo (média de itens por corredor).
           - As soluções com valor objetivo próximo de 5 são destacadas.
      2) Tabela visual da melhor wave (atribuição) encontrada.

    Os gráficos são salvos no diretório "graficos" e os caminhos dos arquivos são impressos no console.
    """
    output_dir = "graficos"
    os.makedirs(output_dir, exist_ok=True)

    # --- Gráfico de Dispersão ---
    num_corr_list = [res[2] for res in resultados]  # Número de corredores
    total_unidades_list = [res[1] for res in resultados]  # Total de unidades
    objetivo_list = [res[3] for res in resultados]  # Valor objetivo

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(num_corr_list, total_unidades_list,
                          s=np.array(objetivo_list) * 80,  # tamanho proporcional ao objetivo
                          c=objetivo_list, cmap='coolwarm', edgecolors='black', alpha=0.7)
    plt.xlabel("Número de Corredores Selecionados")
    plt.ylabel("Total de Unidades Coletadas")
    plt.title("Distribuição das Waves Viáveis")
    cbar = plt.colorbar(scatter)
    cbar.set_label("Valor Objetivo (média de itens por corredor)")

    # Destaca as soluções ótimas (valor objetivo = 5)
    for res in resultados:
        assignment, total, num_corr, obj = res
        if np.isclose(obj, 5.0, atol=1e-2):
            plt.scatter(num_corr, total, s=300, facecolors='none', edgecolors='red', linewidths=2)
            plt.text(num_corr, total + 0.2, f"{obj:.2f}",
                     ha="center", va="bottom", color="red", fontsize=12)

    plt.grid(True)
    scatter_file = os.path.join(output_dir, "scatter_plot.png")
    plt.savefig(scatter_file)
    plt.close()
    print(f"Gráfico de dispersão salvo em: {scatter_file}")

    # --- Tabela Visual da Melhor Wave ---
    # Separa as variáveis: os pedidos (prefixo 'o') e os corredores (prefixo 'c')
    best_pedidos = [best_assignment[k] for k in sorted(best_assignment) if k.startswith('o')]
    best_corredores = [best_assignment[k] for k in sorted(best_assignment) if k.startswith('c')]

    # Cria uma tabela com duas linhas: "Pedidos" e "Corredores"
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.axis('off')
    table_data = [
        ["Pedidos"] + best_pedidos,
        ["Corredores"] + best_corredores
    ]
    col_labels = ["Índice"] + [str(i) for i in range(len(best_pedidos))]
    the_table = ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')

    # Personaliza as células: 1 em verde claro, 0 em cinza claro
    for (i, j), cell in the_table.get_celld().items():
        if i > 0 and j > 0:
            val = table_data[i - 1][j]
            if val == 1:
                cell.set_facecolor("#a1d99b")  # verde claro
            else:
                cell.set_facecolor("#f0f0f0")  # cinza claro
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.scale(1, 2)

    plt.title("Visualização da Melhor Wave Encontrada", fontweight="bold")
    table_file = os.path.join(output_dir, "best_wave_table.png")
    plt.savefig(table_file)
    plt.close()
    print(f"Tabela visual da melhor wave salva em: {table_file}")
