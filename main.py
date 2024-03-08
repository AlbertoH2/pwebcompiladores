from flask import Flask, request, jsonify, render_template
import analizador_lexico as lex
import analizador_sintactico as yacc  # Importa tu analizador sintáctico

app = Flask('app')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/api/v1/lexer', methods = ['POST'])
def lexer():
    data = request.get_json()
    code = data.get('code')
    
    lex.lexer.input(code)
    
    tokens = []
    while True:
        tok = lex.lexer.token()
        if not tok:
            break
        tokens.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'lexpos': tok.lexpos
        })
        
    print("Code:", code)
    print("Tokens", tokens)
    
    # Parsea el código con el analizador sintáctico
    resultado_gramatica = yacc.prueba_sintactica(code)
    
    errors = []
    for result in resultado_gramatica:
        if result.startswith("Error"):
            errors.append(result)
            
    # Si hay errores sintácticos, no se devuelven los tokens
    if errors:
        return render_template('result.html', code=code, errors=errors)
    else:
        return render_template('result.html', code=code, tokens=tokens)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
