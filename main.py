

#Llenamos el total de documentos
total = 0
listaMatriz = []
listaClases = []
dictMatriz = {}

#Los K mas relevantes del escalafon
K=10

#listas
trainingSet=[]
testSet=[]

#Almacena los resultados del algoritmo
newClass=[]

#Estructura de dato de cada entrada de la colección
class Documento:
    def __init__(self,docId,clase,numTerminos,pesosXTermino):
        self.docId=docId
        self.clase=clase
        self.numTerminos=numTerminos
        self.pesosXTermino=dict([(x.split("/")[0],float(x.split("/")[1])) for x in pesosXTermino.split(" ")])
        

#Llenamos la lista trainingSet
with open ("training-set.csv","r")as trainingDoc:
    trainingDoc.readline()
    trainingSet=[Documento(*linea.split("\t")) for linea in trainingDoc.readlines()]

#Llenamos la lista testSet
with open ("test-set.csv","r") as clase:
    clase.readline()
    testSet=[Documento(*linea.split("\t")) for linea in clase.readlines()]

#Llenamos dicionario con matrices
with open ("clases.csv","r") as clase:
    clase.readline()
    listaClases=[linea.split("\t") for linea in clase.readlines()]
    for i in range(len(listaClases)):
        dictMatriz[listaClases[i][0]] = [[0] * 3 for i in range(3)]

def Consultar(testDoc):
    similitudes={}
    for trainingDoc in trainingSet: #Comparo cada clase de test con todos los del training
        similitudes[trainingDoc]=0
        #print(trainingDoc.clase)
        for termino,peso in testDoc.pesosXTermino.items():   #(termino:peso)
            if termino in trainingDoc.pesosXTermino:
                # Si el termino de la clases coinciden le sumo a la variable similitud el producto de ambos terminos
                similitudes[trainingDoc]+=peso*trainingDoc.pesosXTermino[termino]
    escalafon=list(similitudes.items()) #Se crea el escalafón
    escalafon.sort(key=lambda x:x[1],reverse=True)  #Se acomoda de mayor a menor
    return escalafon
def metricasDeEvaluacion(claseReal,claseAsignada):
    if claseReal == claseAsignada:
        dictMatriz[claseAsignada][0][0] += 1
        dictMatriz[claseAsignada][2][0] += 1
        dictMatriz[claseAsignada][0][2] += 1
    else:
        dictMatriz[claseAsignada][0][2] += 1
        dictMatriz[claseReal][2][0] += 1

#print("DocId","Real","Clasificador",sep="\t")
for clase in testSet:
    #Se obtiene el escalafón
    escalafon=Consultar(clase)

    clases={}
    #Se analizan los K más relevantes, se extrae la similitud por clase
    for doc,sim in escalafon[:K]:
        clases[doc.clase] = [sim] + (clases[doc.clase] if doc.clase in clases else [])
    #Se hace el promedio de similitudes por clase
    promedioXClase=[(sum(x) / len(x), y) for y, x in clases.items()]
    promedioXClase.sort(reverse=True)
    #Y se escoje el de promedio más alto
    newClass+=[promedioXClase[0][1]]
    #print(testDoc.docId,testDoc.clase,promedioXClase[0][1],sep="\t")
    total+=1
    metricasDeEvaluacion(clase.clase, promedioXClase[0][1])

#Hacer el análisis de resultados
def imprimirMatriz(clase,matriz):
    matriz[2][2] = total
    matriz[0][1]=matriz[0][2]-matriz[0][0]
    matriz[1][0]=matriz[2][0]-matriz[0][0]
    matriz[2][1]=matriz[2][2]-matriz[2][0]
    matriz[1][2]=matriz[2][2]-matriz[0][2]
    matriz[1][1]=matriz[1][2]-matriz[1][0]
    print(clase)
    print("        ----R E A L----",sep="\t")
    print("         A    ¬A")
    print("C|    ------------------")
    print("L|  A | ",matriz[0][0]," | ",matriz[0][1]," | ",matriz[0][2]," |")
    print("A| ¬A | ",matriz[1][0]," | ",matriz[1][1]," | ",matriz[1][2]," |")
    print("S|    | ",matriz[2][0]," | ",matriz[2][1]," | ",matriz[2][2]," |")
    print("I|    ------------------",sep="\t")


def evaluarResultados(matriz):
    print("Acierto = ",(matriz[1][1]+matriz[0][0])/matriz[2][2])
    print("Error = ",(matriz[0][1]+matriz[1][0])/matriz[2][2])
    print("Precisión = ",matriz[0][0]/matriz[0][2])
    print("Recall = ",matriz[0][0]/matriz[2][0])
    print(sep="\t")
    print(sep="\t")


while True:
    # Imprimimos el menú en pantalla
    for i in  range(len(listaClases)):
        print(i+1,")",listaClases[i][0])
    # Leemos lo que ingresa el usuario
    eligio=input("-Que resultado desea ver? :")
    # Según lo que ingresó, código diferente
    if int(eligio)-1 < 0 or int(eligio)-1 >= len(listaClases):
        print("Opción no válida")
    else:
        imprimirMatriz(listaClases[int(eligio)-1][0],dictMatriz[listaClases[int(eligio)-1][0]])
        evaluarResultados(dictMatriz[listaClases[int(eligio)-1][0]])


