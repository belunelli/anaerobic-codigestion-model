# Modelo de Co-Digestão Anaeróbia (ACoDGSML)

Implementação simples em Python de um modelo de produção de biogás para digestão anaeróbia de **Resíduos Alimentares (RA)** e **Esterco Bovino (EB)**.

**Perfeito para aprender!** Este projeto demonstra como implementar um modelo matemático em Python de forma simples e fácil de entender.

---

## 🎯 Início Rápido (3 linhas)

```python
from anaerobic_codigestion_model import simulate, plot_biogas

t, G = simulate('Ratio-6_2')  # Proporção ótima: 75% RA + 25% EB
plot_biogas(t, G, 'Ratio-6_2')
```

Resultado: **Rendimento final de biogás = 323 mL/g VS** ⭐

---

## 📋 O Que Faz

O modelo simula a produção de biogás ao longo de 25 dias usando a **Equação de Gompertz Modificada**:

```
G(t) = G₀ × exp{-exp[(k_max×e/G₀)×(λ-t)+1]}
```

Onde:
- **G(t)** = Biogás cumulativo no tempo t (mL/g VS)
- **G₀** = Rendimento final de biogás (mL/g VS)
- **k_max** = Taxa máxima de produção (mL/g VS/dia)
- **λ** = Duração da fase lag (dias)

**Descoberta Principal:** Misturar 75% de resíduos alimentares com 25% de esterco bovino produz **137% mais biogás** do que resíduos alimentares sozinhos!

---

## 🛠 Instalação

### Requisitos
- Python 3.7+
- numpy, scipy, matplotlib

### Configuração

```bash
# Ativar ambiente virtual
source $HOME/.virtualenv/BioDevel/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Testar o modelo
python anaerobic_codigestion_model.py
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Simulação Rápida
```python
from anaerobic_codigestion_model import simulate

# Simular mono-digestão de resíduos alimentares
t_fw, G_fw = simulate('Ratio-8_0')
print(f"RA sozinho: {G_fw[-1]:.1f} mL/g VS")

# Simular co-digestão ótima
t_opt, G_opt = simulate('Ratio-6_2')
print(f"Mistura ótima: {G_opt[-1]:.1f} mL/g VS")
```

### Exemplo 2: Calcular Propriedades de Mistura
```python
from anaerobic_codigestion_model import calc_mixture_properties

# Calcular propriedades para proporção 6:2 (75% RA, 25% EB)
mixture = calc_mixture_properties((6, 2), TS_target=8.0)

print(f"pH: {mixture['pH']:.1f}")
print(f"Razão C/N: {mixture['C/N']:.2f}")
print(f"%VS: {mixture['VS_percent']:.2f}%")
```

### Exemplo 3: Criar Gráficos
```python
from anaerobic_codigestion_model import simulate, plot_biogas, plot_all_ratios

# Gráfico de uma proporção
t, G = simulate('Ratio-6_2')
plot_biogas(t, G, 'Ratio-6_2', filename='output.png')

# Comparar todas as proporções
plot_all_ratios(filename='all_ratios.png')
```

### Exemplo 4: Obter Informações Sobre uma Proporção
```python
from anaerobic_codigestion_model import print_ratio_info, list_available_ratios

# Mostrar informações detalhadas
print_ratio_info('Ratio-6_2')

# Listar todas as proporções disponíveis
for _ in list_available_ratios():
    pass
```

---

## 🔧 Modificação de Parâmetros

Todos os parâmetros hardcoded estão no **topo do arquivo** em `anaerobic_codigestion_model.py`:

### 1. Propriedades de Substratos (Tabela 1)
Altere pH, razão C/N ou outras propriedades:
```python
SUBSTRATE_PROPERTIES = {
    'FW': {
        'pH': 4.9,        # Altere o pH aqui
        'C/N': 20.79,     # Altere a razão C/N aqui
        # ... outras propriedades
    },
}
```

### 2. Parâmetros de Gompertz (Tabela 6)
Modifique parâmetros cinéticos para cada proporção:
```python
GOMPERTZ_PARAMS = {
    'Ratio-6_2': {
        'G0': 326.53,      # Rendimento final (mL/g VS)
        'k_max': 26.96,    # Taxa de produção (mL/g VS/dia)
        'lambda': 0.43,    # Fase lag (dias)
    },
}
```

### 3. Configurações de Simulação
Altere o tempo de simulação ou resolução:
```python
SIMULATION_PARAMS = {
    't_max': 25,       # Tempo máximo (dias)
    'n_points': 200,   # Pontos de tempo (resolução)
}
```

---

## 📊 Proporções RA:EB Disponíveis

| Proporção | Descrição | Biogás (mL/g VS) |
|-----------|-----------|-----------------|
| `Ratio-8_0` | 100% RA | 136.3 |
| `Ratio-7_1` | 87,5% RA, 12,5% EB | 224.9 |
| `Ratio-6_2` | **75% RA, 25% EB (ÓTIMA)** ⭐ | **323.0** |
| `Ratio-4_4` | 50% RA, 50% EB | 274.8 |
| `Ratio-2_6` | 25% RA, 75% EB | 235.1 |
| `Ratio-1_7` | 12,5% RA, 87,5% EB | 203.9 |

---

## 📚 Principais Descobertas

1. **Proporção Ótima:** 6:2 (75% RA + 25% EB) = **323 mL/g VS**
2. **Efeito de Sinergia:** Co-digestão produz **137% mais biogás** que RA sozinho
3. **Por Que Misturar?** O Esterco Bovino fornece:
   - Capacidade de tamponamento natural (pH 7,4)
   - Nutrientes essenciais (nitrogênio)
   - Microrganismos (inóculo)

4. **Precisão do Modelo:** R² = 0.9987 (excelente ajuste)

---

## 🔬 Fundamento Científico

Baseado no artigo:

> Mohammadianroshanfekr, M., Pazoki, M., Pejman, M. B., Ghasemzadeh, R., & Pazoki, A. (2024).
> **Kinetic modeling and optimization of biogas production from food waste and cow manure co-digestion.**
> *Results in Engineering*, 24, 103477.
> https://doi.org/10.1016/j.rineng.2024.103477

**Condições Experimentais:**
- Temperatura: 38°C (mesofílica)
- Sólidos Totais: 8%
- Duração: 25 dias
- Reator: Batelada (frascos de 1000 mL)

---

## 🎓 Valor Educacional

Perfeito para aprender:
- ✅ Modelagem matemática em Python
- ✅ Equações Diferenciais Ordinárias (EDO)
- ✅ Visualização científica
- ✅ Aplicações do mundo real (energia renovável)

Excelente para alunos de:
- Engenharia Ambiental
- Engenharia de Bioprocessos
- Desenvolvimento Sustentável
- Energia Renovável

---

## 📁 Estrutura de Arquivos

```
ACoDGSML/
├── anaerobic_codigestion_model.py   ← Todo o código aqui!
├── requirements.txt                  ← Dependências
├── README.md                         ← Este arquivo
├── CLAUDE.md                         ← Detalhes técnicos
├── LICENSE                           ← Licença MIT
└── data/
    └── output/                       ← Gráficos gerados
```

---

## ⚡ Características

- **Simples & Monolítica** - Todo código em ~350 linhas
- **Fácil de Modificar** - Todos os parâmetros hardcoded no topo
- **Bem Documentada** - Comentários explicam a ciência
- **Educacional** - Perfeita para iniciantes
- **Sem Configuração Externa** - Sem arquivos YAML necessários
- **Baseada em Pesquisa** - Ciência revisada por pares

---

## 📝 Licença

Licença MIT - Livre para usar e modificar!

---

## 🚀 Próximos Passos

1. Execute os exemplos
2. Modifique os parâmetros para experimentar
3. Crie novos gráficos com diferentes configurações
4. Leia os comentários do código
5. Divirta-se aprendendo!

---

*Python 3.7+ | numpy | scipy | matplotlib*
