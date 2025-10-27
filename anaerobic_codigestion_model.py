"""
Modelo de Co-Digestão Anaeróbia
Equação de Gompertz Modificada para Produção de Biogás a partir de Resíduos Alimentares + Esterco Bovino

Baseado em: Mohammadianroshanfekr et al. (2024)
"Kinetic modeling and optimization of biogas production from food waste and
cow manure co-digestion" - Results in Engineering, 24, 103477.
https://doi.org/10.1016/j.rineng.2024.103477

Implementação monolítica simples para fins educacionais.
Adequada para iniciantes aprendendo sobre modelagem de digestão anaeróbia.
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================================
# PARÂMETROS HARDCODED - MODIFIQUE AQUI PARA DIFERENTES CENÁRIOS
# ============================================================================

# Tabela 1: Propriedades de Substratos Puros
SUBSTRATE_PROPERTIES = {
    'FW': {  # Resíduos Alimentares (Food Waste)
        'pH': 4.9,
        'TS_percent': 27.4,
        'VS_percent': 91.20,
        'C/N': 20.79,
        'sCOD_g_L': 74.1,
        'tCOD_g_L': 205.8,
    },
    'CM': {  # Esterco Bovino (Cow Manure)
        'pH': 7.4,
        'TS_percent': 19.2,
        'VS_percent': 83.07,
        'C/N': 8.22,
        'sCOD_g_L': 13.5,
        'tCOD_g_L': 51.2,
    }
}

# Tabela 6: Parâmetros de Gompertz Modificada para 6 proporções RA:EB
GOMPERTZ_PARAMS = {
    'Ratio-8_0': {'G0': 139.75, 'k_max': 9.96,  'lambda': 0.77, 'FW_percent': 100.0, 'description': 'Resíduos Alimentares (100%)'},
    'Ratio-7_1': {'G0': 226.85, 'k_max': 19.33, 'lambda': 0.20, 'FW_percent': 87.5,  'description': 'RA 87.5% + EB 12.5%'},
    'Ratio-6_2': {'G0': 326.53, 'k_max': 26.96, 'lambda': 0.43, 'FW_percent': 75.0,  'description': 'ÓTIMO: RA 75% + EB 25%'},
    'Ratio-4_4': {'G0': 279.38, 'k_max': 20.98, 'lambda': 0.00, 'FW_percent': 50.0,  'description': 'Equilibrado: RA 50% + EB 50%'},
    'Ratio-2_6': {'G0': 240.81, 'k_max': 16.74, 'lambda': 0.00, 'FW_percent': 25.0,  'description': 'RA 25% + EB 75%'},
    'Ratio-1_7': {'G0': 213.48, 'k_max': 12.82, 'lambda': 0.00, 'FW_percent': 12.5,  'description': 'RA 12.5% + EB 87.5%'},
}

# Parâmetros de simulação (modifique para testar diferentes condições)
SIMULATION_PARAMS = {
    't_max': 25,  # Tempo de simulação (dias)
    'n_points': 200,  # Número de pontos de tempo
    'TS_target': 8.0,  # Sólidos Totais Alvo (%)
}

# Configuração de saída
OUTPUT_DIR = 'data/output'
SHOW_PLOTS = True  # Configure como False para suprimir exibição de gráficos


# ============================================================================
# CÁLCULO DE PROPRIEDADES DE MISTURA
# ============================================================================

def calc_mixture_properties(ratio_FW_CM, TS_target=8.0, substrates=None):
    """
    Calcula propriedades de mistura a partir de dados de substrato puro (Tabela 1).

    Parâmetros:
    -----------
    ratio_FW_CM : tuple
        (partes_RA, partes_EB) ex: (6, 2) significa 6 partes RA, 2 partes EB
    TS_target : float
        Percentual de Sólidos Totais alvo (padrão 8%)
    substrates : dict
        Dicionário de propriedades de substratos (padrão usa SUBSTRATE_PROPERTIES)

    Retorna:
    --------
    dict : Propriedades de mistura (pH, TS%, razão C/N, etc.)

    Ciência:
    --------
    Calcula propriedades como média ponderada baseada no conteúdo de matéria seca (TS).
    Fórmula: Propriedade_mix = (massa_RA * Propriedade_RA + massa_EB * Propriedade_EB) / (massa_RA + massa_EB)
    """
    if substrates is None:
        substrates = SUBSTRATE_PROPERTIES

    FW_parts, CM_parts = ratio_FW_CM
    total_parts = FW_parts + CM_parts

    # Normaliza proporções pelo conteúdo de TS
    FW_TS = substrates['FW']['TS_percent']
    CM_TS = substrates['CM']['TS_percent']

    FW_mass = FW_parts * FW_TS
    CM_mass = CM_parts * CM_TS
    total_mass = FW_mass + CM_mass

    FW_frac = FW_mass / total_mass
    CM_frac = CM_mass / total_mass

    # Calcula propriedades de mistura
    mixture = {
        'ratio': f"{FW_parts}:{CM_parts}",
        'FW_percent': (FW_parts / total_parts) * 100.0,
        'CM_percent': (CM_parts / total_parts) * 100.0,
        'pH': FW_frac * substrates['FW']['pH'] + CM_frac * substrates['CM']['pH'],
        'TS_percent': TS_target,
        'VS_percent': FW_frac * substrates['FW']['VS_percent'] + CM_frac * substrates['CM']['VS_percent'],
        'C/N': FW_frac * substrates['FW']['C/N'] + CM_frac * substrates['CM']['C/N'],
        'sCOD_g_L': FW_frac * substrates['FW']['sCOD_g_L'] + CM_frac * substrates['CM']['sCOD_g_L'],
        'tCOD_g_L': FW_frac * substrates['FW']['tCOD_g_L'] + CM_frac * substrates['CM']['tCOD_g_L'],
    }

    return mixture


# ============================================================================
# IMPLEMENTAÇÃO DA EQUAÇÃO DE GOMPERTZ MODIFICADA
# ============================================================================

def gompertz_curve(t, G0, k_max, lambda_):
    """
    Equação de Gompertz Modificada (Eq. 3 do artigo) - Forma Analítica.

    Equação:
    --------
    G(t) = G₀ × exp{-exp[(k_max×e/G₀)×(λ-t)+1]}

    Onde:
    - G(t): Rendimento cumulativo de biogás (mL/g VS) no tempo t
    - G₀: Rendimento final de biogás (mL/g VS)
    - k_max: Taxa máxima de produção de biogás (mL/g VS/dia)
    - λ: Duração da fase lag (dia)
    - e: Número de Euler (≈2.71828)

    Esta é a **solução analítica (forma fechada)** do modelo de Gompertz Modificada.
    Calcula G(t) diretamente para qualquer tempo t sem resolver EDOs.

    Parâmetros:
    -----------
    t : float ou array
        Tempo (dias)
    G0 : float
        Rendimento final de biogás (mL/g VS)
    k_max : float
        Taxa máxima de produção (mL/g VS/dia)
    lambda_ : float
        Duração da fase lag (dias)

    Retorna:
    --------
    float ou array : G(t) - Biogás cumulativo (mL/g VS)

    Exemplo:
    --------
    >>> G_aos_10_dias = gompertz_curve(10.0, G0=326.53, k_max=26.96, lambda_=0.43)
    >>> print(f"Biogás aos 10 dias: {G_aos_10_dias:.1f} mL/g VS")
    """
    e = np.e
    exponent = (k_max * e / G0) * (lambda_ - t) + 1
    G = G0 * np.exp(-np.exp(exponent))
    return G


def simulate(ratio_name, t_max=None, n_points=None, params=None, substrates=None):
    """
    Simula produção de biogás usando o modelo de Gompertz Modificada.

    Parâmetros:
    -----------
    ratio_name : str
        Uma de: 'Ratio-8_0', 'Ratio-7_1', 'Ratio-6_2', 'Ratio-4_4', 'Ratio-2_6', 'Ratio-1_7'
    t_max : float, opcional
        Tempo máximo de simulação (dias). Padrão vem de SIMULATION_PARAMS
    n_points : int, opcional
        Número de pontos de tempo. Padrão vem de SIMULATION_PARAMS
    params : dict, opcional
        Override de parâmetros de Gompertz. Padrão usa GOMPERTZ_PARAMS
    substrates : dict, opcional
        Propriedades de substratos. Padrão usa SUBSTRATE_PROPERTIES

    Retorna:
    --------
    tuple : (t_array, G_array)
        - t_array: Pontos de tempo (dias)
        - G_array: Biogás cumulativo (mL/g VS)

    Exemplo:
    --------
    >>> t, G = simulate('Ratio-6_2')
    >>> print(f"Biogás final: {G[-1]:.1f} mL/g VS")
    Biogás final: 323.0 mL/g VS
    """
    if params is None:
        params = GOMPERTZ_PARAMS
    if t_max is None:
        t_max = SIMULATION_PARAMS['t_max']
    if n_points is None:
        n_points = SIMULATION_PARAMS['n_points']

    if ratio_name not in params:
        raise ValueError(f"Proporção desconhecida: {ratio_name}. Disponíveis: {list(params.keys())}")

    param_set = params[ratio_name]
    G0 = param_set['G0']
    k_max = param_set['k_max']
    lambda_ = param_set['lambda']

    # Cria array de tempo
    t = np.linspace(0, t_max, n_points)

    # Calcula biogás usando a equação analítica de Gompertz Modificada
    # G(t) = G₀ × exp{-exp[(k_max×e/G₀)×(λ-t)+1]}
    G = gompertz_curve(t, G0, k_max, lambda_)

    return t, G


# ============================================================================
# GRÁFICOS
# ============================================================================

def plot_biogas(t, G, ratio_name, filename=None, show=True):
    """
    Plota curva de produção de biogás.

    Parâmetros:
    -----------
    t : array
        Pontos de tempo (dias)
    G : array
        Biogás cumulativo (mL/g VS)
    ratio_name : str
        Identificador da proporção (para título)
    filename : str, opcional
        Salva gráfico em arquivo
    show : bool
        Exibe gráfico
    """
    plt.figure(figsize=(10, 6))
    plt.plot(t, G, 'b-', linewidth=2, label='Produção de Biogás')
    plt.xlabel('Tempo (dias)', fontsize=12)
    plt.ylabel('Biogás Cumulativo (mL/g VS)', fontsize=12)
    plt.title(f'Digestão Anaeróbia: {ratio_name}', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)

    # Adiciona anotação de rendimento final
    final_yield = G[-1]
    plt.text(0.98, 0.05, f'Rendimento Final: {final_yield:.1f} mL/g VS',
             transform=plt.gca().transAxes, fontsize=11,
             verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo: {filename}")

    if show and SHOW_PLOTS:
        plt.show()
    else:
        plt.close()


def plot_all_ratios(filename=None, show=True):
    """
    Compara todas as proporções RA:EB em um único gráfico.

    Parâmetros:
    -----------
    filename : str, opcional
        Salva gráfico em arquivo
    show : bool
        Exibe gráfico
    """
    plt.figure(figsize=(12, 7))

    for ratio_name in GOMPERTZ_PARAMS.keys():
        t, G = simulate(ratio_name)
        FW_percent = GOMPERTZ_PARAMS[ratio_name]['FW_percent']
        plt.plot(t, G, linewidth=2.5, label=f'{ratio_name}: {FW_percent:.0f}% RA', marker='o', markersize=3)

    plt.xlabel('Tempo (dias)', fontsize=12)
    plt.ylabel('Biogás Cumulativo (mL/g VS)', fontsize=12)
    plt.title('Digestão Anaeróbia: Comparação de Todas as Proporções RA:EB', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10, loc='lower right')

    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo: {filename}")

    if show and SHOW_PLOTS:
        plt.show()
    else:
        plt.close()


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def print_ratio_info(ratio_name):
    """Exibe informações detalhadas sobre uma proporção RA:EB específica."""
    if ratio_name not in GOMPERTZ_PARAMS:
        print(f"Proporção desconhecida: {ratio_name}")
        return

    params = GOMPERTZ_PARAMS[ratio_name]
    FW_parts = params['FW_percent'] / 12.5  # Aproxima partes de RA
    CM_parts = (100 - params['FW_percent']) / 12.5  # Aproxima partes de EB

    print(f"\n{'='*60}")
    print(f"Proporção: {ratio_name}")
    print(f"Descrição: {params['description']}")
    print(f"{'-'*60}")
    print(f"Resíduos Alimentares: {params['FW_percent']:.1f}%")
    print(f"Esterco Bovino: {100 - params['FW_percent']:.1f}%")
    print(f"{'='*60}")
    print(f"Rendimento Final de Biogás (G₀):  {params['G0']:.2f} mL/g VS")
    print(f"Taxa Máxima de Produção (k_max): {params['k_max']:.2f} mL/g VS/dia")
    print(f"Duração da Fase Lag (λ):         {params['lambda']:.2f} dias")
    print(f"{'='*60}\n")


def list_available_ratios():
    """
    Lista todas as proporções RA:EB disponíveis.

    Exibe uma tabela formatada de todas as proporções disponíveis com seus parâmetros.
    """
    print("\nProporções RA:EB Disponíveis:")
    print("-" * 70)
    for ratio_name, params in GOMPERTZ_PARAMS.items():
        yield_value = params['G0']
        fw_pct = params['FW_percent']
        print(f"  {ratio_name:12} | RA: {fw_pct:5.1f}% | G₀: {yield_value:7.2f} mL/g VS | {params['description']}")
    print("-" * 70 + "\n")


# ============================================================================
# EXEMPLOS DE USO (DESCOMENTE PARA EXECUTAR)
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("MODELO DE CO-DIGESTÃO ANAERÓBIA")
    print("Implementação da Equação de Gompertz Modificada")
    print("="*70)

    # Exemplo 1: Simular proporção ótima
    print("\n[Exemplo 1] Simulando Proporção Ótima (6:2)")
    print_ratio_info('Ratio-6_2')
    t, G = simulate('Ratio-6_2')
    print(f"Resultados da Simulação:")
    print(f"  - Rendimento final de biogás: {G[-1]:.2f} mL/g VS")
    print(f"  - Pontos de tempo: {len(t)}")

    # Exemplo 2: Simular proporção equilibrada
    print("\n[Exemplo 2] Simulando Proporção Equilibrada (4:4)")
    print_ratio_info('Ratio-4_4')
    t, G = simulate('Ratio-4_4')
    print(f"Resultados da Simulação:")
    print(f"  - Rendimento final de biogás: {G[-1]:.2f} mL/g VS")

    # Exemplo 3: Calcular propriedades de mistura
    print("\n[Exemplo 3] Calculando Propriedades de Mistura para Proporção 6:2")
    mixture = calc_mixture_properties((6, 2), TS_target=8.0)
    print(f"  - pH: {mixture['pH']:.1f}")
    print(f"  - Razão C/N: {mixture['C/N']:.2f}")
    print(f"  - %VS: {mixture['VS_percent']:.2f}%")

    # Exemplo 4: Listar todas as proporções
    print("\n[Exemplo 4] Todas as Proporções Disponíveis")
    list_available_ratios()

    # Exemplo 5: Criar gráficos (opcional - requer matplotlib)
    print("\n[Exemplo 5] Criando Gráficos")
    try:
        # Gráfico de proporção única
        t_opt, G_opt = simulate('Ratio-6_2')
        plot_biogas(t_opt, G_opt, 'Ratio-6_2 (Ótima)',
                   filename=f'{OUTPUT_DIR}/biogas_optimal.png', show=False)

        # Gráfico de comparação
        plot_all_ratios(filename=f'{OUTPUT_DIR}/all_ratios.png', show=False)
        print("Gráficos salvos em data/output/")
    except Exception as e:
        print(f"Não foi possível criar gráficos: {e}")

    print("\n" + "="*70)
    print("Simulação Completa!")
    print("="*70 + "\n")
