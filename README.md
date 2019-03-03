# Acceso paralelo a múltiples recursos web almacenados en servidores replicados
Se plantea desarrollar un cliente que recupere múltiples recursos web de varios servidores replicados (N), 
tal que por cada recurso web lea un fragmento del mismo (de tamaño 1/N) de cada uno de los servidores y que, 
además, use pipeline de peticiones para optimizar las peticiones que se envían a cada servidor.

## Autor
[Víctor Nieves Sánchez](https://twitter.com/VictorNS69)

## Enunciado
Podrás encontrar el enunciado en [statement.md](/statement.md)

## Ejemplos de llamadas al programa
Hay publicados tres objetos en dos servidores:

<http://www.datsi.fi.upm.es/~fperez/reto1.txt>

<http://laurel.datsi.fi.upm.es/~fperez/reto1.txt>

<http://www.datsi.fi.upm.es/~fperez/reto2.txt>

<http://laurel.datsi.fi.upm.es/~fperez/reto2.txt>

<http://www.datsi.fi.upm.es/~fperez/reto1.jpg>

<http://laurel.datsi.fi.upm.es/~fperez/reto1.jpg>

Se podría probar:
```
python3 mpwget.py ~fperez/reto1.txt ~fperez/reto2.txt ~fperez/reto1.jpg :http://www.datsi.fi.upm.es :http://laurel.datsi.fi.upm.es
```
## Nota
Puede que estos objetos no estén disponibles en el futuro.