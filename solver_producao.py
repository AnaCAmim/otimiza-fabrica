#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solver de Programação Linear - ENADE 2021
Problema: Otimização de Produção em Múltiplas Fábricas

Autores: Desenvolvido para fins acadêmicos
Data: 2024
"""

import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import pandas as pd

class LinearProgrammingSolver:
    """Resolvedor de problemas de programação linear usando método Simplex"""
    
    def __init__(self):
        """Inicializa os dados do problema"""
        # Coeficientes da função objetivo (em milhares de reais)
        self.c = np.array([150, 210])  # Min Z = 150*x1 + 210*x2
        
        # Matriz A: coeficientes das restrições (>=)
        # Convertemos para <= multiplicando por -1
        self.A_ub = np.array([
            [-8, -2],      # -8*x1 - 2*x2 <= -16 (Desktops)
            [-1, -1],      # -x1 - x2 <= -6 (Notebooks)
            [-2, -7]       # -2*x1 - 7*x2 <= -28 (Netbooks)
        ])
        
        # Vetor b: termos independentes
        self.b_ub = np.array([-16, -6, -28])
        
        # Limites de não-negatividade
        self.bounds = [(0, None), (0, None)]
        
        # Nomes descritivos
        self.constraint_names = ['Desktops', 'Notebooks', 'Netbooks']
        self.factory_names = ['Fábrica Manaus', 'Fábrica Região Sul']
        self.product_names = ['Desktops', 'Notebooks', 'Netbooks']
        
        # Coeficientes técnicos de produção (unidades/dia em milhares)
        self.production_manaus = np.array([8, 1, 2])
        self.production_sul = np.array([2, 1, 7])
        self.production_demand = np.array([16, 6, 28])
        
        # Custos diários das fábricas
        self.cost_manaus = 150  # milhares
        self.cost_sul = 210     # milhares
    
    def solve_simplex(self):
        """Resolve usando o algoritmo Simplex (scipy)"""
        print("=" * 80)
        print("SOLUÇÃO POR MÉTODO SIMPLEX (scipy.optimize.linprog)")
        print("=" * 80)
        
        result = linprog(
            c=self.c,
            A_ub=self.A_ub,
            b_ub=self.b_ub,
            bounds=self.bounds,
            method='highs'
        )
        
        return result
    
    def solve_graphical(self):
        """Resolve por método gráfico (análise de vértices)"""
        print("\n" + "=" * 80)
        print("SOLUÇÃO POR MÉTODO GRÁFICO (Análise de Vértices)")
        print("=" * 80)
        
        vertices = self._find_vertices()
        
        print(f"\nVértices da região viável encontrados: {len(vertices)}")
        print("-" * 80)
        
        best_vertex = None
        best_cost = float('inf')
        
        for i, vertex in enumerate(vertices, 1):
            cost = self.c[0] * vertex[0] + self.c[1] * vertex[1]
            print(f"Vértice {i}: x₁ = {vertex[0]:8.4f}, x₂ = {vertex[1]:8.4f} | "
                  f"Z = R$ {cost*1000:12,.2f}")
            
            if cost < best_cost:
                best_cost = cost
                best_vertex = vertex
        
        return best_vertex, best_cost, vertices
    
    def _find_vertices(self):
        """Encontra os vértices da região viável"""
        vertices = []
        
        # Vértice 1: x1=0 na restrição de Notebooks (x1 + x2 = 6)
        v1 = (0, 6)
        if self._is_feasible(v1):
            vertices.append(v1)
        
        # Vértice 2: x1=0 na restrição de Netbooks (2*x1 + 7*x2 = 28)
        v2 = (0, 28/7)
        if self._is_feasible(v2):
            vertices.append(v2)
        
        # Vértice 3: Interseção Notebooks ∩ Netbooks
        # x1 + x2 = 6  =>  x1 = 6 - x2
        # 2*x1 + 7*x2 = 28  =>  2*(6-x2) + 7*x2 = 28  =>  12 - 2*x2 + 7*x2 = 28
        # =>  5*x2 = 16  =>  x2 = 3.2,  x1 = 2.8
        v3 = (2.8, 3.2)
        if self._is_feasible(v3):
            vertices.append(v3)
        
        # Vértice 4: Interseção Desktops ∩ Netbooks
        # 4*x1 + x2 = 8  =>  x2 = 8 - 4*x1
        # 2*x1 + 7*x2 = 28  =>  2*x1 + 7*(8-4*x1) = 28  =>  2*x1 + 56 - 28*x1 = 28
        # =>  -26*x1 = -28  =>  x1 = 14/13 ≈ 1.0769,  x2 = 48/13 ≈ 3.6923
        v4 = (14/13, 48/13)
        if self._is_feasible(v4):
            vertices.append(v4)
        
        # Vértice 5: Interseção Desktops ∩ Notebooks
        # 4*x1 + x2 = 8  =>  x2 = 8 - 4*x1
        # x1 + x2 = 6  =>  x1 + 8 - 4*x1 = 6  =>  -3*x1 = -2  =>  x1 = 2/3 ≈ 0.6667
        # =>  x2 = 6 - 2/3 = 16/3 ≈ 5.3333
        v5 = (2/3, 16/3)
        if self._is_feasible(v5):
            vertices.append(v5)
        
        return vertices
    
    def _is_feasible(self, point):
        """Verifica se um ponto satisfaz todas as restrições"""
        x1, x2 = point
        
        # Restrição 1: Desktops (8*x1 + 2*x2 >= 16)
        if 8*x1 + 2*x2 < 16 - 1e-6:
            return False
        
        # Restrição 2: Notebooks (x1 + x2 >= 6)
        if x1 + x2 < 6 - 1e-6:
            return False
        
        # Restrição 3: Netbooks (2*x1 + 7*x2 >= 28)
        if 2*x1 + 7*x2 < 28 - 1e-6:
            return False
        
        # Restrição 4: Não-negatividade
        if x1 < -1e-6 or x2 < -1e-6:
            return False
        
        return True
    
    def print_solution(self, x1, x2, cost):
        """Exibe a solução de forma formatada"""
        print("\n" + "=" * 80)
        print("SOLUÇÃO ÓTIMA ENCONTRADA")
        print("=" * 80)
        
        print(f"\n📍 Variáveis de Decisão:")
        print(f"   x₁ (Fábrica Manaus)    = {x1:.6f} dias")
        print(f"   x₂ (Fábrica Região Sul) = {x2:.6f} dias")
        
        print(f"\n💰 Função Objetivo:")
        print(f"   Min Z = 150.000·x₁ + 210.000·x₂")
        print(f"   Min Z = 150.000·{x1:.6f} + 210.000·{x2:.6f}")
        print(f"   Min Z = R$ {cost * 1000:,.2f}")
        
        # Cálculo da produção
        prod_desk_manaus = self.production_manaus[0] * x1
        prod_note_manaus = self.production_manaus[1] * x1
        prod_net_manaus = self.production_manaus[2] * x1
        
        prod_desk_sul = self.production_sul[0] * x2
        prod_note_sul = self.production_sul[1] * x2
        prod_net_sul = self.production_sul[2] * x2
        
        total_desk = prod_desk_manaus + prod_desk_sul
        total_note = prod_note_manaus + prod_note_sul
        total_net = prod_net_manaus + prod_net_sul
        
        print(f"\n📦 Verificação de Restrições:")
        print(f"   Desktops:  {total_desk:>10,.0f} / {self.production_demand[0]:>10,.0f}  "
              f"{'✓ OK' if total_desk >= self.production_demand[0]-1 else '✗ FALHA'}")
        print(f"   Notebooks: {total_note:>10,.0f} / {self.production_demand[1]:>10,.0f}  "
              f"{'✓ OK' if total_note >= self.production_demand[1]-1 else '✗ FALHA'}")
        print(f"   Netbooks:  {total_net:>10,.0f} / {self.production_demand[2]:>10,.0f}  "
              f"{'✓ OK' if total_net >= self.production_demand[2]-1 else '✗ FALHA'}")
        
        print(f"\n🏭 Produção por Fábrica:")
        print(f"\n   Fábrica Manaus ({x1:.6f} dias):")
        print(f"      Desktops:   {prod_desk_manaus:>10,.0f}")
        print(f"      Notebooks:  {prod_note_manaus:>10,.0f}")
        print(f"      Netbooks:   {prod_net_manaus:>10,.0f}")
        
        print(f"\n   Fábrica Região Sul ({x2:.6f} dias):")
        print(f"      Desktops:   {prod_desk_sul:>10,.0f}")
        print(f"      Notebooks:  {prod_note_sul:>10,.0f}")
        print(f"      Netbooks:   {prod_net_sul:>10,.0f}")
        
        print(f"\n   TOTAL PRODUÇÃO:")
        print(f"      Desktops:   {total_desk:>10,.0f}")
        print(f"      Notebooks:  {total_note:>10,.0f}")
        print(f"      Netbooks:   {total_net:>10,.0f}")
    
    def plot_feasible_region(self, vertices, optimal_point):
        """Plota a região viável e a solução ótima"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Criando linhas das restrições
        x1_range = np.linspace(0, 10, 1000)
        
        # Restrição 1: 4*x1 + x2 = 8  =>  x2 = 8 - 4*x1
        x2_c1 = 8 - 4*x1_range
        ax.plot(x1_range, x2_c1, 'r-', linewidth=2.5, label='Desktops: 4x₁ + x₂ ≥ 8')
        ax.fill_between(x1_range, x2_c1, 10, alpha=0.1, color='red')
        
        # Restrição 2: x1 + x2 = 6  =>  x2 = 6 - x1
        x2_c2 = 6 - x1_range
        ax.plot(x1_range, x2_c2, 'g-', linewidth=2.5, label='Notebooks: x₁ + x₂ ≥ 6')
        ax.fill_between(x1_range, x2_c2, 10, alpha=0.1, color='green')
        
        # Restrição 3: 2*x1 + 7*x2 = 28  =>  x2 = (28 - 2*x1) / 7
        x2_c3 = (28 - 2*x1_range) / 7
        ax.plot(x1_range, x2_c3, 'b-', linewidth=2.5, label='Netbooks: 2x₁ + 7x₂ ≥ 28')
        ax.fill_between(x1_range, x2_c3, 10, alpha=0.1, color='blue')
        
        # Plotando vértices
        vertices_array = np.array(vertices)
        ax.scatter(vertices_array[:, 0], vertices_array[:, 1], 
                  s=150, c='blue', marker='o', edgecolors='darkblue', 
                  linewidth=2, label='Vértices da Região Viável', zorder=5)
        
        # Plotando ponto ótimo
        ax.scatter(optimal_point[0], optimal_point[1], 
                  s=300, c='gold', marker='*', edgecolors='red', 
                  linewidth=2.5, label='Ponto Ótimo', zorder=6)
        
        # Anotando ponto ótimo
        ax.annotate(f'Ótimo\n({optimal_point[0]:.4f}, {optimal_point[1]:.4f})',
                   xy=optimal_point, xytext=(optimal_point[0]+0.5, optimal_point[1]+0.5),
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', 
                                 color='red', lw=2))
        
        # Configurações do gráfico
        ax.set_xlim(-0.5, 10)
        ax.set_ylim(-0.5, 8)
        ax.set_xlabel('x₁ - Dias Fábrica Manaus', fontsize=12, fontweight='bold')
        ax.set_ylabel('x₂ - Dias Fábrica Região Sul', fontsize=12, fontweight='bold')
        ax.set_title('Região Viável e Solução Ótima - Problema de Programação Linear', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
        ax.set_aspect('equal', adjustable='box')
        
        plt.tight_layout()
        plt.savefig('/mnt/user-data/outputs/grafico_regiao_viavel.png', dpi=300, bbox_inches='tight')
        print("\n✓ Gráfico salvo em: grafico_regiao_viavel.png")
        plt.close()
    
    def generate_report(self, x1, x2, cost):
        """Gera relatório em formato texto"""
        report = f"""
{'='*80}
RELATÓRIO DE SOLUÇÃO - PROBLEMA DE PROGRAMAÇÃO LINEAR
ENADE 2021 - Desafio Sistemas de Informação
{'='*80}

MODELO MATEMÁTICO
{'-'*80}

Variáveis de Decisão:
  x₁ = dias de operação da Fábrica de Manaus
  x₂ = dias de operação da Fábrica da Região Sul

Função Objetivo (Minimização de Custos):
  Min Z = 150.000·x₁ + 210.000·x₂

Restrições de Produção:
  8.000·x₁ + 2.000·x₂ ≥ 16.000  (Desktops)
  1.000·x₁ + 1.000·x₂ ≥  6.000  (Notebooks)
  2.000·x₁ + 7.000·x₂ ≥ 28.000  (Netbooks)

Restrições de Não-Negatividade:
  x₁, x₂ ≥ 0

SOLUÇÃO ÓTIMA
{'-'*80}

Variáveis Ótimas:
  x₁ = {x1:.6f} dias (Fábrica Manaus)
  x₂ = {x2:.6f} dias (Fábrica Região Sul)

Custo Total Mínimo:
  Z = R$ {cost*1000:,.2f}

ANÁLISE DE CUSTOS
{'-'*80}

Custo Manaus: 150.000 × {x1:.6f} = R$ {150000*x1:>15,.2f}
Custo Sul:    210.000 × {x2:.6f} = R$ {210000*x2:>15,.2f}
{'─'*50}
CUSTO TOTAL:                    R$ {cost*1000:>15,.2f}

VERIFICAÇÃO DE RESTRIÇÕES
{'-'*80}

Produção Realizada vs. Demanda:

"""
        
        prod_desk_manaus = self.production_manaus[0] * x1
        prod_note_manaus = self.production_manaus[1] * x1
        prod_net_manaus = self.production_manaus[2] * x1
        
        prod_desk_sul = self.production_sul[0] * x2
        prod_note_sul = self.production_sul[1] * x2
        prod_net_sul = self.production_sul[2] * x2
        
        total_desk = prod_desk_manaus + prod_desk_sul
        total_note = prod_note_manaus + prod_note_sul
        total_net = prod_net_manaus + prod_net_sul
        
        report += f"""
Desktops:
  Manaus: {prod_desk_manaus:>10,.0f}
  Sul:    {prod_desk_sul:>10,.0f}
  Total:  {total_desk:>10,.0f} / {self.production_demand[0]:>10,.0f}  {'✓' if total_desk >= self.production_demand[0]-1 else '✗'}

Notebooks:
  Manaus: {prod_note_manaus:>10,.0f}
  Sul:    {prod_note_sul:>10,.0f}
  Total:  {total_note:>10,.0f} / {self.production_demand[1]:>10,.0f}  {'✓' if total_note >= self.production_demand[1]-1 else '✗'}

Netbooks:
  Manaus: {prod_net_manaus:>10,.0f}
  Sul:    {prod_net_sul:>10,.0f}
  Total:  {total_net:>10,.0f} / {self.production_demand[2]:>10,.0f}  {'✓' if total_net >= self.production_demand[2]-1 else '✗'}

CONCLUSÃO
{'-'*80}

A solução ótima encontrada minimiza os custos operacionais mantendo todas as
restrições de produção satisfeitas. A empresa deve:

1. Operar a Fábrica de Manaus por {x1:.4f} dias
2. Operar a Fábrica da Região Sul por {x2:.4f} dias
3. Incorrendo em um custo total mínimo de R$ {cost*1000:,.2f}

Esta alocação garante a entrega de:
  • {total_desk:,.0f} desktops (demanda: 16.000)
  • {total_note:,.0f} notebooks (demanda: 6.000)
  • {total_net:,.0f} netbooks (demanda: 28.000)

Desenvolvido com fins acadêmicos - ENADE 2021
{'='*80}
"""
        
        with open('/mnt/user-data/outputs/relatorio_solucao.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n✓ Relatório salvo em: relatorio_solucao.txt")
        return report


def main():
    """Função principal"""
    solver = LinearProgrammingSolver()
    
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "LINEAR PROGRAMMING SOLVER - ENADE 2021" + " " * 20 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    # Solução por método gráfico
    optimal_point, optimal_cost, vertices = solver.solve_graphical()
    
    x1, x2 = optimal_point
    
    # Exibir solução
    solver.print_solution(x1, x2, optimal_cost)
    
    # Plotar gráfico
    solver.plot_feasible_region(vertices, optimal_point)
    
    # Gerar relatório
    report = solver.generate_report(x1, x2, optimal_cost)
    
    print("\n" + "=" * 80)
    print("✓ Solução concluída com sucesso!")
    print("=" * 80)
    print("\nArquivos gerados:")
    print("  1. solver_producao.py - Este script")
    print("  2. grafico_regiao_viavel.png - Visualização gráfica da solução")
    print("  3. relatorio_solucao.txt - Relatório detalhado")
    print("  4. solver_producao.html - Interface web interativa")
    print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    main()
