from collections import namedtuple

def get_variables_from_expression(expression, alfabeto = 'abcdefghijklmnopqrstuvwxyz'):
    return list({char for char in expression if char in alfabeto})

def calcula_cadenas_binarias(cadena, alfabeto = 'abcdefghijklmnopqrstuvwxyz'):
    """A partir de una una expresion (cadena) en forma de clausula, calcula cuales son los posibles valores de verdad para cada una de las variables (p, q, r...)
    de las que este compuesta en forma de cadena binaria. Las posibilidades vienen en una lista de cadena binaria en la que 0 es False y 1 True.

    Args:
        cadena (str): Ingresa en un solo string, sin separaciones las variables de la expresion algebraica
        alfabeto (str, optional): . Defaults to 'abcdefghijklmnopqrstuvwxyz'.

    Returns:
        list: Lista de cadenas binarias
    """    
    comb = 2**(len(get_variables_from_expression(cadena, alfabeto)))
    size = len(bin(comb-1)[2:])
    cadenas = []
    for i in range(comb):
        cadena = str(bin(i)[2:])
        while size!=len(cadena):
            cadena = '0'+cadena
        cadenas.append(cadena)
    return cadenas

def get_tuplas_clausulas_list(cadena, variables  ='abcdefghijklmnopqrstuvwxyz' ):
    """A partir de una una expresion (cadena) en forma de clausula, transforma la clausula en una lista de tuplas compuesto por una LISTA DE
    TERMINOS que contienen sus terminos ya sea como variables o indices de otras clausulas; NIVEL, indica que tan interna es la clausa respecto 
    a las otras; NEGADO, si el termino en cuestion es negado. 

    Args:
        cadena (str): Cadena que contiene la clausula. 
        variables (str, optional): Una cadena de todas las variables esperadas en la epxresion (Ej: 'pqrs'). Defaults to 'abcdefghijklmnopqrstuvwxyz'.
    Raises:
        Exception: En caso la expresión no se de de la forma correcta, que la expresión implique niveles negativos de clausulas, se este cerrando una clausula sin haberla abierto, 
        el ingreso de un caracter que no forme para del alfabeto o sea '{', '}', ',', ' '.  

    Returns:
        list: Lista con tuplas de cada clausula dentro de la expresion con formato detallado en la descripcion. 
    """    
    CLAUS = namedtuple('Clausula', ['terminos', 'nivel', 'negado'])
    clausulas = []
    nivel = 0
    clausulas_pendientes = -1 #stack
    negado = False
    salir = False
    while not salir:
        char = cadena[0]
        if char=='{': # Apertura
            clausulas_pendientes += 1 
            nivel += 1
            clausulas.append(CLAUS([], nivel, negado))
            negado = False
        elif char=='}':#Cierre de clausula
            if clausulas_pendientes<0:
                raise Exception("Error en la cadena")
            if clausulas_pendientes>0:
                nivel_inferior = clausulas[-1].nivel - 1
                index_clausula = clausulas.index(clausulas[-1])
                nivel -= 1
                if nivel_inferior<0:
                    raise Exception("Formato incorrecto de clausula")
                for clausula in clausulas:
                    if clausula.nivel==nivel_inferior:
                        clausula.terminos.append(index_clausula)
            clausulas_pendientes -= 1    
            negado = False
        elif char=='~': #Negacion
            negado = not negado
        else:
            if char in variables: #terminos
                if len(clausulas)<=0:
                    raise Exception("Error en la cadena")
                clausulas[-1].terminos.append(char if not negado else '~'+char)
                negado = False  
            elif not (char==',' or char==' '):
                raise Exception("Error en caracter")
        cadena = cadena[1:]
        if clausulas_pendientes<0 and not negado:
            salir = True
        elif len(cadena)==0:
            raise Exception('Error en la cadena')
    return clausulas

def evaluar_clausula(clausula, lista_clausulas: list, variables_valuadas):
    """Permite determinar el valor de una clausula. 

    Args:
        clausula (list): Tupla con caracteristicas de una clausula. 
        lista_clausulas (list): Clausulas involucradas en la expresion. 
        variables_valuadas (dict): Variables involucradas en la expresion. 

    Returns:
        bool: Valor de la clausula ingresada. 
    """    
    operacion = 'and' if clausula.nivel ==1 else 'or'
    valuadas = []
    for termino in clausula.terminos:
        #Evaluacion de terminos
        if type(termino)== int:
            valuadas.append(evaluar_clausula(lista_clausulas[termino], lista_clausulas, variables_valuadas))
        else:
            if termino[0]=='~':
                valuadas.append(not variables_valuadas.get(termino[1]))
            else:
                valuadas.append(variables_valuadas.get(termino[0]))
        #Precipita una respuesta de toda la expresion segun le ultimo valor obtenido y la operacion en la que esta implicada directamente
        if operacion=='and' and valuadas[-1]==False:
            return False
        elif operacion=='or' and valuadas[-1]==True:
            return True
    """             
    #Seccion sustituida por la linea que le sigue
    if operacion=='and': #AND: Si llego a este punto, todos los valuadas fueron true, porque si no habria retornado en la linea 96
        return True
    else: #or: Si llego a este punto significa que no encontro ningun True (hubiera retornado en ln 98), todas son False por tanto toda la expresion lo es
        return False 
    """
    return operacion=='and'
    
def evaluar_expresion(expresion_claus, alfabeto = 'abcdefghijklmnopqrstuvwxyz'):
    """A partir de una expresion brinda los resultados segun se evaluen. De el diccionario resultante es posible ver si es satisfacible

    Args:
        expresion_claus (_type_): Clausula inicial
        alfabeto (str, optional): Cadena de letras permitidas como variables dentro de la expresion. Defaults to 'abcdefghijklmnopqrstuvwxyz'.

    Returns:
        dict: Diccionario con cada cadena binaria y su valor
    """    
    cadenas_binarias = calcula_cadenas_binarias(expresion_claus, alfabeto)
    exp_claus_forma_tuplas = get_tuplas_clausulas_list(expresion_claus, alfabeto)
    cadenas_resultados = {}
    variables = get_variables_from_expression(expresion_claus, alfabeto)
    for cadena_b in cadenas_binarias:
        if len(variables) != len(cadena_b):
            print("Error inesperado")
            return
        dicc = { variables[i]: True if cadena_b[i]=='1' else False for i in range(len(cadena_b))}

        cadenas_resultados[cadena_b] = evaluar_clausula(exp_claus_forma_tuplas[0], exp_claus_forma_tuplas, dicc )
    satisfacible = []
    for cadena in cadenas_resultados:
        if cadenas_resultados[cadena]==True:
            satisfacible.append({variables[char] : cadena[char] for char in range(len(cadena)) })
            #break #Para que solo muestre un resultado que hace satisfacible 
    if len(satisfacible) == len(cadenas_resultados):
        print("Es tautologia")
    elif len(satisfacible)==0:
        print("Es contradiccion")
    return satisfacible if len(satisfacible)>0 else False #, [cadena for cadena in cadenas_resultados if cadenas_resultados[cadena]=True]