

""" Recibe [p, q, r] ,'pqr'"""
from collections import namedtuple
from logging.config import valid_ident
from turtle import done
from webbrowser import get



def calcula_cadenas_binarias(cadena, alfabeto = 'abcdefghijklmnopqrstuvwxyz'):
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

def get_tuplas_clausulas_list(cadena, variables  ='abcdefghijklmnopqrstuvwxyz' ):
    CLAUS = namedtuple('Point4', ['terminos', 'nivel', 'negado', 'valor'])
    clausulas = []
    nivel = 0
    clausulas_pendientes = -1 #stack
    negado = False
    while True:
        char = cadena[0]

        if char=='{': # Apertura
            clausulas_pendientes += 1 
            nivel += 1
            clausulas.append(CLAUS([], nivel, negado, [None]))
            negado = False
        elif char=='}':#Cierre de clausula
            if clausulas_pendientes<0:
                raise Exception("Error en la cadena")
            if clausulas_pendientes>0:
                nivel_inferior = clausulas[-1].nivel - 1
                index_clausula = clausulas.index(clausulas[-1])
                nivel -= 1
                if nivel_inferior<0:
                    print("error en cadena")
                    break
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

def evaluar_expresion(list_tuplas, cadena_binaria, variables):
    if len(cadena_binaria)!=len(variables):
        raise Exception("Hubo un error al ingresar las variables involucradas")
    variables_valuadas = { variables[i]: True if cadena_binaria[i]=='1' else False for i in range(len(cadena_binaria))}
    #list_tuplas[0].valor[0] = False

def evaluar_clausula(clausula, lista_clausulas, variables_valuadas):
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

print(evaluar_clausula(get_tuplas_clausulas_list('{{~p}, {q}}')[0], get_tuplas_clausulas_list('{{p}, {q}}'), {'p': 0, 'q': 1}))
def verifica_si_es_satisfactible(expresion):
    pass