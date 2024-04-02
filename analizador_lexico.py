import ply.lex as lex
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

tokens = ['PRINT', 'IZQPARENT', 'DERPARENT', 'IZQCORCHET', 'DERCORCHET', 'MAYORQUE', 
          'INT', 'PUNTOCOMA', 'COMILLAS', 'DOSPUNTOS', 'ENTERO', 'ID', 'WHILE', 'STRING']  

palabras_reservadas = {
    'print': 'PRINT',
    'while': 'WHILE'
}

def clasificar_token(token):
    if token is None:
        return 'Token inválido: None'
    elif token.type == 'ID':
        return 'Identificador' if token.value not in palabras_reservadas else 'Palabra reservada'
    elif token.type in ['INT', 'ENTERO', 'STRING']:
        return 'Tipo de dato'
    elif token.type in ['COMILLAS', 'DOSPUNTOS', 'IZQPARENT', 'DERPARENT', 'PUNTOCOMA', 'IZQCORCHET', 'DERCORCHET', 'MAYORQUE']:
        return 'Símbolo'
    elif token.type == 'PRINT':
        return 'Reservada PRINT'
    elif token.type == 'WHILE':
        return 'Reservada WHILE'
    else:
        return 'Token no existente'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'ENTERO'  
    return t

def t_STRING(t):
    r'\"([^\\\"]|\\.)*\"' 
    return t

t_PUNTOCOMA = r'\;'
t_IZQPARENT = r'\('
t_DERPARENT = r'\)'
t_IZQCORCHET = r'\{'
t_DERCORCHET = r'\}'
t_COMILLAS = r'\"'
t_MAYORQUE = r'\>'
t_DOSPUNTOS = r'\:'
t_ignore = ' \t\n'

def t_error(t):
    t.lexer.skip(1)  
    return t

lexer = lex.lex()

def ingreso(datos):
    if not datos:
        return ['Cadena inválida: La cadena está vacía.']

    lexer.input(datos)
    lexer.lineno = 1
    lexer_list = []

    for token in lexer:
        lexer_list.append(token)

    return lexer_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar_cadena():
    cadena = request.json['cadena']
    try:
        resultado_lexico = ingreso(cadena)
        return jsonify(resultado_lexico=[(f'" {token.value} " Token de tipo: {clasificar_token(token)}') for token in resultado_lexico])
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)