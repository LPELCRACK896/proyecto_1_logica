import inciso2 as i2

print("p ∧ ~p")
print(i2.DPLL([{("p", True)}, {("p", False)}]))
print("q ∨ p ∨ ~p")
print(i2.DPLL([{("q", True), ("p", True), ("p", False)}]))