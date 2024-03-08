import ply.lex as lex

# al comienzo de tu módulo analizador_lexico.py
resultado_lexema = []

# Palabras reservadas
reservada = (
    'FOR', 
    'DO', 
    'WHILE', 
    'IF', 
    'ELSE',
    'STATIC',
    'VOID',
    'PUBLIC',
    'LENGHT',
    'PRINTLN', 
    'MAIN',
    'SYSTEM',
    'OUT',
)

# Tokens
tokens = (
    'IDENTIFICADOR',
    'ENTERO',
    'CADENA',
    'ASIGNAR',
    
    'SUMA',
    'RESTA',
    'MULT',
    'DIV',
    'POTENCIA',
    'MODULO',
    
    'MINUSMINUS',
    'PLUSPLUS',
    
    #Logica
    'AND',
    'OR',
    'NOT',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORQUE',
    'MAYORIGUAL',
    'IGUAL',
    'DISTINTO',
    # Symbolos
    'NUMERAL',

    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAIZQ',
    'LLADER',
    
    # Otros
    'PUNTO',
    'PUNTOCOMA',
    'COMA',
    'COMDOB',
    'MAYORDER', #>>
    'MAYORIZQ', #<<
) + reservada


# Expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MINUSMINUS = r'\-\-'

t_PUNTO = r'\.'
t_MULT = r'\*'
t_DIV = r'/'
t_MODULO = r'\%'
t_POTENCIA = r'(\*{2} | \^)'

t_ASIGNAR = r'='
# Expresiones Logicas
t_AND = r'\&\&'
t_OR = r'\|{2}'
t_NOT = r'\!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_PUNTOCOMA = ';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_COMDOB = r'\"'

def t_FOR(t):
    r'for\b'
    return t

def t_SYSTEM(t):
    r'system\b'
    return t

def t_DO(t):
    r'do\b'
    return t

def t_WHILE(t):
    r'while\b'
    return t

def t_IF(t):
    r'if\b'
    return t

def t_ELSE(t):
    r'else\b'
    return t

def t_STATIC(t):
    r'static\b'
    return t

def t_VOID(t):
    r'void\b'
    return t

def t_PUBLIC(t):
    r'public\b'
    return t

def t_LENGHT(t):
    r'lenght\b'
    return t

def t_PRINTLN(t):
    r'println\b'
    return t

def t_MAIN(t):
    r'main\b'
    return t

def t_OUT(t):
    r'out\b'
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = t.value.upper() if t.value.upper() in reservada else 'IDENTIFICADOR'
    return t

# Regla para cadenas de texto
def t_CADENA(t):
    r'\"(.*?)\"'
    t.value = t.value[1:-1]  # Elimina las comillas alrededor de la cadena
    return t


def t_NUMERAL(t):
    r'\#'
    return t

def t_PLUSPLUS(t):
    r'\+\+'
    return t

def t_MENORIGUAL(t):
    r'<='
    return t

def t_MAYORIGUAL(t):
    r'>='
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_DISTINTO(t):
    r'!='
    return t

def t_MAYORDER(t):
    r'<<'
    return t

def t_MAYORIZQ(t):
    r'>>'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de multiple linea")
    
def t_comments_ONELine(t):
    r'\/\/(.)*\n'
    t.lexer.lineno += 1
    print("Comentario de una linea")
t_ignore =' \t'


def t_error( t):
    global resultado_lexema
    estado = "** Token no valido en la Linea {:4} Valor {:16} Posicion {:4}".format(str(t.lineno), str(t.value), str(t.lexpos))
    resultado_lexema.append(estado)
    t.lexer.skip(1)
    
    
# Prueba de ingreso
def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        # print("lexema de "+tok.type+" valor "+tok.value+" linea "tok.lineno)
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno),str(tok.type) ,str(tok.value), str(tok.lexpos) )
        resultado_lexema.append(estado)
    return resultado_lexema

# Construir el analizador léxico
lexer = lex.lex()

if __name__ == '__main__':
    while True:
        data = input("ingrese: ")
        prueba(data)
        print(resultado_lexema)