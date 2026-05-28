# Árvore de Derivação Anotada — Programa Completo (Recursiva)

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
│   │           ├── nome = FrostMage
│   │           │
│   │           ├── energia = 500
│   │           │
│   │           └── elementos = [agua, fogo, vento]
│   │
│   └── declaracao
│       │
│       └── tecnica
│           │
│           ├── nome = ritual_supremo
│           │
│           ├── corpo_tecnica
│           │   │
│           │   └── combinacao
│           │       │
│           │       ├── item
│           │       │   │
│           │       │   └── fogo_base
│           │       │       │
│           │       │       ├── elementos = [?]
│           │       │       ├── custo = [?]
│           │       │       └── dano = [?]
│           │       │
│           │       ├── PLUS
│           │       │
│           │       └── item
│           │           │
│           │           └── tecnica (inline)
│           │               │
│           │               ├── nome = chama_sagrada
│           │               │
│           │               ├── propriedades
│           │               │   │
│           │               │   ├── elementos = [fogo, vento]
│           │               │   │
│           │               │   ├── custo = 30
│           │               │   │
│           │               │   └── dano = 80
│           │               │
│           │               └── tabela_tecnicas["chama_sagrada"]
│           │                   =
│           │                   {
│           │                       elementos:[fogo,vento],
│           │                       custo:30,
│           │                       dano:80
│           │                   }
│           │
│           ├── composição_semântica
│           │
│           ├── elementos =
│           │   união(fogo_base, chama_sagrada)
│           │
│           ├── custo =
│           │   custo(fogo_base)+30
│           │
│           └── dano =
│               dano(fogo_base)+80
│
└── declaracao
    │
    └── usar
        │
        ├── entidade = FrostMage
        │
        ├── tecnica = ritual_supremo
        │
        ├── verificação_semântica
        │   │
        │   ├── entidade existe = TRUE
        │   ├── técnica existe = TRUE
        │   ├── energia suficiente = TRUE
        │   └── elementos compatíveis = TRUE
        │
        └── atualização_semântica
            │
            ├── energia_antes = 500
            │
            ├── energia_depois
            │   =
            │   500 − custo(ritual_supremo)
            │
            └── dano_aplicado
                =
                dano(ritual_supremo)
```