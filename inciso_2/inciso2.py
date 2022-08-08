# Proyecto 1 - Logica Matematica
import random


def get_literals(B_):
    B_list = [i for sub in B_ for i in sub]
    print(B_list)
    no_neg = [*set((B_list[i], True) if len(B_list[i]) < 2
                   else (B_list[i][1:], False)
                   for i in range(len(B_list)))]
    return no_neg

# def formula_to_literals(formula):


def random_literal(formula):
    for clausula in formula:
        for literal in clausula:
            return literal[0]

def generate_BC(Blist, lit):
    litComp = '~' + lit if len(lit) == 1 else lit[1:]
    for j in Blist:
        if litComp in j:
            j.remove(litComp)
    for k in Blist:
        if lit in k:
            Blist.remove(k)
    return Blist


# Algoritmo davis-putnam-logemann-loveland
# Devuelve una tupla (exito, asignaciones) indicando si la formula es satisfacible
def DPLL(formula, asignaciones={}):
    # caso base
    if len(formula) == 0:
        return True, asignaciones
    if any([len(c) == 0 for c in formula]) > 0:
        return False, None
    l = random_literal(formula)
    new_cnf = []
    for clausula in formula:
        if (l, True) not in clausula: new_cnf.append(clausula)
    for i in range(len(new_cnf)):
        c = clausula.difference({(l, False)})
        new_cnf[i] = c

    sat, vals = DPLL(new_cnf, {**asignaciones, **{l: True}})
    if sat:
        return sat, vals
    new_cnf = []
    for clausula in formula:
        if (l, False) not in clausula: new_cnf.append(clausula)
    for i in range(len(new_cnf)):
        c = clausula.difference({(l, True)})
        new_cnf[i] = c
    sat, vals = DPLL(new_cnf, {**asignaciones, **{l: False}})
    if sat:
        return sat, vals
    return False, None




print(DPLL([{("p", True), ("q", False)}, {("p", True), ("r", True)}]))
