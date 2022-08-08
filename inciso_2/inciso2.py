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


def DPLL(formula, asignaciones={}):
    # caso base
    if len(formula) == 0:
        return True, asignaciones
    if any([len(c) == 0 for c in formula]) > 0:
        return False, None
    l = random_literal(formula)
    new_cnf = [clausula for clausula in formula if (l, True) not in clausula] # No incluir la clausula si contiene (l, True)
    new_cnf = [clausula.difference({(l, False)}) for clausula in new_cnf] # Eliminar el valor negado de l de las otras clausulas
    sat, vals = DPLL(new_cnf, {**asignaciones, **{l: True}})
    if sat:
        return sat, vals
    new_cnf = [clausula for clausula in formula if (l, False) not in clausula]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = DPLL(new_cnf, {**asignaciones, **{l: False}})
    if sat:
        return sat, vals

    return False, None

def dpll(cnf, assignments={}):
    if len(cnf) == 0:
        return True, assignments

    if any([len(c) == 0 for c in cnf]):
        return False, None

    l = random_literal(cnf)

    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals
    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals

    return False, None



print(DPLL([{("p", True), ("q", False)}, {("p", True), ("r", True)}]))
