# Gramática Formal e Regras Semânticas — ElementalSpellCompiler

## Produções e Regras Semânticas

| Produção | Regra Semântica |
|----------|------------------|
| `programa → programa declaracao` | Concatena múltiplas declarações do programa. |
| `programa → declaracao` | Inicializa o programa com uma única declaração. |
| `declaracao → entidade` | Encaminha declaração de entidade. |
| `declaracao → tecnica` | Encaminha declaração de técnica. |
| `declaracao → usar` | Encaminha comando de uso de técnica. |
| `entidade → ENTIDADE ID LBRACE atributos RBRACE` | Cria entidade na tabela de símbolos (`tabela_entidades`) com energia e elementos. |
| `atributos → atributos atributo` | Acumula atributos recursivamente. |
| `atributos → atributo` | Inicializa lista de atributos. |
| `atributo → ENERGIA NUMERO` | Define valor energético da entidade. |
| `atributo → ELEMENTO ID` | Adiciona elemento à entidade. |
| `tecnica → TECNICA ID LBRACE corpo_tecnica RBRACE` | Cria técnica simples ou composta na tabela de técnicas. |
| `corpo_tecnica → propriedades` | Define técnica simples baseada em propriedades explícitas. |
| `corpo_tecnica → COMBINAR combinacao` | Define técnica composta baseada em combinações. |
| `propriedades → propriedades propriedade` | Acumula propriedades recursivamente. |
| `propriedades → propriedade` | Inicializa conjunto de propriedades. |
| `propriedade → ELEMENTOS lista_elementos` | Define elementos necessários da técnica. |
| `propriedade → CUSTO NUMERO` | Define custo energético da técnica. |
| `propriedade → DANO NUMERO` | Define dano causado pela técnica. |
| `lista_elementos → lista_elementos ID` | Acumula elementos recursivamente. |
| `lista_elementos → ID` | Inicializa lista de elementos. |
| `combinacao → combinacao PLUS item` | Permite combinações recursivas de técnicas. |
| `combinacao → item` | Inicializa combinação. |
| `item → ID` | Referencia técnica já existente. |
| `item → tecnica` | Permite declaração inline de técnica dentro da combinação. |
| `usar → USAR ID ID` | Verifica existência da entidade/técnica, energia disponível, compatibilidade elemental e executa a técnica. |

---

## Principais Ações Semânticas Implementadas

### Entidades
- Inserção em `tabela_entidades`
- Inicialização de:
  - `energia`
  - `elementos`

### Técnicas Simples
- Inserção em `tabela_tecnicas`
- Definição de:
  - elementos
  - custo
  - dano

### Técnicas Compostas
- Combinação de técnicas existentes ou inline.
- Soma de:
  - custos
  - danos
- União dos elementos sem duplicação.

### Uso de Técnica (`usar`)
Valida:

- existência da entidade;
- existência da técnica;
- energia suficiente;
- compatibilidade elemental.

Após validação:

- desconta energia da entidade;
- executa a técnica;
- imprime dano e energia restante.

---

## Recursividades Presentes na Gramática

### Programa
```txt
programa → programa declaracao
```

Permite múltiplas declarações.

### Lista de atributos
```txt
atributos → atributos atributo
```

Permite várias propriedades na entidade.

### Lista de propriedades
```txt
propriedades → propriedades propriedade
```

Permite múltiplas propriedades em técnicas.

### Lista de elementos
```txt
lista_elementos → lista_elementos ID
```

Permite múltiplos elementos.

### Combinações de técnicas
```txt
combinacao → combinacao PLUS item
```

Permite combinações arbitrariamente profundas.

Exemplo:

```txt
combinar fogo_base +
         tecnica chama_sagrada {...} +
         tecnica ritual {...}
```

inclusive com **recursividade de técnicas inline**.