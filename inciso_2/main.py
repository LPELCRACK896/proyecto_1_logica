{("p", False), ("q", False),        ("q", True), ("s", False), ("p", False), ("s", True), ("q", False), ("s", True)}
{("p", False), ("q", False),("q", True), ("s", False), ("p", False), ("s", True), ("q", False), ("s", True)}

("p", False), ("q", False), ("q", True), ("s", False), ("p", False), ("s", True), ("q", False), ("s", True)

[["p", False], ["q", False],["q", True], ["s", False], ["p", False], ["s", True], ["q", False], ["s", True]]

def __select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]
 
def dpll(cnf, assignments={}):
 
    if len(cnf) == 0:
        return True, assignments
 
    if any([len(c)==0 for c in cnf]):
        return False, None
 
    p = __select_literal(cnf)
 
    new_cnf = [c for c in cnf if (p, True) not in c]
    new_cnf = [c.difference({(p, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{p: True}})
    if sat:
        return sat, vals
 
    new_cnf = [c for c in cnf if (p, False) not in c]
    new_cnf = [c.difference({(p, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{p: False}})
    if sat:
        return sat, vals
        
     q = __select_literal(cnf)
 
    new_cnf = [c for c in cnf if (q, True) not in c]
    new_cnf = [c.difference({(q, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{q: True}})
    if sat:
        return sat, vals
 
    new_cnf = [c for c in cnf if (q, False) not in c]
    new_cnf = [c.difference({(q, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{q: False}})
    if sat:
        return sat, vals
        
     s = __select_literal(cnf)
 
    new_cnf = [c for c in cnf if (s, True) not in c]
    new_cnf = [c.difference({(s, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{s: True}})
    if sat:
        return sat, vals
 
    new_cnf = [c for c in cnf if (s, False) not in c]
    new_cnf = [c.difference({(s, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{s: False}})
    if sat:
        return sat, vals
 
    return False, None
