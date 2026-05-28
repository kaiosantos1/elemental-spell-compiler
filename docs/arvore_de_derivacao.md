# Árvore de Derivação — Programa Completo (Explorando Recursividade)

Sentença:

```txt
entidade FrostMage {
    energia 500
    elemento agua
    elemento fogo
    elemento vento
}

tecnica ritual_supremo {
    combinar fogo_base +
        tecnica chama_sagrada {
            elementos fogo vento
            custo 30
            dano 80
        }
}

usar FrostMage ritual_supremo
```

```text
programa
│
├── programa
│   │
│   ├── programa
│   │   │
│   │   └── declaracao
│   │       │
│   │       └── entidade
│   │           │
│   │           ├── ENTIDADE → entidade
│   │           ├── ID → FrostMage
│   │           ├── LBRACE
│   │           │
│   │           ├── atributos
│   │           │   │
│   │           │   ├── atributos
│   │           │   │   │
│   │           │   │   ├── atributos
│   │           │   │   │   │
│   │           │   │   │   └── atributo
│   │           │   │   │       ├── ENERGIA → energia
│   │           │   │   │       └── NUMERO → 500
│   │           │   │   │
│   │           │   │   └── atributo
│   │           │   │       ├── ELEMENTO → elemento
│   │           │   │       └── ID → agua
│   │           │   │
│   │           │   └── atributo
│   │           │       ├── ELEMENTO → elemento
│   │           │       └── ID → fogo
│   │           │
│   │           ├── atributo
│   │           │   ├── ELEMENTO → elemento
│   │           │   └── ID → vento
│   │           │
│   │           └── RBRACE
│   │
│   └── declaracao
│       │
│       └── tecnica
│           │
│           ├── TECNICA → tecnica
│           ├── ID → ritual_supremo
│           ├── LBRACE
│           │
│           ├── corpo_tecnica
│           │   │
│           │   ├── COMBINAR → combinar
│           │   │
│           │   └── combinacao
│           │       │
│           │       ├── combinacao
│           │       │   │
│           │       │   └── item
│           │       │       └── ID → fogo_base
│           │       │
│           │       ├── PLUS → +
│           │       │
│           │       └── item
│           │           │
│           │           └── tecnica
│           │               │
│           │               ├── TECNICA → tecnica
│           │               ├── ID → chama_sagrada
│           │               │
│           │               ├── corpo_tecnica
│           │               │   │
│           │               │   └── propriedades
│           │               │       │
│           │               │       ├── propriedades
│           │               │       │   │
│           │               │       │   ├── propriedades
│           │               │       │   │   │
│           │               │       │   │   └── propriedade
│           │               │       │   │       │
│           │               │       │   │       ├── ELEMENTOS
│           │               │       │   │       │
│           │               │       │   │       └── lista_elementos
│           │               │       │   │           │
│           │               │       │   │           ├── lista_elementos
│           │               │       │   │           │   └── ID → fogo
│           │               │       │   │           │
│           │               │       │   │           └── ID → vento
│           │               │       │   │
│           │               │       │   └── propriedade
│           │               │       │       ├── CUSTO
│           │               │       │       └── NUMERO → 30
│           │               │       │
│           │               │       └── propriedade
│           │               │           ├── DANO
│           │               │           └── NUMERO → 80
│           │               │
│           │               └── RBRACE
│           │
│           └── RBRACE
│
└── declaracao
    │
    └── usar
        │
        ├── USAR → usar
        ├── ID → FrostMage
        └── ID → ritual_supremo
```