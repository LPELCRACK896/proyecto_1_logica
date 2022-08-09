import inciso1 as inc
import pandas as pd

while True:
    res = input("1. Ingresar expresion boolean en forma clausulal \n2. Salir\n")
    if res == '1':
        """
         mamadas par que quede una tabla de verdad
         p     |    q     |   r    | ... 
        1           0           1
            etc...
         """
        exp = input("Ingresar expresion booleana en forma clausulal\n")
        resultado = inc.evaluar_expresion(exp)
        df = pd.DataFrame(resultado, columns = ['p','q','r'])
        print(df)
    elif res == '2':
        break
    else:
        print("Ingrese una opcion valida")