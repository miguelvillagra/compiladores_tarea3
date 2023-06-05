# compiladores_tarea3

Repositorio para tarea3 de la materia compiladores.
Integrante: Miguel Villagra.
contacto: miguel.villagra@fpuna.edu.py

Version de python: Python 3.10.11

Se requiere de la libreria ply, instalarlo con el siguiente comando.
```
pip install ply
```

Este script implementa el analizador sintáctico descendente recursivo de la tarea2 utilizando la biblioteca ply. 
Se han hecho modificaciones para que sea posible la traduccion a XML.

Define las reglas de la gramática JSON simplificada y utiliza la estrategia de manejo de errores Panic Mode 
para sincronizar y continuar el análisis en caso de encontrar errores.

El JSON a probar se encuenta en el archivo: 'fuente.json'

Luego de instalar las librerias necesarias, ejecutar el programa con el siguiente comando:
```
python main.py
```

EJEMPLO:


![Captura de pantalla (159)](https://github.com/miguelvillagra/compiladores_tarea3/assets/88117555/04023c50-55ed-44d1-a6b5-8892b23cb873)
