import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import lexer

# Resultado del análisis
resultado_gramatica = []

precedence = (
    ('right', 'ASIGNAR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMINUS'),
)

nombres = {}

parens_abiertos = 0
parens_cerrados = 0
llaves_abiertas = 0
llaves_cerradas = 0

def p_declaracion_asignar(t):
    'declaracion : IDENTIFICADOR ASIGNAR expresion PUNTOCOMA'
    nombres[t[1]] = t[3]

def p_declaracion_expr(t):
    'declaracion : expresion'
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion
                |   expresion RESTA expresion
                |   expresion MULT expresion
                |   expresion DIV expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '**':
        t[0] = t[1] ** t[3]

def p_expresion_uminus(t):
    '''expresion : RESTA expresion %prec UMINUS'''
    t[0] = -t[2]


def p_expresion_grupo(t):
    '''expresion  : PARIZQ expresion PARDER
                | LLAIZQ expresion LLADER
                | CORIZQ expresion CORDER'''
    global parens_abiertos, parens_cerrados, llaves_abiertas, llaves_cerradas
    t[0] = t[2]
    if t[1] == '(':
        parens_abiertos += 1
    elif t[1] == ')':
        parens_cerrados += 1
    elif t[1] == '{':
        llaves_abiertas += 1
    elif t[1] == '}':
        llaves_cerradas += 1

def p_expresion_logicas(t):
    '''
    expresion   :  expresion MENORQUE expresion 
                |  expresion MAYORQUE expresion 
                |  expresion MENORIGUAL expresion 
                |   expresion MAYORIGUAL expresion 
                |   expresion IGUAL expresion 
                |   expresion DISTINTO expresion
                |  PARIZQ expresion PARDER MENORQUE PARIZQ expresion PARDER
                |  PARIZQ expresion PARDER MAYORQUE PARIZQ expresion PARDER
                |  PARIZQ expresion PARDER MENORIGUAL PARIZQ expresion PARDER 
                |  PARIZQ  expresion PARDER MAYORIGUAL PARIZQ expresion PARDER
                |  PARIZQ  expresion PARDER IGUAL PARIZQ expresion PARDER
                |  PARIZQ  expresion PARDER DISTINTO PARIZQ expresion PARDER
    '''
    if t[2] == "<": t[0] = t[1] < t[3]
    elif t[2] == ">": t[0] = t[1] > t[3]
    elif t[2] == "<=": t[0] = t[1] <= t[3]
    elif t[2] == ">=": t[0] = t[1] >= t[3]
    elif t[2] == "==": t[0] = t[1] == t[3]
    elif t[2] == "!=": t[0] = t[1] != t[3]

def p_expresion_booleana(t):
    '''
    expresion   :   expresion AND expresion 
                |   expresion OR expresion 
                |   expresion NOT expresion 
                |  PARIZQ expresion AND expresion PARDER
                |  PARIZQ expresion OR expresion PARDER
                |  PARIZQ expresion NOT expresion PARDER
    '''
    if t[2] == "&&":
        t[0] = t[1] and t[3]
    elif t[2] == "||":
        t[0] = t[1] or t[3]
    elif t[2] == "!":
        t[0] = not t[3]

def p_expresion_numero(t):
    'expresion : ENTERO'
    t[0] = t[1]

def p_expresion_cadena(t):
    'expresion : COMDOB expresion COMDOB'
    t[0] = t[2]

def p_expresion_nombre(t):
    'expresion : IDENTIFICADOR'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("Nombre desconocido ", t[1])
        t[0] = 0

def p_for_loop(t):
    '''
    declaracion : FOR PARIZQ IDENTIFICADOR ASIGNAR expresion PUNTOCOMA expresion MENORIGUAL expresion PUNTOCOMA expresion PLUSPLUS PARDER LLAIZQ imprimir LLADER
                | FOR PARIZQ IDENTIFICADOR ASIGNAR expresion PUNTOCOMA expresion MENORIGUAL expresion PUNTOCOMA expresion PLUSPLUS PARDER LLAIZQ SYSTEM PUNTO OUT PUNTO PRINTLN PARIZQ CADENA PARDER PUNTOCOMA LLADER
    '''
    print("Bucle for encontrado")
    if len(t) == 14:  # Sin imprimir dentro del bucle
        t[0] = ("Bucle for encontrado",)
    else:  # Con imprimir dentro del bucle
        t[0] = ("Bucle for encontrado con impresión",)


def p_imprimir(t):
    '''
    imprimir : SYSTEM PUNTO OUT PUNTO PRINTLN PARIZQ CADENA PARDER PUNTOCOMA
            | SYSTEM PUNTO OUT PUNTO PRINTLN PARIZQ CADENA SUMA ENTERO PARDER PUNTOCOMA
    '''
    pass  # Aquí podrías realizar acciones específicas si necesitas algún tipo de procesamiento especial

    
def p_error(t):
    global resultado_gramatica, parens_abiertos, parens_cerrados, llaves_abiertas, llaves_cerradas
    if t is not None:
        resultado = "Error sintactico de tipo {} en el valor {}".format(str(t.type), str(t.value))
        print(resultado)
        resultado_gramatica.append(resultado)
    else:
        errores = []
        if parens_abiertos > parens_cerrados:
            errores.append("Error: Falta cerrar parentesis")
        elif parens_abiertos < parens_cerrados:
            errores.append("Error: Falta abrir parentesis")
        if llaves_abiertas > llaves_cerradas:
            errores.append("Error: Falta cerrar llave")
        elif llaves_abiertas < llaves_cerradas:
            errores.append("Error: Falta abrir llave")
        
        if errores:
            for error in errores:
                print(error)
                resultado_gramatica.append(error)
        else:
            print("Error: Falta cerrar llave y/o parentesis")
            resultado_gramatica.append("Error: Falta cerrar llave y/o parentesis")

    

# Instanciamos el analizador léxico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica, parens_abiertos, parens_cerrados, llaves_abiertas, llaves_cerradas
    resultado_gramatica.clear()
    parens_abiertos = 0
    parens_cerrados = 0
    llaves_abiertas = 0
    llaves_cerradas = 0

    # Concatenar todas las líneas en una sola cadena
    codigo_completo = ""
    for linea in data.splitlines():
        if linea.strip():  # Ignorar líneas en blanco
            codigo_completo += linea.strip() + " "

    # Realizar el análisis sintáctico en el código completo
    parser.parse(codigo_completo)

    errores = []
    if parens_abiertos > parens_cerrados:
        errores.append("Error: Falta cerrar parentesis")
    elif parens_abiertos < parens_cerrados:
        errores.append("Error: Falta abrir parentesis")
    if llaves_abiertas > llaves_cerradas:
        errores.append("Error: Falta cerrar llave")
    elif llaves_abiertas < llaves_cerradas:
        errores.append("Error: Falta abrir llave")
    
    if errores:
        print("Errores sintácticos: ")
        for error in errores:
            print(error)
            resultado_gramatica.append(error)
    else:
        print("El análisis sintáctico se completó sin errores")

    return resultado_gramatica


if __name__ == '__main__':
    # Aquí defines tu entrada como una variable
    i = 0 
    while True:
        try:
            s = input('Ingresa el dato >>> ')
        except EOFError:
            continue
        if not s:  
            continue
        
        gram = parser.parse(s)
        print("Resultado ", gram)
        prueba_sintactica(s)
