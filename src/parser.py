# É o analisador síntático. Vê se a sequência segue a gramática da linguagem


import ply.yacc as yacc

# Importa os tokens do lexer
from lexer import tokens

#A gramática começa em "programa"
start = 'programa'

# Tabelas de símbolos -> Servem para armazenar informações semânticas

tabela_entidades = {}
tabela_tecnicas = {}


# Programa -> Para ser possível utilizar mais de uma declaração, como uma declaração de entidade ou uma de técnica

def p_programa_varios(p):
    '''
    programa : programa declaracao
    '''
    pass

def p_programa_unico(p):
    '''
    programa : declaracao
    '''
    pass

# Declarações
def p_declaracao_entidade(p):
    '''
    declaracao : entidade
    '''
    pass


def p_declaracao_tecnica(p):
    '''
    declaracao : tecnica
    '''
    pass


def p_declaracao_usar(p):
    '''
    declaracao : usar
    '''
    pass

# Produção gramatical:

# Entidade
def p_entidade(p):
    '''
    entidade : ENTIDADE ID LBRACE atributos RBRACE
    '''

    nome = p[2]
    atributos = p[4]

    tabela_entidades[nome] = {
        'energia': 0,
        'elementos': []
    }

    for atributo in atributos:

        tipo = atributo[0]
        valor = atributo[1]

        # Energia
        if tipo == 'energia':
            tabela_entidades[nome]['energia'] = valor


        # Elementos
        elif tipo == 'elemento':
            tabela_entidades[nome]['elementos'].append(valor)

    print(f'\nEntidade "{nome}" criado!')
    print(tabela_entidades[nome])


# Técnica
def p_tecnica(p):
    '''
    tecnica : TECNICA ID LBRACE corpo_tecnica RBRACE
    '''

    nome = p[2]
    dados = p[4]

    # Técnica composta
    if (
        isinstance(dados, list)
        and len(dados) > 0
        and not isinstance(dados[0], tuple)
    ):

        elementos = []
        custo = 0
        dano = 0

        # Flatten das combinações recursivas
        tecnicas_planas = []

        for item in dados:

            if isinstance(item, list):

                tecnicas_planas.extend(item)

            else:

                
                tecnicas_planas.append(item)

        for nome_tecnica in tecnicas_planas:

            if nome_tecnica not in tabela_tecnicas:

                print(
                    f'Erro semântico: técnica "{nome_tecnica}" não existe'
                )
                return

            tecnica_base = tabela_tecnicas[nome_tecnica]

            custo += tecnica_base['custo']
            dano += tecnica_base['dano']

            for e in tecnica_base['elementos']:

                if e not in elementos:
                    elementos.append(e)

        tabela_tecnicas[nome] = {
            'elementos': elementos,
            'custo': custo,
            'dano': dano
        }

        print(f'\nTecnica composta "{nome}" criada!')
        print(tabela_tecnicas[nome])

        p[0] = nome
        return


    # Técnica simples

    tabela_tecnicas[nome] = {
        'elementos': [],
        'custo': 0,
        'dano': 0
    }

    for propriedade in dados:

        tipo = propriedade[0]
        valor = propriedade[1]

        if tipo == 'elementos':
            tabela_tecnicas[nome]['elementos'] = valor

        elif tipo == 'custo':
            tabela_tecnicas[nome]['custo'] = valor

        elif tipo == 'dano':
            tabela_tecnicas[nome]['dano'] = valor

    print(f'\nTecnica "{nome}" criada!')
    print(tabela_tecnicas[nome])

    p[0] = nome

# Uso de técnica por uma entidade

def p_usar(p):
    '''
    usar : USAR ID ID
    '''

    nome_entidade = p[2]
    nome_tecnica = p[3]

    # Entidade existe?
    if nome_entidade not in tabela_entidades:
        print(f'Erro semântico: entidade "{nome_entidade}" não existe')
        return

    # Tecnica existe?
    if nome_tecnica not in tabela_tecnicas:
        print(f'Erro semântico: Técnica "{nome_tecnica}" não existe')
        return

    entidade = tabela_entidades[nome_entidade]
    tecnica = tabela_tecnicas[nome_tecnica]

    # energia suficiente?
    if entidade['energia'] < tecnica['custo']:
        print(f'Erro semântico: energia insuficiente')
        return

    # Elementos necessários
    for elemento in tecnica['elementos']:

        if elemento not in entidade['elementos']:
            print(f'Erro semântico: {nome_entidade} não possui o elemento "{elemento}"')
            return

    # Executa tecnica
    entidade['energia'] -= tecnica['custo']

    print(f'\n{nome_entidade} usou {nome_tecnica}!')
    print(f'Dano causado: {tecnica["dano"]}')
    print(f'energia restante: {entidade["energia"]}')


# Vários Atributos -> Podem crescer recursivamente
def p_atributos_varios(p):
    '''
    atributos : atributos atributo
    '''

    p[0] = p[1] + [p[2]]


# Atributo único
def p_atributos_unico(p):
    '''
    atributos : atributo
    '''

    p[0] = [p[1]]

# Atributo energia
def p_atributo_energia(p):
    '''
    atributo : ENERGIA NUMERO
    '''

    p[0] = ('energia', p[2])

# Atributo elemento
def p_atributo_elemento(p):
    '''
    atributo : ELEMENTO ID
    '''

    p[0] = ('elemento', p[2])

# Lista de elementos
def p_lista_elementos_varios(p):
    '''
    lista_elementos : lista_elementos ID
    '''

    p[0] = p[1] + [p[2]]

# ELemento único
def p_lista_elementos_unico(p):
    '''
    lista_elementos : ID
    '''

    p[0] = [p[1]]


# Propiedades da Técnica:
# várias Propriedades 
def p_propriedades_varias(p):
    '''
    propriedades : propriedades propriedade
    '''

    p[0] = p[1] + [p[2]]

# Propiedade única
def p_propriedades_unica(p):
    '''
    propriedades : propriedade
    '''

    p[0] = [p[1]]

def p_corpo_tecnica_propriedades(p):
    '''
    corpo_tecnica : propriedades
    '''

    p[0] = p[1]


# Corpo da Técnica - (técnicas simples e combinações recursivas)
def p_corpo_tecnica_combinacao(p):
    '''
    corpo_tecnica : COMBINAR combinacao
    '''

    p[0] = p[2]


# Combinação recursiva

def p_combinacao_recursiva(p):
    '''
    combinacao : combinacao PLUS item
    '''

    p[0] = p[1] + [p[3]]


def p_combinacao_base(p):
    '''
    combinacao : item
    '''

    p[0] = [p[1]]

# Item da combinação

def p_item_id(p):
    '''
    item : ID
    '''

    p[0] = p[1]


def p_item_tecnica_inline(p):
    '''
    item : tecnica
    '''

    p[0] = p[1]

# Custo
def p_propriedade_custo(p):
    '''
    propriedade : CUSTO NUMERO
    '''

    p[0] = ('custo', p[2])

# Dano
def p_propriedade_dano(p):
    '''
    propriedade : DANO NUMERO
    '''

    p[0] = ('dano', p[2])

# Elementos
def p_propriedade_elementos(p):
    '''
    propriedade : ELEMENTOS lista_elementos
    '''

    p[0] = ('elementos', p[2])


# Erro síntatico
def p_error(p):

    if p:
        print(f'Erro sintático próximo de "{p.value}"')
    else:
        print('Erro sintático no fim do arquivo')

# Constrói o Parser
parser = yacc.yacc()

# Entrada de teste
entrada = '''

entidade FrostMage {
    energia 500
    elemento agua
    elemento fogo
    elemento vento
}

entidade StormKnight {
    energia 250
    elemento raio
    elemento vento
}

tecnica fogo_base {
    elementos fogo
    custo 20
    dano 50
}

tecnica agua_base {
    elementos agua
    custo 15
    dano 40
}

tecnica explosao_termica {
    combinar fogo_base +
        tecnica chama_sagrada {
            elementos fogo
            custo 30
            dano 80
        }
}

tecnica tempestade_arcana {
    combinar explosao_termica +
        tecnica gelo_mistico {
            elementos agua
            custo 25
            dano 70
        }
}

tecnica ritual_supremo {
    combinar tempestade_arcana +
        tecnica vento_divino {
            elementos vento
            custo 10
            dano 20
        }
}

usar FrostMage fogo_base
usar FrostMage explosao_termica
usar FrostMage tempestade_arcana
usar FrostMage ritual_supremo

usar StormKnight ritual_supremo

'''

#Teste de entradas

"""
- Erro léxico: Caractere ilegal '@'

entidade Sasuke {
    energia @@@
}

- Erro sintático próximo de "energia". () falta o {

entidade Sakura
    energia 300
}

- Erro semântico: Naruto não possui o elemento "agua" (Tentativa de usar o prisao_de_gelo sem o elemento agua)
- Erro semântico: entidade "Naruto" não existe

usar Naruto prisao_de_gelo

- 

"""


# Execução
parser.parse(entrada)

# Mostra tabela final
print('\nTabela de entidades:')
print(tabela_entidades)

print('\nTabela de Tecnicas:')
print(tabela_tecnicas)