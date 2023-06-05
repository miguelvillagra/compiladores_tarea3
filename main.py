from ply import yacc
import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens y expresiones regulares para los tokens
tokens = [
    'L_CORCHETE',
    'R_CORCHETE',
    'L_LLAVE',
    'R_LLAVE',
    'COMA',
    'DOS_PUNTOS',
    'LITERAL_CADENA',
    'LITERAL_NUM',
    'PR_TRUE',
    'PR_FALSE',
    'PR_NULL'
]

t_L_CORCHETE = r'\['
t_R_CORCHETE = r'\]'
t_L_LLAVE = r'\{'
t_R_LLAVE = r'\}'
t_COMA = r','
t_DOS_PUNTOS = r':'
t_LITERAL_CADENA = r'\".*?\"'
t_LITERAL_NUM = r'\d+(\.\d+)?((e|E)(\+|-)?\d+)?'
t_PR_TRUE = r'true|TRUE'
t_PR_FALSE = r'false|FALSE'
t_PR_NULL = r'null|NULL'
t_ignore = ' \t\n'

# Función de manejo de errores
def t_error(t):
    print(f"Error de análisis léxico: Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()

# Reglas de la gramática
def p_json(p):
    '''json : element'''
    p[0] = p[1]
    if p.parser.token() is None:  # Verificar si se ha alcanzado el fin de archivo
        print("Análisis sintáctico exitoso. El archivo fuente es válido.")
    else:
        token = p.parser.token()
        
        print(f"Error de análisis sintáctico: Token inesperado '{token.value}' en la línea {token.lineno}, posición {token.lexpos}")

def p_element(p):
    '''element : object
               | array'''
    p[0] = p[1]

def p_array(p):
    '''array : L_CORCHETE C'''
    p[0] = p[2]

def p_C(p):
    '''C : element_list R_CORCHETE
         | R_CORCHETE'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1]

def p_element_list(p):
    '''element_list : element A'''
    p[0] = [p[1]] + p[2]

def p_A(p):
    '''A : COMA element A
         |'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_object(p):
    '''object : L_LLAVE D'''
    if len(p) == 2:
        p[0] = {}
    else:
        p[0] = dict(p[2])

def p_D(p):
    '''D : attributes_list R_LLAVE
         | R_LLAVE'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1]

def p_attributes_list(p):
    '''attributes_list : attribute B'''
    p[0] = [p[1]] + p[2]

def p_B(p):
    '''B : COMA attribute B
         |'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_attribute(p):
    'attribute : attribute_name DOS_PUNTOS attribute_value'
    p[0] = (p[1], p[3])

def p_attribute_name(p):
    'attribute_name : LITERAL_CADENA'
    p[0] = p[1]

def p_attribute_value(p):
    '''attribute_value : element
                       | LITERAL_CADENA
                       | LITERAL_NUM
                       | PR_TRUE
                       | PR_FALSE
                       | PR_NULL'''
    p[0] = p[1]

# Función de manejo de errores
def p_error(p):
    if p:
        print(f"Error de análisis sintáctico: Token inesperado '{p.value}' en la línea {p.lineno}, posición {p.lexpos}")
    else:
        print("Error de análisis sintáctico: Fin de archivo inesperado")


# Construir el analizador sintáctico
parser = yacc.yacc()

# Traducción a XML
def translate_json_to_xml(source_code):
    result = parser.parse(source_code)
    if result is not None:
        print("Análisis sintáctico exitoso. El archivo fuente es válido.")
        xml = generate_xml(result)
        return xml
    else:
        print("Análisis sintáctico fallido. Se encontraron errores.")
        return None


# Función para generar el XML a partir de la estructura de datos
def generate_xml(data):
    if isinstance(data, dict):
        xml = ""
        for key, value in data.items():
            xml += f"<{key}>"
            xml += generate_xml(value)
            xml += f"</{key}>"
        return xml
    elif isinstance(data, list):
        xml = ""
        for item in data:
            xml += "<item>"
            xml += generate_xml(item)
            xml += "</item>"
        return xml
    else:
        return str(data)

# Función principal
def main():
    # Leer el archivo fuente JSON
    filename = "fuente.json"
    with open(filename, "r") as file:
        source_code = file.read()
    
    # Traducir el archivo fuente a XML
    xml = translate_json_to_xml(source_code)
    
    # Imprimir el resultado solo si no hay errores de análisis sintáctico
    if xml is not None:
        print(xml)

if __name__ == '__main__':
    main()
