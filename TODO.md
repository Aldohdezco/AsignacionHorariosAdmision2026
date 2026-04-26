Planteamiento del problema
Una coordinación académica debe asignar bloques de tiempo (2 horas por bloque) a un conjunto de clases, evitando traslapes que violen las siguientes restricciones operativas:
A.	Un grupo no puede cursar dos clases en el mismo bloque de tiempo.
B.	Un docente no puede impartir dos clases en el mismo bloque de tiempo.

Objetivo general
Optimizar la asignación de bloques de tiempo para clases académicas mediante el modelado del problema como un grafo de conflictos y la aplicación de algoritmos de coloreo.

Tareas para realizar
1.	Modelar el conjunto de clases como un grafo de conflictos a partir de restricciones por grupo y por docente (como ejemplo considere los datos de la Tabla 1).
2.	Construir la representación gráfica del grafo para su procesamiento.
3.	Aplicar un algoritmo Greedy (paso a paso), dibujando el grafo de conflictos generado considerando el conjunto de datos de la Tabla 1 con el orden: B, A, H, F, I, E, D, C, G.
4.	Aplicar cualquier otro algoritmo de coloreo de grafos para compararlo con el algoritmo Greedy, considere los mismos datos de la Tabla 1 y coloree el grafo resultante.
5.	Argumentar un resultado teórico que le permita determinar: ¿cuándo se obtiene un número mínimo de bloques de tiempo?, o ¿cómo saber que ya no se puede reducir el número de bloques de tiempo.?
6.	Realizar el análisis de la complejidad de los algoritmos de coloreo utilizados.
7.	Proponer una implementación computacional para al menos uno de los algoritmos propuestos para el caso general de resolver conflictos mediante el coloreo grafos. 


Tabla 1.  Regla de conflicto: dos clases están en conflicto si comparten el mismo Grupo o Docente.
Id_Clase	Materia	Grupo	Docente
A	Mate I	G1	T1
B	Mate II	G1	T2
C	Mate III	G1	T3
D	Física I	G2	T1
E	Física II	G2	T2
F	Física III	G2	T3
G	Prog I	G3	T1
H	Prog II	G3	T2
I	Prog III	G3	T3


Preguntas guía
a)	¿Cómo se construye el grafo de conflictos a partir de datos de clases?
b)	¿Cuál es el número mínimo de bloques requerido para un conjunto de clases dado?
c)	¿Qué algoritmo de coloreo produce soluciones de mejor calidad (menos bloques) bajo el mismo tiempo de cómputo?
d)	¿Cómo se valida que el horario resultante no contiene conflictos?
e)	¿En una implementación computacional que estructura de datos es adecuada para representar los datos del grafo de conflictos?
f)	Cómo se quiere obtener un óptimo minimal sobre el número de bloques de tiempo, ¿cómo saber si ya obtuvo tal valor óptimo?
g)	¿Cómo cambia la solución al introducir el conflicto sobre la disponibilidad de los docentes por bloque?
Por ejemplo:
Disponibilidad por docente:
T1: NO disponible en B1 y B4 → permitidos {B2, B3}
T2: NO disponible en B2 y B3 → permitidos {B1, B4}
T3: NO disponible en B1 y B3 → permitidos {B2, B4}
