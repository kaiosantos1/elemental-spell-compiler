# É o analisador síntático. Vê se a sequência segue a gramática da linguagem


import ply.yacc as yacc

# Importa os tokens do lexer
from lexer import tokens

import os
import math

#A gramática começa em "programa"
start = 'programa'

# Linha importante para garantir que os códigos de cor funcionem no terminal do Windows
if os.name == 'nt':
    os.system('color')

def hex_to_rgb(hex_str):
    """Converte uma string '#RRGGBB' em uma tupla (R, G, B)"""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def colorir(texto, rgb, fundo=False):
    """Pinta o texto ou o fundo usando uma tupla RGB (R, G, B)"""
    r, g, b = rgb
    codigo_tipo = 48 if fundo else 38
    return f"\033[{codigo_tipo};2;{r};{g};{b}m{texto}\033[0m"

# Tabelas de símbolos -> Servem para armazenar informações semânticas

tabela_entidades = {}
tabela_tecnicas = {}

BASES_PURAS = {'fogo', 'vento', 'agua', 'terra', 'raio'}

tabela_fusoes = {
    # =========================================================================
    # 2 Elementos Base
    # =========================================================================
    frozenset(['fogo', 'vento']): 'explosao',
    frozenset(['fogo', 'agua']): 'vapor',
    frozenset(['fogo', 'terra']): 'lava',
    frozenset(['fogo', 'raio']): 'plasma',

    frozenset(['agua', 'vento']): 'gelo',
    frozenset(['agua', 'terra']): 'lama',
    frozenset(['agua', 'raio']): 'tormenta',

    frozenset(['vento', 'terra']): 'areia',
    frozenset(['vento', 'raio']): 'tempestade',
    
    frozenset(['raio', 'terra']): 'magnetismo',

    # =========================================================================
    # 3 Elementos Base
    # =========================================================================
    frozenset(['fogo', 'vento', 'agua']): 'magma',
    frozenset(['fogo', 'vento', 'terra']): 'terremoto',
    frozenset(['fogo', 'vento', 'raio']): 'cristal',
    frozenset(['fogo', 'agua', 'terra']): 'obsidiana',
    frozenset(['fogo', 'agua', 'raio']): 'radiacao',
    frozenset(['fogo', 'terra', 'raio']): 'meteorito',
    frozenset(['vento', 'agua', 'terra']): 'permafrost',
    frozenset(['vento', 'agua', 'raio']): 'furacao',
    frozenset(['vento', 'terra', 'raio']): 'fulgurito',
    frozenset(['agua', 'terra', 'raio']): 'pantano',

    # =========================================================================
    # 4 Elementos Base
    # =========================================================================
    frozenset(['fogo', 'vento', 'agua', 'terra']): 'cataclisma',
    frozenset(['fogo', 'vento', 'agua', 'raio']): 'decaimento',
    frozenset(['fogo', 'vento', 'terra', 'raio']): 'supernova',
    frozenset(['fogo', 'agua', 'terra', 'raio']): 'miasma',
    frozenset(['vento', 'agua', 'terra', 'raio']): 'vortice',

    # =========================================================================
    # Singularidade
    # =========================================================================
    frozenset(['fogo', 'vento', 'agua', 'terra', 'raio']): 'caos'
}

cores_elementos = {
    # =========================================================================
    # Elementos Base
    # =========================================================================
    'fogo': (255, 80, 0),          # Laranja avermelhado
    'agua': (0, 140, 255),         # Azul vivo
    'vento': (200, 240, 255),      # Azul-esbranquiçado
    'terra': (120, 72, 32),        # Marrom
    'raio': (255, 255, 80),        # Amarelo elétrico

    # =========================================================================
    # 2 Elementos Base
    # =========================================================================
    'explosao': (255, 170, 0),     # Laranja brilhante
    'vapor': (220, 220, 220),      # Cinza claro
    'lava': (255, 50, 0),          # Vermelho-lava
    'plasma': (255, 0, 255),       # Magenta energético

    'gelo': (170, 240, 255),       # Azul gelo
    'lama': (102, 76, 51),         # Marrom escuro
    'tormenta': (50, 80, 180),     # Azul tempestuoso

    'areia': (230, 210, 120),      # Bege
    'tempestade': (120, 120, 200), # Azul arroxeado
    'magnetismo': (180, 0, 180),   # Roxo magnético

    # =========================================================================
    # 3 Elementos Base
    # =========================================================================
    'magma': (255, 100, 0),        # Laranja incandescente
    'terremoto': (90, 50, 40),     # Marrom escuro
    'cristal': (180, 255, 255),    # Ciano cristalino
    'obsidiana': (25, 20, 35),     # Preto arroxeado
    'radiacao': (0, 255, 80),      # Verde radioativo
    'meteorito': (100, 90, 110),   # Cinza espacial
    'permafrost': (190, 230, 255), # Azul congelado
    'furacao': (80, 180, 220),     # Azul-turquesa
    'fulgurito': (255, 220, 120),  # Dourado vítreo
    'pantano': (70, 110, 40),      # Verde musgo

    # =========================================================================
    # 4 Elementos Base
    # =========================================================================
    'cataclisma': (180, 30, 30),   # Vermelho destrutivo
    'decaimento': (110, 255, 110), # Verde pálido
    'supernova': (255, 255, 255),  # Branco estelar
    'miasma': (100, 60, 120),      # Roxo sombrio
    'vortice': (60, 100, 180),     # Azul profundo

    # =========================================================================
    # Singularidade
    # =========================================================================
    'caos': (20, 20, 20),          # Preto absoluto
}

fusoes_inversas = {v: k for k, v in tabela_fusoes.items()}

def interpola_cor(lista_rgb):
    """Recebe uma lista de tuplas (R, G, B) reais e faz a média quadrática delas"""    
    r, g, b = 0, 0, 0
    for cor in lista_rgb:
        r += cor[0] ** 2
        g += cor[1] ** 2
        b += cor[2] ** 2
        
    n = len(lista_rgb)
    return (
        int(math.sqrt(r / n)),
        int(math.sqrt(g / n)),
        int(math.sqrt(b / n))
    )

#Todos os elementos
elementos_validos = set()

# Pega os elementos base e os resultados da tabela de fusões
for componentes, resultado in tabela_fusoes.items():
    elementos_validos.update(componentes)
    elementos_validos.add(resultado)

def decay(elemento):
    """Retorna o conjunto de bases puras que compõem um elemento (puro ou já fundido)"""
    if elemento in BASES_PURAS:
        return {elemento}

    return set(fusoes_inversas[elemento])

def fusao(elementos):
    """
    Decai uma lista de elementos até suas bases puras
    e retorna o elemento resultante da fusão máxima dessas bases e sua cor
    """

    bases_unicas = set()
    for elemento in elementos:
        bases_unicas.update(decay(elemento))

    elemento_resultado = tabela_fusoes[frozenset(bases_unicas)]
    return elemento_resultado, cores_elementos[elemento_resultado]


def criar_tecnica_simples(nome, propriedades):
    """ Cria uma técnica simples """
    elementos_raw = []
    custo = 0
    dano = 0
    cor_usuario = None

    for tipo, valor in propriedades:
        if tipo == 'elementos':
            elementos_raw = valor
        elif tipo == 'custo':
            custo = valor
        elif tipo == 'dano':
            dano = valor
        elif tipo == 'cor':
            cor_usuario = valor

    if not elementos_raw:
        print(f'Erro semântico: a técnica "{nome}" precisa de ao menos um elemento.')
        return None

    for elemento in elementos_raw:
        if elemento not in elementos_validos:
            print(f'Erro semântico: O elemento "{elemento}" na técnica "{nome}" não existe nas regras do sistema.')
            return None

    # Remove duplicados preservando a ordem de definição
    elementos_unicos = list(dict.fromkeys(elementos_raw))

    if len(elementos_unicos) > 1:
        elemento_final, cor_tabela = fusao(elementos_unicos)
    else:
        elemento_final = elementos_unicos[0]
        cor_tabela = cores_elementos[elemento_final]

    cor_manual = cor_usuario is not None
    cor_final = cor_usuario if cor_manual else cor_tabela

    tabela_tecnicas[nome] = {
        'elementos': [elemento_final],
        'custo': custo,
        'dano': dano,
        'cor': cor_final,
        'cor_manual': cor_manual,
    }

    print(f'\nTecnica "{colorir(nome, cor_final)}" criada!')
    print(tabela_tecnicas[nome])
    return nome


def criar_tecnica_composta(nome, nomes_tecnicas):
    """ Cria uma técnica composta a partir da combinação de técnicas já existentes """
    elementos_base = []
    custo = 0
    dano = 0
    cores_sub_tecnicas = []
    cor_manual = False

    for nome_tecnica in nomes_tecnicas:

        if nome_tecnica not in tabela_tecnicas:
            print(f'Erro semântico: técnica "{nome_tecnica}" não existe')
            return None

        tecnica_base = tabela_tecnicas[nome_tecnica]
        custo += tecnica_base['custo']
        dano += tecnica_base['dano']
        cores_sub_tecnicas.append(tecnica_base['cor'])
        cor_manual = cor_manual or tecnica_base['cor_manual']
        elementos_base.extend(tecnica_base['elementos'])

    # Remove duplicados das bases antes de mandar para a fusão (caso combinem técnicas do mesmo elemento)
    elementos_base = list(dict.fromkeys(elementos_base))

    if len(elementos_base) > 1:
        elemento_final, cor_tabela = fusao(elementos_base)
    else:
        elemento_final = elementos_base[0]
        cor_tabela = cores_elementos[elemento_final]

    # Se nenhuma das técnicas combinadas tem cor definida manualmente (direta ou
    # herdada de uma combinação anterior), usa-se a cor de tabela do resultado.
    # Caso ao menos uma tenha, interpola-se as cores das técnicas combinadas.
    cor_final = interpola_cor(cores_sub_tecnicas) if cor_manual else cor_tabela

    tabela_tecnicas[nome] = {
        'elementos': [elemento_final],
        'custo': custo,
        'dano': dano,
        'cor': cor_final,
        'cor_manual': cor_manual,
    }

    partes_coloridas = [colorir(nomes_tecnicas[i], cores_sub_tecnicas[i]) for i in range(len(nomes_tecnicas))]
    print('\n--- Fusão Elemental Realizada ---')
    print(' + '.join(partes_coloridas))
    print(f'→ {colorir(elemento_final, cor_final)}')
    print('=========================================')

    print(f'\nTecnica composta "{colorir(nome, cor_final)}" criada!')
    print(tabela_tecnicas[nome])
    return nome


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

    energia = 0
    elementos_raw = []

    for tipo, valor in atributos:

        # Energia
        if tipo == 'energia':
            energia = valor

        # Elementos
        elif tipo == 'elemento':
            if valor not in elementos_validos:
                print(f'Erro semântico: O elemento "{valor}" atribuído à entidade "{nome}" não existe nas regras do sistema.')
                return

            elementos_raw.append(valor)

    # Os elementos da entidade ficam exatamente como foram definidos, só removendo duplicados.
    # Não há fusão nem decaimento, precisando ter o exato elemento de uma técnica para usa-la
    tabela_entidades[nome] = {
        'energia': energia,
        'elementos': list(dict.fromkeys(elementos_raw)),
    }

    print(f'\nEntidade "{nome}" criado!')
    print(tabela_entidades[nome])


# Técnica
def p_tecnica(p):
    '''
    tecnica : TECNICA ID LBRACE corpo_tecnica RBRACE
    '''

    nome = p[2]
    tipo_corpo, dados = p[4]

    if tipo_corpo == 'combinacao':
        resultado = criar_tecnica_composta(nome, dados)
    else:
        resultado = criar_tecnica_simples(nome, dados)

    if resultado is not None:
        p[0] = resultado

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
        print('Erro semântico: energia insuficiente')
        return

    # A entidade precisa ter o elemento da técnica sem fundir ou decair seus elementos
    elemento_tecnica = tecnica['elementos'][0]
    if elemento_tecnica not in entidade['elementos']:
        print(
            f'Erro semântico: A entidade "{nome_entidade}" não possui o elemento "{elemento_tecnica}" '
            f'necessário para manifestar a técnica "{nome_tecnica}".'
        )
        return

    # Executa tecnica
    entidade['energia'] -= tecnica['custo']

    print(f'\n{nome_entidade} usou {colorir(nome_tecnica, tecnica["cor"])}!')
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

# Propriedade única
def p_propriedades_unica(p):
    '''
    propriedades : propriedade
    '''

    p[0] = [p[1]]

def p_corpo_tecnica_propriedades(p):
    '''
    corpo_tecnica : propriedades
    '''

    p[0] = ('propriedades', p[1])


# Corpo da Técnica - (técnicas simples e combinações recursivas)
def p_corpo_tecnica_combinacao(p):
    '''
    corpo_tecnica : COMBINAR combinacao
    '''

    p[0] = ('combinacao', p[2])


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

def p_propriedade_cor(p):
    '''
    propriedade : COR HEXCODE
    '''
    p[0] = ('cor', hex_to_rgb(p[2]))


# Erro síntatico
def p_error(p):

    if p:
        print(f'Erro sintático próximo de "{p.value}"')
    else:
        print('Erro sintático no fim do arquivo')

# Constrói o Parser
parser = yacc.yacc()

if __name__ == "__main__":
    # Entrada de padrão
    entrada_default = '''

    entidade FrostMage {
        energia 500
        elemento fogo
        elemento vento
        elemento agua
        elemento terra
    }

    entidade ExplosionMage {
        energia 300
        elemento explosao
    }

    tecnica fogo_base {
        elementos fogo
        custo 10
        dano 20
    }

    tecnica vento_base {
        elementos vento
        custo 15
        dano 25
        cor #00FF00
    }

    tecnica terra_base {
        elementos terra
        custo 12
        dano 18
    }

    tecnica agua_base {
        elementos agua
        custo 5
        dano 10
    }

    tecnica tempestade_direta {
        elementos vento raio
        custo 20
        dano 30
    }

    tecnica explosao {
        combinar fogo_base + vento_base
    }

    tecnica lava {
        combinar fogo_base + terra_base
    }

    tecnica magma {
        combinar explosao + agua_base
    }

    usar FrostMage fogo_base
    usar FrostMage explosao
    usar ExplosionMage explosao
    usar ExplosionMage fogo_base
    '''

    # Execução
    parser.parse(entrada_default)

    # Mostra tabela final
    print('\nTabela de entidades:')
    print(tabela_entidades)

    print('\nTabela de Tecnicas:')
    print(tabela_tecnicas)