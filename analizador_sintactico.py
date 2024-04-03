from flask import Flask, render_template, request, jsonify
from analizador_lexico import lexer, ingreso, tokens
from ply.yacc import yacc

app = Flask(__name__)

def p_program(p):
    '''
    program : statement
            | program statement
    '''

def p_statement(p):
    '''
    statement : while_loop_statement
    '''

def p_while_loop_statement(p):
    '''
    while_loop_statement : WHILE IZQPARENT expression MAYORQUE INT DERPARENT LLAVEIZQ print_statement LLAVEDER
    '''

def p_print_statement(p):
    '''
    print_statement : PRINT IZQPARENT STRING DERPARENT PUNTOCOMA
    '''

def p_expression(p):
    '''
    expression : ID
               | INT
    '''

def p_error(p):
    raise SyntaxError("Error sintáctico en la posición {}".format(p.lexpos))

parser = yacc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar_lexico', methods=['POST'])
def analizar_cadena_lexico():
    cadena = request.json['cadena']
    try:
        tokens_lexicos = ingreso(cadena)
        return jsonify(resultado_lexico=tokens_lexicos)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/analizar_sintactico', methods=['POST'])
def analizar_cadena_sintactico():
    cadena = request.json['cadena']
    try:
        resultado_sintactico = parser.parse(cadena, lexer=lexer)
        if resultado_sintactico is None:
            mensaje = "La cadena fue aceptada correctamente."
        else:
            mensaje = "Cadena no aceptada"
        return jsonify(resultado_sintactico=mensaje)
    except SyntaxError as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)