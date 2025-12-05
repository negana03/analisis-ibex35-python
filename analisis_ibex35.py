"""
Contamos con un archivo que contiene los datos de las cotizaciones del IBEX 35
organizado en el siguiente formato:

Cabecera:
    "Fecha", "Último valor", "Apertura", "Máximo", "Mínimo", "Volumen",
    "% Variación"
Datos:
    "Fecha1", "ÚltimoValor1", "ValorApertura1", "MáximoDiario1",
    "MínimoDiario1", "VolumenNegociado1", "VariaciónInterdiaria1%" ...

La información en el fichero está ordenada desde una fecha más moderna a
una fecha más antigua. 

El siguiente programa procesa este archivo, almacena los datos en una
estructura adecuada y presenta al usuario un menú interactivo con 6 opciones
para que realice distintas consultas.


Autora: Galera Navarro, Nerea 
"""

"""
En cuanto al código, comenzamos importando las bibliotecas necesarias,
luego definimos las clases Fecha e InfoDiaria. A continuación, procedemos con
la implementación de las funciones, siguiendo el orden establecido por el menú.

El menú continuará apareciendo después de cada consulta, hasta que el usuario
seleccione explícitamente la opción 6) Salir.
    
Para generar la gráfica, utilizamos la función pyplot de la biblioteca
matplotlib, tal como se especifica en el guion.
"""

import matplotlib.pyplot as plt

class Fecha:
    def __init__(self):
        self.dia = list() #de int
        self.mes = list() #de int
        self.año = list() #de int

class InfoDiaria:
    def __init__(self):
        self.fecha = Fecha()
        self.ultimovalor = list() #de float
        self.apertura = list() #de float
        self.max = list() #de float
        self.min = list() #de float
        self.volumen = list() #de str
        self.variacion = list() #de str

    
def LeerFichero(nombre_fichero: str, info: InfoDiaria):
    """
    Esta función lee la información de un fichero y la guarda en la estructura
    de datos correspondiente (registros).
    
    Para poder guardar los datos como float:        
      1. Eliminamos las comillas, los puntos, porcentajes y las 'M' y 'B'.
      2. Sustitimos las comas por puntos (para indicar los decimales).

    Parameters
    ----------
    info : InfoDiaria
        Variable de tipo InfoDiaria con la información sobre las cotizaciones.

    Returns
    -------
    bool
        True si se ha podido leer y cargar correctamente el fichero. 
        False si ha ocurrido algún error.
    """
    
    try:
        fich = open(nombre_fichero, encoding = "UTF-8")
        
    except:
        ok = False
        print("Error en la apertura del fichero. ")
        
    else:
        ok = True
        fich.readline()
        linea = fich.readline().rstrip("\n")
        
        lista_fechas = []
        
        while linea != '':
            
            # Eliminamos las comillas del inicio y final de la línea
            linea = linea.strip('"')  
            linea = linea.split('","')
            
            # Eliminamos los puntos, sustituimos las comas para separar los 
            # decimales por puntos y eliminamos la M de millón
            for caracter in linea:                
                i = linea.index(caracter)
                linea[i] = caracter.replace('.', '')                
                linea[i] = linea[i].replace(',', '.')
                linea[i] = linea[i].replace('%', '')
                linea[i] = linea[i].replace('M', '')
            
            # Remplazamos las posibles B (de billones) presentes y convertimos
            # la suma a millones
                if 'B' in caracter:
                    linea[i] = linea[i].replace('B', '')
                    linea[i] = float(linea[i]) * 1000 # Convertimos a millones
            
            # Rellenamos las listas con la información correspondiente
            lista_fechas.append(linea[0])
            info.ultimovalor.append(float(linea[1]))
            info.apertura.append(float(linea[2]))
            info.max.append(float(linea[3]))
            info.min.append(float(linea[4]))
            info.volumen.append(float(linea[5]))
            info.variacion.append(float(linea[6]))
            
            linea = fich.readline().rstrip("\n")    
     
        fich.close()  
        
        info.fechas = ClaseFecha(lista_fechas)       
      
    return ok, info

def ClaseFecha(lista_fechas: list) -> Fecha:
    """
    Función que crea una variable de tipo Fecha a partir de la lista de 
    fechas leídas del fichero.
    
    Parameters
    ----------
    lista_fechas : list
        Lista de str leídas del fichero que representan fechas (formato 
        ddmmaaa).

    Returns
    -------
    info_fechas : Fecha
        Variable de tipo Fecha con la información de la lista
        El día, mes y año de cada fecha se guardan como enteros.

    """
    
    info_fechas = Fecha()
    
    # Recorremos los elementos de la lista de fechas
    for fecha in lista_fechas:
        dia = int(fecha[0:2])
        info_fechas.dia.append(dia)
        
        mes = int(fecha[2:4])
        info_fechas.mes.append(mes)
        
        año = int(fecha[4:8])
        info_fechas.año.append(año)    
    
    return info_fechas
    
        
def ConvertirFechaEntero(dia: int, mes: int, año: int) -> int:
    """
    Esta función recibe tres enteros de una fecha (día, mes y año) y los 
    convierte a un solo entero para poder comparar esta fecha con otras.
    
    Parameters
    ----------
    dia : int
    mes : int
    año : int
        Enteros representando día, mes y año respectivamente.

    Returns
    -------
    fecha: int
        Fecha como entero.

    """
    
    fecha = int(str(año).zfill(4) + str(mes).zfill(2) + str(dia).zfill(2))

    return fecha


def PedirFecha(info) -> int:
    """
    Esta función pide al usuario una fecha (día, mes y año), la convierte 
    a entero mediante la función FechaAEntero y la devuelve.
    
    Si la fecha es anterior o posterior a las presentes en el fichero, 
    pedirá al usuario que vuelva a introducirla.
    
    Returns
    -------
    fecha: int
        Fecha como entero (formato aaaammdd).

    """
    
    # Leemos la primera y la última fecha del fichero
    fecha_posterior = ConvertirFechaEntero(info.fechas.dia[0],
                                           info.fechas.mes[0], 
                                           info.fechas.año[0])    
    fecha_anterior = ConvertirFechaEntero(info.fechas.dia[-1],
                                          info.fechas.mes[-1], 
                                          info.fechas.año[-1])
    
    print("Por favor, introduzca una fecha: ")
    dia = int(input("Día: "))
    mes = int(input("Mes: "))
    año = int(input("Año: "))
    
    fecha = ConvertirFechaEntero(dia, mes, año)

    while not fecha_anterior <= fecha <= fecha_posterior:
        print("Fecha no válida. Por favor, introduzca una fecha válida: ")
        
        dia = int(input("Día: "))
        mes = int(input("Mes: "))
        año = int(input("Año: "))
        
        fecha = ConvertirFechaEntero(dia, mes, año)
        
    return fecha


def CotMaxMin(fecha_ini: int, fecha_fin: int, info: InfoDiaria
              ) -> (float, float):
    """
    Esta función determina las cotizaciones máxima y mínima entre dos fechas
    dadas.
    Creamos una lista con las máximas y otra con las mínimas, y las vamos
    rellenando para cada día entre las fechas dadas. La cotización máxima 
    resultante será la mayor de la lista de cotizaciones máximas, y la 
    cotización mínima, la menor de la lista de cotizaciones mínimas.
    
    Parameters
    ----------
    fecha_ini : int
        Fecha inicial.
        
    fecha_fin : int
        Fecha final.
        
    info : InfoDiaria
        Variable tipo InfoDiaria con la información de las cotizaciones.

    Returns
    -------
    cot_max: float
        Valor máximo de cotización.
        
    cot_min: float
        Valor mínimo de cotización.

    """
    
    lista_cot_max = []
    lista_cot_min = []
       
    for i in range(len(info.fechas.dia)):
        dia = info.fechas.dia[i]
        mes = info.fechas.mes[i]
        año = info.fechas.año[i]
        
        fecha = ConvertirFechaEntero(dia, mes, año)
        
        if fecha_ini <= fecha <= fecha_fin:            
            lista_cot_max.append(info.max[i])
            lista_cot_min.append(info.min[i])

    cot_max = max(lista_cot_max)
    cot_min = min(lista_cot_min)
    
    return cot_max, cot_min


def VariacionPorcentual(opcion_usuario: str, fecha_ini: int, fecha_fin: int,
                  info: InfoDiaria) -> float:
    """
    Esta función calcula la variación porcentual de la cotización de apertura
    o de cierre (según se seleccione) entre dos fechas dadas.
    
    Parameters
    ----------
    fecha_ini : int
        Fecha inicial.
        
    fecha_fin : int
        Fecha final.
    
    opcion_usuario : str
        Opción elegida por el usuario.
        
    info : InfoDiaria
        Variable tipo InfoDiaria con la información de las cotizaciones.

    Returns
    -------
    variacion: float
        Variación porcentual entre las fechas indicadas.

    """
    
    lista_cotiz = []
    
    # Recorremos las fechas y cotizaciones
    for i in range(len(info.fechas.dia)):
        dia = info.fechas.dia[i]
        mes = info.fechas.mes[i]
        año = info.fechas.año[i]
        
        fecha_a_comparar = ConvertirFechaEntero(dia, mes, año)
        
        if fecha_ini <= fecha_a_comparar <= fecha_fin:
            if opcion_usuario == 'A':
                lista_cotiz.append(info.apertura[i])
                
            elif opcion_usuario == 'C':
                lista_cotiz.append(info.ultimovalor[i])

    # Comprobamos que la lista tiene al menos 2 elementos.
    # Dado que las fechas están ordenadas de más reciente a más antigua
    # invertimos los valores en cot_inicio y cot_fin
    if len(lista_cotiz) >= 2:
        cot_inicio = lista_cotiz[-1]  # El primer valor debe ser el más antiguo
        cot_fin = lista_cotiz[0]  # El último valor el más reciente
        
        # Variación porcentual 
        variacion = round(((cot_fin - cot_inicio) / cot_inicio) * 100, 4)
        
    else:
        print("Lo siento, no hay suficientes datos entre las fechas dadas. ")
        variacion = 0
    
    return variacion    
   
     
def VolumenTotal(fecha_ini: int, fecha_fin: int, vol_min: float,
             info: InfoDiaria) -> float:
    """
    Función que determina el volumen total entre dos fechas, tomando en cuenta
    sólo los días en los que se supera un volumen mínimo.
    
    Verifica si cada fecha está dentro de un rango dado, y si el volumen de
    negociación de esa fecha es mayor que el mínimo establecido, lo agrega a
    un acumulador "volumen_total".

    Parameters
    ----------
    fecha_ini : int
        Fecha inicial convertida a entero.
        
    fecha_fin : int
        Fecha final convertida a entero.
        
    vol_min : float
        Volumen mínimo a tener en cuenta.
        
    info : InfoDiaria
        Variable tipo InfoDiaria con la información de las cotizaciones.

    Returns
    -------
    volumen_total: float
        Volumen total.

    """
    volumen_total = 0
    
    for i in range(len(info.fechas.dia)):
        dia = info.fechas.dia[i]
        mes = info.fechas.mes[i]
        año = info.fechas.año[i]
        
        fecha = ConvertirFechaEntero(dia, mes, año)
        
        if fecha_ini <= fecha <= fecha_fin:
            if info.volumen[i] > vol_min:
                volumen_total += info.volumen[i]
            
    return volumen_total


def ObtenerFechasYAperturas(fecha_ini: int, fecha_fin: int,
                    info: InfoDiaria) -> (list, list):
    """
    La siguiente función recibe dos fechas: una inicial y una final, luego,
    crea una lista de fechas y otra de cotizaciones de apertura y las rellena
    con la información correspondiente.

    Parameters
    ----------
    fecha_ini : int
        Fecha inicial.
        
    fecha_fin : int
        Fecha final.
        
    info : InfoDiaria
        Variable tipo InfoDiaria con la información de las cotizaciones.

    Returns
    -------
    lista_fechas: list
        Lsita con las fechas correspondientes
        
    lista_cot_apertura: list
        Lista con los valores de cotización en los días indicados a la apertura

    """

    lista_fechas = []
    lista_cot_apertura = []
       
    for i in range(len(info.fechas.dia)):
        dia = info.fechas.dia[i]
        mes = info.fechas.mes[i]
        año = info.fechas.año[i]
        
        fecha = ConvertirFechaEntero(dia, mes, año)
        
        if fecha_ini <= fecha <= fecha_fin:            
            lista_fechas.append(str(info.fechas.dia[i]) + '.' 
                            + str(info.fechas.mes[i]) + '.' 
                            + str(info.fechas.año[i]))
            
            lista_cot_apertura.append(info.apertura[i])


    return lista_fechas, lista_cot_apertura


def GraficaEvolucionCot(fechas_cot: list(), cot_apertura: list()):
    
    """
    La siguiente función dibuja una gráfica que representa la evolución de las 
    cotizaciones entre dos fechas dadas.
    """
    
    # Invertimos las listas para ordenar las fechas correctamente
    # De más antigua a más reciente
    if ConvertirFechaEntero(int(fechas_cot[0].split('.')[0]), 
                            int(fechas_cot[0].split('.')[1]), 
                            int(fechas_cot[0].split('.')[2])) > \
       ConvertirFechaEntero(int(fechas_cot[-1].split('.')[0]), 
                            int(fechas_cot[-1].split('.')[1]), 
                            int(fechas_cot[-1].split('.')[2])):
        fechas_cot = fechas_cot[::-1]
        cot_apertura = cot_apertura[::-1]
        
    # Simplificamos las fechas para la estética del eje X
    fechas_simplificadas = [fecha.split('.')[0] + '.'
                            + fecha.split('.')[1] for fecha in fechas_cot]
    # Gráfica        
    plt.plot(fechas_simplificadas, cot_apertura,
             label = "Evolución de las cotizaciones")
    plt.title("Evolución de las cotizaciones")
    plt.xlabel("Fechas")
    plt.ylabel("Valor de las cotizaciones (en puntos)")
    plt.legend(loc = 'best')
    
    plt.show()
    
    
def EscribirFichero(info: InfoDiaria, fecha_ini: int, fecha_fin: int,
                       ) -> bool:
    """
    La siguiente función guarda en un fichero las fechas y las cotizaciones de
    apertura y de clausura entre dos fechas dadas.

    Parameters
    ----------
    fecha_ini : int
        Fecha inicial.
        
    fecha_fin : int
        Fecha final.
        
    info : InfoDiaria
        Variable tipo InfoDiaria con la información de las cotizaciones.

    Returns
    -------
    bool
        True si se ha podido abrir y guardar la información en el fichero. 
        False si ha ocurrido algun error.

    """
    
    # Nombre del fichero constituido por las fechas inicial y final,
    # separando por '_' el día, mes y año de cada una de ellas.
    nom_fichero = str(fecha_ini)[6:8] + '_' + str(fecha_ini)[4:6] + '_' + \
        str(fecha_ini)[0:4] + '_a_' + str(fecha_fin)[6:8] + '_' + \
        str(fecha_ini)[4:6] + '_' + str(fecha_ini)[0:4]    

    try:
        f = open(nom_fichero + ".dat", "w", encoding = "UTF-8")  
        
    except:
        ok = False
        print("Error en la apertura del fichero")  
        
    else:
        ok = True
        # Cabecera
        f.write("  Fecha \t  Apertura   Clausura \n")
        
        for i in range(len(info.fechas.dia)):
            dia = info.fechas.dia[i]
            mes = info.fechas.mes[i]
            año = info.fechas.año[i]
            
            fecha_actual = ConvertirFechaEntero(dia, mes, año)  
            if fecha_ini <= fecha_actual <= fecha_fin:
                linea = str(dia) + "/" + str(mes) + "/" + str(año) + "\t" + \
                        str(info.apertura[i]) + "\t\t" + \
                        str(info.ultimovalor[i]) + "\n"
                        
                f.write(linea)
            
                
        f.close()
    
    return ok


def MenuOpciones() -> int:
    """
    Función con el menú de opciones para el usuario. Pide elegir una y devuelve
    el número de la opción escogida.

    Returns
    -------
    opcion_elegida: int
        Número de la opción elegida del menú.

    """
    print("-" * 20 + " Menú " + "-" * 20 
          + '\n' 
          
          + "1) Máximo y mínimio de cotización entre dos fechas." 
          + '\n' 
          
          + "2) Variación porcentual de cotización de apertura o clausura " +
              "entre dos fechas. "
          + '\n' 
          
          + "3) Volumen total negociado entre dos fechas, " + 
             "sólo contando aquellos días en los que el volumen sea superior" +
            " a'x' €. " 
          + '\n'
          
          + "4) Representación gráfica de la evolución de la cotización de " +
              "apertura entre dos fechas. "
          + '\n'
          
          + "5) Guardar en un fichero la información de las cotizaciónes " +
              "entre dos fechas concretas. " +
              "Ordenadas desde la fecha más moderna hasta la más antigua. " 
          + '\n'
          
          + "6) Salir. "
          + '\n')
        
    opcion_elegida = int(input("Por favor, elija una opción: "))
        
    return opcion_elegida

          
def main():
    # Empezamos el programa explicando al usuario lo que hace
    print(__doc__)
    
    # Pedimos el nombre del fichero al usuario
    fichero = input("Por favor, introduzca el nombre del fichero: ")
    
    info_diaria = InfoDiaria()  
    ok, info = LeerFichero(fichero, info_diaria)
    
    if ok:
        opcion = MenuOpciones()
        
        # Mostraremos el menú en bucle hasta que el usuario seleccione "Salir".
        while opcion != 6:
            
            if opcion == 1:
                fecha_1 = PedirFecha(info)
                fecha_2 = PedirFecha(info)
      
                cot_max, cot_min = CotMaxMin(fecha_1, fecha_2, info)
                    
                print("El máximo de cotización es ", cot_max, "y el mínimo ", 
                          cot_min)
                
            elif opcion == 2:
                fecha_1 = PedirFecha(info)
                fecha_2 = PedirFecha(info)
                print("Mostrar información de apertura: A" + '\n' 
                      + "Mostrar información de clausura: C" + '\n')
                
                opcion2 = input("Elija una opción: ")
                
                variacion = VariacionPorcentual(opcion2, fecha_1, fecha_2,
                                                info)
                
                print("La variación porcentual entre esas fechas es ",
                      variacion,"%")
            
            elif opcion == 3:
                fecha_1 = PedirFecha(info)
                fecha_2 = PedirFecha(info)
                
                volumen_min = float(input("Volumen mínimo a tener en cuenta \
                                          (en millones): "))
                volumen_total = VolumenTotal(fecha_1, fecha_2,
                                             volumen_min, info)
                print("El volumen total entre las fechas dadas en los que el \
                      volumen es superior a", volumen_min, "M es",
                      volumen_total, "M. ")
                      
            elif opcion == 4:
                fecha_1 = PedirFecha(info)
                fecha_2 = PedirFecha(info)
                fechas_cot, cot_apertura = ObtenerFechasYAperturas(fecha_1,
                                                                   fecha_2,
                                                                   info)
                
                # Gráfica
                GraficaEvolucionCot(fechas_cot, cot_apertura)
                
            elif opcion == 5:
                fecha_1 = PedirFecha(info)
                fecha_2 = PedirFecha(info)
                
                ok = EscribirFichero(info, fecha_1, fecha_2)
                
                if ok:
                    print("La información se ha guardado correctamente en " +
                          "el fichero")
                else:
                    print("No ha sido posible guardar la información en " +
                          "el fichero. ")
                
            else:
                print("Por favor, elija una opción válida. ")
            
            opcion = MenuOpciones()
            
        if opcion == 6:
            print("Cerrando el programa...")

                         
if __name__ == '__main__':
    main()       
