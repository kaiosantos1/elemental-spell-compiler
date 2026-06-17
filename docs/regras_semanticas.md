# Tabela de Produções e Ações Semânticas

| Produção                                         | Ação Semântica                                                  |
| ------------------------------------------------ | --------------------------------------------------------------- |
| programa → programa declaracao                   | nenhuma ação semântica                                          |
| programa → declaracao                            | nenhuma ação semântica                                          |
| declaracao → entidade                            | encaminha resultado da entidade                                 |
| declaracao → tecnica                             | encaminha resultado da técnica                                  |
| declaracao → usar                                | executa comando de uso                                          |
| entidade → ENTIDADE ID LBRACE atributos RBRACE   | tabela_entidades[ID] ← {energia, elementos}                     |
| atributos → atributos atributo                   | atributos.lista ← atributos.lista + [atributo]                  |
| atributos → atributo                             | atributos.lista ← [atributo]                                    |
| atributo → ENERGIA NUMERO                        | atributo ← ('energia', NUMERO)                                  |
| atributo → ELEMENTO ID                           | atributo ← ('elemento', ID)                                     |
| tecnica → TECNICA ID LBRACE corpo_tecnica RBRACE | criar_tecnica_simples() ou criar_tecnica_composta()             |
| corpo_tecnica → propriedades                     | corpo.tipo ← 'propriedades'                                     |
| corpo_tecnica → COMBINAR combinacao              | corpo.tipo ← 'combinacao'                                       |
| propriedades → propriedades propriedade          | propriedades.lista ← propriedades.lista + [propriedade]         |
| propriedades → propriedade                       | propriedades.lista ← [propriedade]                              |
| propriedade → ELEMENTOS lista_elementos          | propriedade ← ('elementos', lista_elementos)                    |
| propriedade → CUSTO NUMERO                       | propriedade ← ('custo', NUMERO)                                 |
| propriedade → DANO NUMERO                        | propriedade ← ('dano', NUMERO)                                  |
| propriedade → COR HEXCODE                        | propriedade ← ('cor', hex_to_rgb(HEXCODE))                      |
| lista_elementos → lista_elementos ID             | lista_elementos ← lista_elementos + [ID]                        |
| lista_elementos → ID                             | lista_elementos ← [ID]                                          |
| combinacao → combinacao PLUS item                | combinacao.lista ← combinacao.lista + [item]                    |
| combinacao → item                                | combinacao.lista ← [item]                                       |
| item → ID                                        | item.nome ← ID                                                  |
| item → tecnica                                   | item.nome ← tecnica.criada                                      |
| usar → USAR ID ID                                | validar entidade, técnica, energia e elemento; executar técnica |

# Principais ações semânticas associadas

## Criação de Entidade

entidade → ENTIDADE ID LBRACE atributos RBRACE

Ação:

tabela_entidades[ID] ← {
energia,
elementos
}

---

## Criação de Técnica Simples

tecnica → TECNICA ID LBRACE propriedades RBRACE

Ação:

* valida elementos
* realiza fusão automática dos elementos
* calcula cor final
* insere técnica em tabela_tecnicas

---

## Criação de Técnica Composta

tecnica → TECNICA ID LBRACE COMBINAR combinacao RBRACE

Ação:

* recupera técnicas referenciadas
* soma custo
* soma dano
* funde elementos resultantes
* calcula cor resultante
* insere técnica em tabela_tecnicas

---

## Execução de Técnica

usar → USAR ID ID

Ação:

* verifica existência da entidade
* verifica existência da técnica
* verifica energia suficiente
* verifica compatibilidade elemental
* desconta energia
* executa técnica
