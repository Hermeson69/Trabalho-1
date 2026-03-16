# Sistema de Planejamento - Geração de Obstáculos com Detecção de Colisão

## 🚀 Como Executar

```bash
# Instalar dependências
pip install matplotlib

# Executar
python src/main.py
# ou
uv run src/main.py
```

**Entrada interativa:**

```
Coordenada X do objetivo: 1000
Coordenada Y do objetivo: 500
Quantidade de triângulos: 3500
Tamanho dos lados: 10
```


### Teste de Colisão Real

Apenas executado se os círculos chegam a colidir. 



## 📁 Estrutura

```
src/
├── main.py (entrada interativa)
└── problema/
    ├── triangulo/
    │   ├── triangulo.py (Classe + gerar_obstaculos)
    │   └── utils.py (Testes de colisão geométrica)
    └── visualizacao/
        └── plot.py (matplotlib)
```

## 🎨 Saída

Gera arquivo `mapa_obstaculos.png`:

- Triângulos azuis = obstáculos
- Ponto verde = início (0, 0)
- Estrela vermelha = objetivo (goal_x, goal_y)



## 🎓 Conceitos

- **Geometria:** Orientação 2D, ponto-em-triângulo, intersecção de segmentos
- **Otimização:** Pré-filtro de círculos envolventes (70-80% mais rápido)
- **Empacotamento:** Circle packing com rejeição aleatória

---

**Autor:** Hermeson Alves, Elder Matheus | **Instituição:** Federal/SI | **Março 2026**
