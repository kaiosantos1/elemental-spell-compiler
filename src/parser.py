# É o analisador síntático. Vê se a sequência segue a gramática da linguagem


import ply.yacc as yacc

# Importa os tokens do lexer
from lexer import tokens

#A gramática começa em "programa"
start = 'programa'

# Tabelas de símbolos -> Servem para armazenar informações semânticas

tabela_entidades = {}
tabela_tecnicas = {}

tabela_fusoes = {

    # 1. Combinações Base + Base (2 Elementos)
    frozenset(['fogo', 'vento']): 'explosao',
    frozenset(['fogo', 'agua']): 'vapor',
    frozenset(['fogo', 'terra']): 'lava',
    frozenset(['fogo', 'raio']): 'plasma',

    frozenset(['agua', 'vento']): 'gelo',
    frozenset(['agua', 'terra']): 'lama',
    frozenset(['agua', 'raio']): 'tormenta',

    frozenset(['vento', 'terra']): 'areia',
    frozenset(['vento', 'raio']): 'tempestade',
    
    frozenset(['raio', 'terra']): 'cristal',


    # 2. Combinações derivadas + Base

    # Explosão (Fogo + Vento)
    frozenset(['explosao', 'fogo']): 'explosao',       
    frozenset(['explosao', 'vento']): 'explosao', 
    frozenset(['explosao', 'explosao']): 'explosao',
    frozenset(['explosao', 'agua']): 'magma',     
    frozenset(['explosao', 'terra']): 'terremoto',     
    frozenset(['explosao', 'raio']): 'supernova',      

    # Vapor (Fogo + Agua)
    frozenset(['vapor', 'fogo']): 'vapor',
    frozenset(['vapor', 'agua']): 'vapor',
    frozenset(['vapor', 'vapor']): 'vapor',
    frozenset(['vapor', 'vento']): 'nevoa',           
    frozenset(['vapor', 'terra']): 'geiser', 
    frozenset(['vapor', 'raio']): 'nevoa_acida',

    # Lava (Fogo + Terra)
    frozenset(['lava', 'fogo']): 'lava',
    frozenset(['lava', 'terra']): 'lava',
    frozenset(['lava', 'lava']): 'lava',
    frozenset(['lava', 'agua']): 'obsidiana', 
    frozenset(['lava', 'vento']): 'cinzas', 
    frozenset(['lava', 'raio']): 'meteorito',  

    # Plasma (Fogo + Raio)
    frozenset(['plasma', 'fogo']): 'plasma',
    frozenset(['plasma', 'raio']): 'plasma',
    frozenset(['plasma', 'plasma']): 'plasma',
    frozenset(['plasma', 'agua']): 'radiacao',      
    frozenset(['plasma', 'vento']): 'laser',    
    frozenset(['plasma', 'terra']): 'metal_liquido', 

    # Gelo (Agua + Vento)
    frozenset(['gelo', 'agua']): 'gelo',
    frozenset(['gelo', 'vento']): 'gelo',
    frozenset(['gelo', 'gelo']): 'gelo',
    frozenset(['gelo', 'fogo']): 'gelo_seco',         
    frozenset(['gelo', 'terra']): 'permafrost',    
    frozenset(['gelo', 'raio']): 'ventania_polar',  

    # Lama (Agua + Terra)
    frozenset(['lama', 'agua']): 'lama',
    frozenset(['lama', 'terra']): 'lama',
    frozenset(['lama', 'lama']): 'lama',
    frozenset(['lama', 'fogo']): 'argila',             
    frozenset(['lama', 'vento']): 'poeira',           
    frozenset(['lama', 'raio']): 'areia_movedica',    

    # Tormenta (Agua + Raio)
    frozenset(['tormenta', 'agua']): 'tormenta',
    frozenset(['tormenta', 'raio']): 'tormenta',
    frozenset(['tormenta', 'tormenta']): 'tormenta',
    frozenset(['tormenta', 'fogo']): 'chuva_acida',   
    frozenset(['tormenta', 'vento']): 'furaçao',  
    frozenset(['tormenta', 'terra']): 'pântano',    

    # Areia (Vento + Terra)
    frozenset(['areia', 'vento']): 'areia',
    frozenset(['areia', 'terra']): 'areia',
    frozenset(['areia', 'areia']): 'areia',
    frozenset(['areia', 'fogo']): 'vidro',     
    frozenset(['areia', 'agua']): 'lodo',     
    frozenset(['areia', 'raio']): 'fulgurito',     

    # Tempestade (Vento + Raio)
    frozenset(['tempestade', 'vento']): 'tempestade',
    frozenset(['tempestade', 'raio']): 'tempestade',
    frozenset(['tempestade', 'tempestade']): 'tempestade',
    frozenset(['tempestade', 'fogo']): 'incendio',    
    frozenset(['tempestade', 'agua']): 'diluvio',
    frozenset(['tempestade', 'terra']): 'desabamento',  

    # Cristal (Raio + Terra)
    frozenset(['cristal', 'raio']): 'cristal',
    frozenset(['cristal', 'terra']): 'cristal',
    frozenset(['cristal', 'cristal']): 'cristal',
    frozenset(['cristal', 'fogo']): 'rubi',          
    frozenset(['cristal', 'agua']): 'prisma',      
    frozenset(['cristal', 'vento']): 'som_sonico' 


    
}

cores_elementos = {

    # 1. Elementos Base

    'fogo': (255, 69, 0),          # Vermelho Alaranjado
    'agua': (30, 144, 255),        # Azul Esquilo
    'vento': (240, 230, 140),      # Amarelo Cáqui Claro
    'raio': (138, 43, 226),        # Roxo Violeta
    'terra': (139, 69, 19),        # Marrom Sela

    # 2. Elementos derivados de 2 vias (Base + Base)

    'explosao': (255, 140, 0),     # Laranja Escuro (Fogo + Vento)
    'vapor': (220, 220, 220),      # Branco Cinzento (Fogo + Água)
    'lava': (226, 88, 34),         # Laranja Vulcânico (Fogo + Terra)
    'plasma': (255, 0, 128),       # Rosa Choque (Fogo + Raio)
    'gelo': (0, 255, 255),         # Ciano (Água + Vento)
    'lama': (101, 67, 33),         # Marrom Escuro (Água + Terra)
    'tormenta': (72, 61, 139),     # Azul Escuro Purpúreo  (Água + Raio)
    'areia': (238, 214, 175),      # Bege Areia (Vento + Terra)
    'tempestade': (112, 128, 144), # Cinza Ardósia (Vento + Raio)
    'cristal': (186, 85, 211),     # Orquídea Média (Raio + Terra)

    # 3. Elementos derivados de 3 vias (Derivado + Base)
    
    # Derivados de Explosão
    'magma': (178, 34, 34),        # Vermelho Tijolo
    'terremoto': (74, 53, 41),     # Marrom Profundo
    'supernova': (255, 255, 204),  # Amarelo Estelar Pálido 

    # Derivados de Vapor
    'nevoa': (245, 245, 245),      # Branco Fumaça 
    'geiser': (175, 238, 238),     # Turquesa Pálido
    'nevoa_acida': (152, 251, 152),# Verde Pálido Elétrico

    # Derivados de Lava
    'obsidiana': (21, 21, 21),     # Preto Vidro Vulcânico
    'cinzas': (169, 169, 169),     # Cinza Escuro 
    'meteorito': (105, 105, 105),  # Cinza Carbono

    # Derivados de Plasma
    'radiacao': (50, 205, 50),     # Verde Lima Fluorescente
    'laser': (255, 0, 0),          # Vermelho Puro Concentrado
    'metal_liquido': (212, 175, 55),# Ouro Metálico 

    # Derivados de Gelo
    'gelo_seco': (240, 248, 255),  # Branco Gelo 
    'permafrost': (95, 158, 160),  # Azul Cadete 
    'ventania_polar': (176, 224, 230),# Azul Pó 

    # Derivados de Lama
    'argila': (210, 105, 30),      # Chocolate 
    'poeira': (222, 184, 135),     # Madeiro Claro 
    'areia_movedica': (188, 143, 143),# Rosado Argiloso 

    # Derivados de Tormenta
    'chuva_acida': (127, 255, 0),  # Verde Amarelado Ácido 
    'furaçao': (47, 79, 79),       # Verde Ardósia Escuro
    'pântano': (46, 139, 87),      # Verde Mar

    # Derivados de Areia
    'vidro': (143, 188, 143),      # Verde Mar Escuro
    'lodo': (85, 107, 47),         # Verde Oliva Escuro
    'fulgurito': (205, 133, 63),   # Bronze Natural

    # Derivados de Tempestade
    'incendio': (255, 0, 0),       # Vermelho Vivo
    'diluvio': (0, 0, 128),        # Azul Marinho Profundo 
    'desabamento': (112, 105, 89), # Cinza Castanho 

    # Derivados de Cristal
    'rubi': (156, 0, 48),          # Vermelho Rubi Profundo
    'prisma': (255, 192, 203),     # Rosa Claro Refratado
    'som_sonico': (230, 230, 250)  # Lavanda Pálido 
}

elementos_derivados = {
   
    # 1. Derivados de 2 vias (Base + Base)

    'explosao': ['fogo', 'vento'],
    'vapor': ['fogo', 'agua'],
    'lava': ['fogo', 'terra'],
    'plasma': ['fogo', 'raio'],
    
    'gelo': ['agua', 'vento'],
    'lama': ['agua', 'terra'],
    'tormenta': ['agua', 'raio'],
    
    'areia': ['vento', 'terra'],
    'tempestade': ['vento', 'raio'],
    
    'cristal': ['raio', 'terra'],

    # 2. Derivados de 3 vias (Derivado + Base)
    
    # Derivados de Explosão
    'magma': ['explosao', 'agua'],
    'terremoto': ['explosao', 'terra'],
    'supernova': ['explosao', 'raio'],

    # Derivados de Vapor
    'nevoa': ['vapor', 'vento'],
    'geiser': ['vapor', 'terra'],
    'nevoa_acida': ['vapor', 'raio'],

    # Derivados de Lava
    'obsidiana': ['lava', 'agua'],
    'cinzas': ['lava', 'vento'],
    'meteorito': ['lava', 'raio'],

    # Derivados de Plasma
    'radiacao': ['plasma', 'agua'],
    'laser': ['plasma', 'vento'],
    'metal_liquido': ['plasma', 'terra'],

    # Derivados de Gelo
    'gelo_seco': ['gelo', 'fogo'],
    'permafrost': ['gelo', 'terra'],
    'ventania_polar': ['gelo', 'raio'],

    # Derivados de Lama
    'argila': ['lama', 'fogo'],
    'poeira': ['lama', 'vento'],
    'areia_movedica': ['lama', 'raio'],

    # Derivados de Tormenta
    'chuva_acida': ['tormenta', 'fogo'],
    'furaçao': ['tormenta', 'vento'],
    'pântano': ['tormenta', 'terra'],

    # Derivados de Areia
    'vidro': ['areia', 'fogo'],
    'lodo': ['areia', 'agua'],
    'fulgurito': ['areia', 'raio'],

    # Derivados de Tempestade
    'incendio': ['tempestade', 'fogo'],
    'diluvio': ['tempestade', 'agua'],
    'desabamento': ['tempestade', 'terra'],

    # Derivados de Cristal
    'rubi': ['cristal', 'fogo'],
    'prisma': ['cristal', 'agua'],
    'som_sonico': ['cristal', 'vento']
}

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

        elementos_base = []
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
                if e not in elementos_base:
                    elementos_base.append(e)

        if len(elementos_base) > 2:

            print(
                f'Erro semântico: fusões suportam no máximo 2 elementos. '
                f'Elementos recebidos: {elementos_base}'
            )

            return

        fusao = tabela_fusoes.get(
            frozenset(elementos_base)
        )

        if fusao:

            cor1 = cores_elementos[elementos_base[0]]
            cor2 = cores_elementos[elementos_base[1]]
            cor_resultado = cores_elementos[fusao]

            print('\nElementos encontrados:')
            print(elementos_base)

            print('\nFusão elemental')

            print(
                f'{elementos_base[0]} + {elementos_base[1]}'
            )

            print(
                f'→ {fusao}'
            )

            print('\nRGB')

            print(
                f'{cor1} + {cor2}'
            )

            print(
                f'→ {cor_resultado}'
            )

            elementos = [fusao]

        else:
            elementos = elementos_base

        tabela_tecnicas[nome] = {
            'elementos': elementos,
            'requisitos': elementos_base,
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

    elementos_necessarios = tecnica.get(
        'requisitos',
        tecnica['elementos']
    )

    for elemento in elementos_necessarios:

        # elemento derivado?
        if elemento in elementos_derivados:

            requisitos = elementos_derivados[elemento]

            for req in requisitos:

                if req not in entidade['elementos']:
                    print(
                        f'Erro semântico: {nome_entidade} não possui o elemento "{req}" '
                        f'para formar "{elemento}"'
                    )
                    return

        else:

            if elemento not in entidade['elementos']:
                print(
                    f'Erro semântico: {nome_entidade} não possui o elemento "{elemento}"'
                )
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

if "__name__" == "__main__":
    # Entrada de padrão
    entrada_default = '''

    entidade FrostMage {
        energia 500
        elemento fogo
        elemento vento
        elemento agua
        elemento terra
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
    }

    tecnica agua_base {
        elementos agua
        custo 5
        dano 10
    }

    tecnica terra_base {
        elementos terra
        custo 12
        dano 18
    }

    tecnica explosao {
        combinar fogo_base + vento_base
    }

    tecnica magma {
        combinar explosao + agua_base
    }

    tecnica explosao_aprimorada {
        combinar explosao + fogo_base
    }

    tecnica terremoto {
        combinar explosao + terra_base
    }

    tecnica lava {
        combinar fogo_base + terra_base
    }


    usar FrostMage explosao
    usar FrostMage magma
    usar FrostMage explosao_aprimorada
    usar FrostMage terremoto
    usar FrostMage lava
    '''

    #Teste de entradas

    """

    """


    # Execução
    parser.parse(entrada_default)

    # Mostra tabela final
    print('\nTabela de entidades:')
    print(tabela_entidades)

    print('\nTabela de Tecnicas:')
    print(tabela_tecnicas)