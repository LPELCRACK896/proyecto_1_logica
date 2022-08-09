import inciso1 as inc
import pandas as pd
expresiones =[]

def formatRes(resultado):
    print("\nCombinaciones que la hacen satisfacibles: ")
    header  = '| '
    for variable in resultado[0].keys():
        header += variable+' | '
    print(header)
    for rw in resultado:#lista
        row = '|'
        for value in rw:#diccionario
            row += ' '+str(rw.get(value))+' |'
        print(row)

def simulacion(expresiones: list):
    for r in expresiones:
        print("Expresion evaluada: {r}\n")
        input("Ver resultado... ")
        resultado = inc.evaluar_expresion(r)
        if resultado:
            formatRes(resultado)
        else:
            print("La expresion no es satisfacible")
        input("Siguiente expresion...\n")

while True:
    res = input("1. Ingresar expresion boolean en forma clausulal \n3. Salir\n")
    if res == '1':
        exp = input("Ingresar expresion booleana en forma clausulal\n")
        resultado = inc.evaluar_expresion(exp)
        df = pd.DataFrame(resultado, columns = ['p','q','r'])
        print(df)
    elif res=='2':
        simulacion(expresiones)
        input("Enter para regresar el menu")
    elif res == '3':
        break
    else:
        print("Ingrese una opcion valida")
 
