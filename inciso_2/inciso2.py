# Proyecto 1 - Logica Matematica
import random



def random_literal(formula):
    for clausula in formula:
        for literal in clausula:
            return literal[0]


# Algoritmo davis-putnam-logemann-loveland
# Devuelve una tupla (exito, asignaciones) indicando si la formula es satisfacible
def DPLL(formula, asignaciones={}):
    # caso base
    if len(formula) == 0:
        return True, asignaciones
    if any([len(c) == 0 for c in formula]) > 0:
        return False, None
    l = random_literal(formula)
    # Intentar siguiendo la rama positiva
    new_cnf = []
    for clausula in formula:
        if (l, True) not in clausula:
            new_cnf.append(clausula)
    for i in range(len(new_cnf)):
        new_cnf[i] = new_cnf[i].difference({(l, False)})
    sat, vals = DPLL(new_cnf, {**asignaciones, **{l: True}})
    if sat:
        return sat, vals

    # Intentar otra vez pero siguiendo la rama negativa
    new_cnf = []
    for clausula in formula:
        if (l, False) not in clausula:
            new_cnf.append(clausula)
    for i in range(len(new_cnf)):
        new_cnf[i] = new_cnf[i].difference({(l, True)})
    sat, vals = DPLL(new_cnf, {**asignaciones, **{l: False}})
    if sat:
        return sat, vals
    return False, None





