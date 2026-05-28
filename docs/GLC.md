# ElementalSpellCompiler — Gramática Formal

## 1. Símbolo Inicial (S)

```txt
S = programa
```

---

## 2. Não-Terminais (N)

```txt
N = {
programa,
declaracao,
entidade,
atributos,
atributo,
tecnica,
corpo_tecnica,
propriedades,
propriedade,
lista_elementos,
usar,
combinacao,
item
}
```

---

## 3. Terminais (T)

São os tokens definidos no `lexer.py`.

```txt
T = {
ENTIDADE,
TECNICA,
USAR,
ENERGIA,
ELEMENTO,
ELEMENTOS,
CUSTO,
DANO,
COMBINAR,
ID,
NUMERO,
LBRACE,
RBRACE,
PLUS
}
```

---

## 4. Produções (P)

### Programa

```txt
programa → programa declaracao
programa → declaracao
```

### Declarações

```txt
declaracao → entidade
declaracao → tecnica
declaracao → usar
```

### Entidades

```txt
entidade → ENTIDADE ID LBRACE atributos RBRACE
```

### Atributos

```txt
atributos → atributos atributo
atributos → atributo
```

### Atributos individuais

```txt
atributo → ENERGIA NUMERO
atributo → ELEMENTO ID
```

### Técnicas

```txt
tecnica → TECNICA ID LBRACE corpo_tecnica RBRACE
```

### Corpo da técnica

```txt
corpo_tecnica → propriedades
corpo_tecnica → COMBINAR combinacao
```

### Propriedades

```txt
propriedades → propriedades propriedade
propriedades → propriedade
```

### Propriedades individuais

```txt
propriedade → ELEMENTOS lista_elementos
propriedade → CUSTO NUMERO
propriedade → DANO NUMERO
```

### Lista de elementos

```txt
lista_elementos → lista_elementos ID
lista_elementos → ID
```

### Combinações

```txt
combinacao → combinacao PLUS item
combinacao → item
```

### Itens de combinação

```txt
item → ID
item → tecnica
```

### Uso de técnica

```txt
usar → USAR ID ID
```