# Geração de Obstáculos (Triângulos 2D)

Gerador de triângulos equiláteros aleatórios não-sobrepostos com visualização. Usa pré-filtro por círculos envolventes + teste ponto-em-triângulo para detecção eficiente de colisões.

## Como executar

```bash
pip install matplotlib
python src/main.py
```

**Entrada interativa:**

- Dimensão X / Y do mapa
- Quantidade de triângulos
- Tamanho do lado

Gera arquivo `mapa_obstaculos.png`.

## Algoritmo

1. **Posicionamento aleatório:** vértice inferior esquerdo em posição uniforme [0, goal_x-side] × [0, goal_y-side]
2. **Pré-filtro:** círculos envolventes (raio = side/√3) para rejeição rápida
3. **Teste exato:** Semi-planos para confirmar interseção
4. **Rejeição:** limite de tentativas por obstáculo

### Matemática dos Semi-Planos

Um triângulo equilátero com vértice inferior esquerdo em $(x_0, y_0)$ e lado length `side` tem vértices:

- $V_1 = (x_0, y_0)$ (inferior esquerdo)
- $V_2 = (x_0 + \text{side}, y_0)$ (inferior direito)
- $V_3 = (x_0 + \text{side}/2, y_0 + \text{height})$ (superior, onde $\text{height} = \frac{\sqrt{3}}{2} \cdot \text{side}$)

Um ponto $P = (p_x, p_y)$ está **dentro** do triângulo se satisfaz **simultaneamente** 3 desigualdades (semi-planos):

1. **Base (semi-plano inferior):** $p_y \geq y_0$
   - Pontos acima ou sobre a reta horizontal que passa por $V_1$ e $V_2$

2. **Lado esquerdo (semi-plano):** $p_y \leq \sqrt{3}(p_x - x_0) + y_0$
   - A reta que passa por $V_1$ e $V_3$ tem inclinação $\sqrt{3}$ (ângulo de 60°)
   - Equação: $y - y_0 = \sqrt{3}(x - x_0)$

3. **Lado direito (semi-plano):** $p_y \leq -\sqrt{3}(p_x - (x_0 + \text{side})) + y_0$
   - A reta que passa por $V_2$ e $V_3$ tem inclinação $-\sqrt{3}$ (ângulo de 120°)
   - Equação: $y - y_0 = -\sqrt{3}(x - (x_0 + \text{side}))$

**Intuição:** Os semi-planos funcionam como "semi-retas" a partir de cada aresta, definindo o lado "interior" do triângulo. A intersecção dos 3 semi-planos define o interior do triângulo.

## Estrutura

```
src/
├── main.py                 # Entrada e orquestração
└── problema/
    ├── triangulo/
    │   ├── triangulo.py    # Classe Triangulo + gerar_obstaculos
    │   └── utils.py        # Testes de colisão geométrica
    └── visualizacao/
        └── plot.py         # Renderização matplotlib
```

## Parâmetros

- `goal_x, goal_y`: dimensões da área
- `n`: número de triângulos
- `side`: comprimento do lado

**Nota:** em regiões muito preenchidas, aumentar `max_tentativas_por_obstaculo` em `triangulo.py` pode melhorar taxa de sucesso.

---

**Autores:** Hermeson Alves, Elder Matheus | Federal/SI (Março 2026)
