import inciso2 as i2

print('\nPROYECTO 1 - LOGICA MATEMATICA\n')

print("p ∧ ~p")
print(i2.DPLL([{("p", True)}, {("p", False)}]))

print("\nq V p V ~p")
print(i2.DPLL([{("q", True), ("p", True), ("p", False)}]))

print("\n(~p V ~r V ~s) ∧ (~q V ~p V ~s)")
print(i2.DPLL([{("p", False), ("r", False), ("s", False)}, 
               {("q", False), ("p", False), ("s", False)}]))

print("\n(~p V ~q) ∧ (q V ~s) ∧ (~p V s) ∧ (~q V s)")
print(i2.DPLL([{("p", False), ("q", False)}, 
               {("q", True), ("s", False)},
               {("p", False), ("s", True)}, 
               {("q", False), ("s", True)}]))

print("\n(~p V ~q V ~r) ∧ (q V ~r V p) ∧ (~p V q V r)")

print(i2.DPLL([{("p", False), ("q", False), ("r", False)},
               {("q", True), ("r", False), ("p", True)},
               {("p", False), ("q", True), ("r", True)}]))

print("\nr ∧ (~q V ~r) ∧ (~p V q V ~r) ∧ q")
print(i2.DPLL([{("r", True)},
               {("q", False), ("r", False)}, 
               {("p", False), ("q", True), ("r", False)},
               {("q", True)}]))
print("\n")
