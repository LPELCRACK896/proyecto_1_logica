from collections import namedtuple
from logging.config import valid_ident
from turtle import done
from webbrowser import get

def calcula_cadenas_binarias(cadena, alfabeto = 'abcdefghijklmnopqrstuvwxyz'):
    """A partir de una una expresion (cadena) en forma de clausula, calcula cuales son los posibles valores de verdad para cada una de las variables (p, q, r...)
    de las que este compuesta en forma de cadena binaria. Las posibilidades vienen en una lista de cadena binaria en la que 0 es False y 1 True.

    Args:
        cadena (str): Ingresa en un solo string, sin separaciones las variables de la expresion algebraica
        alfabeto (str, optional): . Defaults to 'abcdefghijklmnopqrstuvwxyz'.

    Returns:
        _type_: list
    """    
    cant_variables = 0
    alf = []
    for i in cadena:
        if i in alfabeto and i not in alf:
            cant_variables += 1
            alf.append(i)
    comb = 2**(cant_variables)
    size = len(bin(comb-1)[2:])
    cadenas = []
    for i in range(comb):
        cadena = str(bin(i)[2:])
        while size!=len(cadena):
            cadena = '0'+cadena
        cadenas.append(cadena)
    return cadenas

def get_tuplas_clausulas_list( cadena, variables  ='abcdefghijklmnopqrstuvwxyz' ):
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
    while True:
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
            elif char==',' or char==' ':
                pass
            else:
                raise Exception("Error en caracter")
        cadena = cadena[1:]
        if clausulas_pendientes<0 and not negado:
            break
        elif len(cadena)==0:
            raise Exception('Error en la cadena')
    return clausulas

def evaluar_clausula(clausula, lista_clausulas, variables_valuadas):
    """Permite determinar el valor de una clausula. 

    Args:
        clausula (_type_): Tupla con caracteristicas de una clausula. 
        lista_clausulas (_type_): Clausulas involucradas en la expresion. 
        variables_valuadas (_type_): Variables involucradas en la expresion. 

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

def evaluar_expresion(expresion_claus):
    pass