from flask import Flask, jsonify
from analizador_lexico import lexer, tokens
from ply.yacc import yacc

app = Flask(__name__)

tokens = lexer.tokens

# Regla inicial del programa
def p_program(p):
    '''
    program : statement
            | program statement
    '''

# Regla para las sentencias
def p_statement(p):
    '''
    statement : while_loop_statement
              | print_statement
    '''

# Regla para el bucle while
def p_while_loop_statement(p):
    '''
    while_loop_statement : WHILE IZQPARENT expression MAYORQUE INT DERPARENT LLAVEIZQ print_statement LLAVEDER
    '''

# Regla para la sentencia print
def p_print_statement(p):
    '''
    print_statement : PRINT IZQPARENT STRING DERPARENT PUNTOCOMA
    '''

# Regla para la expresión
def p_expression(p):
    '''
    expression : ID
               | INT
               | STRING
    '''

# Manejo de errores sintácticos
def p_error(p):
    if p:
        raise SyntaxError(f"Error sintáctico en la posición {p.lexpos}")
    else:
        raise SyntaxError("Error sintáctico: fin de archivo inesperado")

# Construcción del analizador sintáctico
parser = yacc()

if __name__ == '__main__':
    app.run(debug=True)

