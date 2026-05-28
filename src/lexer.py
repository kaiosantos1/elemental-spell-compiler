# É o analisador léxico. Ele lê o texto e separa em Tokens. 
# O lexer funciona como um “quebrador de palavras”, ele pega caracteres e identifica: palavras reservadas; números; símbolos; identificadores


import ply.lex as lex


# Palavras reservadas -> São palavras que têm significado especial na linguagem ; é um dicionário Python. Do lado esquedo tem a palavra escrita e do direito o Token gerado

reserved = {
    'entidade':'ENTIDADE',
    'tecnica': 'TECNICA',
    'energia':'ENERGIA',
    'elemento': 'ELEMENTO',
    'elementos': 'ELEMENTOS',
    'custo': 'CUSTO',
    'dano': 'DANO',
    'usar': 'USAR',
    'combinar':'COMBINAR'
}


# Tokens -> É lista de todos os tokens possíveis da linguagem. A linguagem reconhece: identificadores; números; {; }; palavras reservadas

tokens = [
    'ID',
    'NUMERO',
    'LBRACE',
    'RBRACE',
    'PLUS'
] + list(reserved.values())


# Expressões regulares -> Padrão para reconhecer texto


t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS = r'\+'

# Ignorar espaços e TAB
t_ignore = ' \t'


# Token de número
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Token de ID
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Verifica se é palavra reservada
    t.type = reserved.get(t.value, 'ID')

    return t


# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Erro Léxico
def t_error(t):
    print(f'Caractere ilegal: {t.value[0]}')
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

# Entrada de teste
entrada = '''

entidade FrostMage {
    energia 500
    elemento agua
    elemento fogo
}

tecnica fogo_base {
    elementos fogo
    custo 20
    dano 50
}

usar FrostMage fogo_base
'''

# Teste do lexer
lexer.input(entrada)

for token in lexer:
    print(token)