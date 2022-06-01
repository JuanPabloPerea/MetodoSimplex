import numpy as np
class DualSimplex(object):
    #Constructor (función de inicialización)
    def __init__(self,z,B,bound):  
        self.X_count=len(z)          # Número de variables
        self.b_count=len(bound)      # Número de restricciones
        self.z=z                     #Función objetiva
        self.C=[]                    #Verifique el número
        self.B=B                     #Variables base, debido a las reglas de operación, las variables base deben darse en orden
        self.bound=bound             #Constraints, incluida la constante final derecha
        self.flag=0                  #Tipo de solución, 0 es (temporalmente) ninguna solución, 1 es la única solución óptima
        self.special=False           #Constraints Todos los coeficientes son mayores o iguales a 0, no hay una solución factible
    #Iteración (), función de iteración
    def Iteration(self):    	
        lim=100		#Evita la iteración infinita
        while(lim>0):
            self.C=[] #Check number clear
            for j in range(self.X_count):     
                zj=0
                for i in range(self.b_count): # Atraviese el coeficiente de fila completo de la j-ésima columna y calcule el número de prueba de la j-ésima variable
                    zj+=self.bound[i][j]*self.z[self.B[i]]#Restringir el orden de las variables base B
                self.C.append(self.z[j]-zj) #Check number, 'cj-zj'
            self.Check() # Juzgar si la iteración ha terminado
            if self.flag>0: # Solución, termina la iteración
                break
            else: # De lo contrario, transformación base (rotación)
                self.pivot()
                lim-=1

        #Si hay una solución óptima, genere la solución óptima y el valor extremo de la función objetivo
        X=[0]*self.X_count
        count=0
        for i in self.B:
                X[i]=self.bound[count][self.X_count]
                count+=1
        Z=0
        for i in range(self.X_count):
            Z+=self.z[i]*X[i]
        if self.special:
            print("No hay solución factible")
        elif self.flag==1:
            print("Existe una solución óptima única",X,format(Z,'.2f'))  
        elif self.flag==0:
            print("Sin solución")

    #Check (), compruebe si es la solución óptima
    def Check(self):   	
        self.flag=1
        for i in range(self.b_count):
            if self.bound[i][self.X_count]<0:		#Si hay restricciones en el extremo derecho de la constante es negativa, continúe iterando
                self.flag=0
                break 

    #pivot (), transformación base (rotación)
    def pivot(self):
        [i,j,main]=self.FindMain()  # Método de simplicidad: encuentra el elemento principal
        self.B[i]=j                 # La variable de intercambio en la variable base se reemplaza con la variable de intercambio
        for x in range(self.X_count+1):	#Transforma la línea de la variable base
            self.bound[i][x]=self.bound[i][x]/main
        for k in range(self.b_count):	#Transforma otras líneas
            if k!=i:
                times=self.bound[k][j]  #múltiple
                for t in range(self.X_count+1):
                    temp=self.bound[i][t]*times
                    self.bound[k][t]=self.bound[k][t]-temp

    def FindMain(self):                 #Encuentre el elemento principal de acuerdo con la regla θ y determine las variables swap-in y swap-out
        matbound=np.mat(self.bound)
        if np.min(matbound[:,:-1])>=0:
            self.special=True
        bi=[]
        for i in range(self.b_count):
            bi.append(self.bound[i][self.X_count])
        iout=bi.index(min(bi))          #OK para intercambiar variables  
        Theta=[]                        #θ
        for j in range(self.X_count):
            if self.bound[iout][j]>=0 or self.C[j]==0:      #El dividendo no es 0, el divisor debe ser menor que 0
                theta=float('inf')      # Da un número infinito positivo para una fácil eliminación
            else:
                theta=self.C[j]/self.bound[iout][j]
            Theta.append(theta)
        jin=Theta.index(min(Theta))      #OK para intercambiar variables
        main=self.bound[iout][jin]        
        return [iout,jin,main]
m=DualSimplex([-2,-3,-4,0,0],[3,4],[[-1,-2,-1,1,0,-3],[-2,1,-3,0,1,-4]])
n=m.Iteration()