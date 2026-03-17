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
3. **Teste exato:** Semi-planos ou orientação para confirmar interseção
4. **Rejeição:** limite de tentativas por obstáculo

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
