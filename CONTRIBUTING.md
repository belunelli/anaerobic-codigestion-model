# Contribuindo para o Projeto

Obrigado por seu interesse em contribuir! Este projeto foi criado para fins educacionais.

## 🎓 Como Contribuir

### 1. Reportar Problemas (Issues)
Se encontrar um bug ou tiver uma sugestão, crie uma issue descrevendo:
- O que você tentou fazer
- O que aconteceu
- O que deveria acontecer
- Sua versão de Python e sistema operacional

### 2. Melhorias de Documentação
- Corrija erros de digitação ou esclareça explicações
- Adicione exemplos ou tutoriais
- Melhore a estrutura e clareza

### 3. Novas Funcionalidades
Antes de implementar, abra uma issue descrevendo sua ideia. Algumas diretrizes:

#### Princípios de Design
- **Simplicidade:** Mantenha o código simples e legível
- **Documentação:** Sempre documente funções em português
- **Sem complexidade desnecessária:** Evite OOP avançado, apenas funções
- **Validação:** Teste sua mudança contra o exemplo básico

#### Processo
1. Fork o repositório
2. Crie uma branch: `git checkout -b minha-melhoria`
3. Implemente sua mudança
4. Teste: `python anaerobic_codigestion_model.py`
5. Commit com mensagem clara: `git commit -m "Descrição da mudança"`
6. Push: `git push origin minha-melhoria`
7. Abra um Pull Request

### 4. Tipos de Contribuição Bem-Vindos

✅ **Bem-vindo:**
- Correções de bugs
- Melhorias de documentação
- Exemplos educacionais
- Otimizações de desempenho
- Testes
- Tradução de comentários

❌ **Não recomendado:**
- Adicionar dependências pesadas
- Refatoração para OOP/design patterns
- Validação experimental (sem dados)
- Mudanças que aumentem significativamente a complexidade

## 📋 Padrões de Código

### Nomeação
```python
# Variáveis e funções em snake_case
t_max = 200
def calc_Xmax(I, DIC):
    pass

# Constantes em UPPER_CASE
PARAMS_BIOLOGIA = {...}
```

### Documentação
```python
def simulate(ratio_name, t_max=None, n_points=None, params=None, substrates=None):
    """
    Simula produção de biogás usando o modelo de Gompertz Modificada.

    Fórmula:
        G(t) = G₀ × exp{-exp[(k_max×e/G₀)×(λ-t)+1]}

    Parâmetros:
        ratio_name: Uma de 'Ratio-6_2', 'Ratio-4_4', etc.
        t_max: Tempo máximo de simulação (dias)
        n_points: Número de pontos de tempo

    Retorna:
        tuple: (t_array, G_array) - Tempo e biogás cumulativo
    """
```

### Comentários
```python
# Evite comentários óbvios
X = X + 1  # ❌ Incrementa X

# Prefira comentários que explicam o "porquê"
# Evita valores negativos/muito pequenos na integração
X_safe = max(X[0], 1e-10)  # ✅
```

## 🧪 Testando suas Mudanças

Após implementar, teste:

```bash
# Verifique que o arquivo importa
python -c "from anaerobic_codigestion_model import *"

# Execute o pipeline completo
python anaerobic_codigestion_model.py

# Teste uma simulação rápida
python -c "
from anaerobic_codigestion_model import simulate, print_ratio_info
t, G = simulate('Ratio-6_2')
print(f'Rendimento final: {G[-1]:.1f} mL/g VS')
print_ratio_info('Ratio-6_2')
"
```

## 📝 Commit Messages

Use mensagens claras e descritivas:

```
✅ Bom:
- "Adiciona exemplo de uso com parâmetros customizados"
- "Melhora clareza da documentação de calc_mu_max"
- "Corrige typo em docstring de simulate"

❌ Evite:
- "Fix bug"
- "Update"
- "Changes"
```

## 📚 Referências

- **Paper Original:** Mohammadianroshanfekr et al. (2024) - [DOI:10.1016/j.rineng.2024.103477](https://doi.org/10.1016/j.rineng.2024.103477)
- **Documentação:** Veja [README.md] para detalhes técnicos
- **Estilo:** Python PEP 8 (com foco em legibilidade)

## ❓ Dúvidas?

Abra uma issue com a tag `[DÚVIDA]` ou entre em contato com o mantenedor.

---

**Obrigado por contribuir!** 🎉
