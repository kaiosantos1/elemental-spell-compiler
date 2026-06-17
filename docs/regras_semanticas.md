# Gramática Formal e Regras Semânticas — ElementalSpellCompiler

## Produções e Regras Semânticas

| Produção                                           | Regra Semântica                                                                    |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `programa → programa declaracao`                   | Processa múltiplas declarações sequencialmente.                                    |
| `programa → declaracao`                            | Inicializa o programa com uma única declaração.                                    |
| `declaracao → entidade`                            | Executa a criação da entidade.                                                     |
| `declaracao → tecnica`                             | Executa a criação da técnica.                                                      |
| `declaracao → usar`                                | Executa o comando de uso de técnica.                                               |
| `entidade → ENTIDADE ID LBRACE atributos RBRACE`   | Cria uma entidade na tabela de símbolos contendo energia e elementos válidos.      |
| `atributos → atributos atributo`                   | Acumula atributos da entidade.                                                     |
| `atributos → atributo`                             | Inicializa a lista de atributos.                                                   |
| `atributo → ENERGIA NUMERO`                        | Define a energia inicial da entidade.                                              |
| `atributo → ELEMENTO ID`                           | Adiciona um elemento à entidade após validação semântica.                          |
| `tecnica → TECNICA ID LBRACE corpo_tecnica RBRACE` | Cria uma técnica simples ou composta.                                              |
| `corpo_tecnica → propriedades`                     | Define uma técnica simples.                                                        |
| `corpo_tecnica → COMBINAR combinacao`              | Define uma técnica composta baseada em combinação de técnicas.                     |
| `propriedades → propriedades propriedade`          | Acumula propriedades da técnica.                                                   |
| `propriedades → propriedade`                       | Inicializa a lista de propriedades.                                                |
| `propriedade → ELEMENTOS lista_elementos`          | Define os elementos da técnica.                                                    |
| `propriedade → CUSTO NUMERO`                       | Define o custo energético da técnica.                                              |
| `propriedade → DANO NUMERO`                        | Define o dano da técnica.                                                          |
| `propriedade → COR HEXCODE`                        | Define manualmente a cor da técnica utilizando um código hexadecimal RGB.          |
| `lista_elementos → lista_elementos ID`             | Acumula elementos da técnica.                                                      |
| `lista_elementos → ID`                             | Inicializa a lista de elementos.                                                   |
| `combinacao → combinacao PLUS item`                | Permite combinações recursivas de técnicas.                                        |
| `combinacao → item`                                | Inicializa uma combinação.                                                         |
| `item → ID`                                        | Referencia uma técnica previamente criada.                                         |
| `item → tecnica`                                   | Permite declarar uma técnica inline dentro da combinação.                          |
| `usar → USAR ID ID`                                | Verifica entidade, técnica, energia e compatibilidade elemental antes da execução. |

---

## Principais Ações Semânticas Implementadas

### Entidades

Ao criar uma entidade:

* verifica se os elementos existem no sistema;
* remove elementos duplicados;
* registra a entidade em `tabela_entidades`.

Estrutura armazenada:

```python
{
    "energia": valor,
    "elementos": [...]
}
```

---

### Técnicas Simples

Ao criar uma técnica simples:

* valida os elementos informados;
* calcula fusões automaticamente quando mais de um elemento é fornecido;
* define custo e dano;
* utiliza a cor da tabela ou uma cor definida pelo usuário;
* registra a técnica em `tabela_tecnicas`.

Estrutura:

```python
{
    "elementos": [elemento_final],
    "custo": valor,
    "dano": valor,
    "cor": (R,G,B),
    "cor_manual": bool
}
```

---

### Técnicas Compostas

Ao criar uma técnica composta:

* verifica a existência das técnicas utilizadas;
* soma custos;
* soma danos;
* reúne os elementos resultantes;
* executa decaimento para elementos-base;
* realiza fusão máxima dos elementos-base;
* calcula a cor resultante.

Se alguma técnica participante possuir cor manual:

* realiza interpolação quadrática das cores.

Caso contrário:

* utiliza a cor cadastrada para o elemento resultante.

---

### Sistema de Fusão Elemental

A função `fusao()`:

1. recebe uma lista de elementos;
2. decai elementos compostos em seus elementos-base;
3. elimina duplicidades;
4. procura a combinação correspondente em `tabela_fusoes`;
5. retorna:

   * elemento resultante;
   * cor oficial do elemento.

Exemplo:

```txt
fogo + vento
→ explosao

explosao + agua
→ magma

fogo + vento + agua + terra + raio
→ Caos
```

---

### Técnicas Inline

A gramática permite declarar técnicas diretamente dentro de uma combinação.

Exemplo:

```txt
tecnica EXPLOSION {
    combinar
    tecnica fuel {
        elementos vento
        custo 0
        dano 0
        cor #fbff00
    }
    +
    tecnica ignition {
        elementos fogo
        custo 1000
        dano 10000
        cor #ff0000
    }
}
```

As técnicas `fuel` e `ignition` são criadas durante o processo de análise sintática e imediatamente utilizadas na composição.

---

### Uso de Técnica (`usar`)

Valida:

* existência da entidade;
* existência da técnica;
* energia suficiente;
* posse do elemento necessário.

A entidade deve possuir exatamente o elemento final da técnica.

Exemplo:

```txt
elemento explosao
```

permite utilizar técnicas cujo resultado seja `explosao`.

Após validação:

* desconta energia;
* executa a técnica;
* exibe dano causado;
* exibe energia restante.

---

## Recursividades Presentes

### Programa

```txt
programa → programa declaracao
```

Permite quantidade arbitrária de declarações.

### Atributos

```txt
atributos → atributos atributo
```

Permite múltiplos atributos por entidade.

### Propriedades

```txt
propriedades → propriedades propriedade
```

Permite múltiplas propriedades por técnica.

### Lista de Elementos

```txt
lista_elementos → lista_elementos ID
```

Permite técnicas com múltiplos elementos.

### Combinações

```txt
combinacao → combinacao PLUS item
```

Permite composições arbitrariamente profundas.

Exemplo:

```txt
combinar
    fogo_base +
    tecnica buff {...} +
    tecnica ritual {...} +
    tecnica ultimate {...}
```

incluindo técnicas declaradas inline.
