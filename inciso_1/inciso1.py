

""" Recibe [p, q, r] ,'pqr'"""
from collections import namedtuple



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

CLAUS = namedtuple('Point3', ['terminos', 'nivel', 'negado'])
def get_tuplas_clausulas_list(cadena, variables  ='abcdefghijklmnopqrstuvwxyz' ):
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

def evaluar_expresion(list_tuplas, cadena_binaria):
    pass