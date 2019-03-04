# Enunciado

El servicio web está concebido como una arquitectura cliente-servidor tal que un único servidor se encarga de proporcionar acceso a una determinado recurso web. No hay ningún tipo de soporte para la replicación, que, en caso de que sí lo hubiera, permitiría una mayor escalabilidad, repartiendo la carga de peticiones, y una mejor disponibilidad.

En cualquier caso, aunque sea de una forma manual, en la web se puede, hasta cierto punto, replicar un recurso haciendo que distintas URLs hagan referencia al mismo recurso (mirrors donde un usuario puede acceder a un recurso, eligiendo frecuentemente el más cercano geográficamente, y seleccionando otra URL si la anteriormente probada ha fallado) o incluso la misma URL, en el caso de que asociado a un mismo nombre DNS haya varias máquinas.

En ocasiones, el uso de varios servidores en una arquitectura cliente-servidor puede deberse a la necesidad de acceder en paralelo a distintos fragmentos de un recurso, distribuido entre dichos servidores, para intentar de esta forma acceder más eficientemente al mismo (como ocurre con los sistemas de ficheros paralelos, que estudiaremos en la asignatura).

Sobre esa idea se plantea este ejercicio. Se va a suponer que trabajamos con recursos web, de un tamaño considerable para que tenga sentido el acceso paralelo, que están replicados en varios servidores (N) y se va a desarrollar un cliente que pida a cada servidor una parte de cada recurso requerido creando localmente un fichero por cada uno de los recursos. Para llevar a cabo este acceso paralelo, el cliente usará la opción de rangos presente en el protocolo HTTP, que permite solicitar el contenido parcial de un recurso web.

Por otro lado, tal como se explica en la parte teórica de la asignatura, gracias al uso de conexiones persistentes y al pipeline de peticiones, la versión 1.1 del protocolo HTTP permite mejorar el rendimiento a la hora de solicitar múltiples objetos de un mismo servidor al reducir la sobrecarga de conexiones y disminuir las latencias acumuladas.

En este ejercicio práctico vamos a mezclar ambas ideas: uso de rangos y pipeline de peticiones. Se plantea desarrollar un cliente que recupere múltiples recursos web de varios servidores replicados (N), tal que por cada recurso web lea un fragmento del mismo (de tamaño 1/N) de cada uno de los servidores y que, además, use pipeline de peticiones para optimizar las peticiones que se envían a cada servidor.

Para intentar aclarar el comportamiento esperado, suponga que hay 4 objetos (desde O1 de tamaño T1 hasta O4 de tamaño T4) y 3 servidores replicados (S1, S2 y S3). El cliente enviaría al servidor S1 cuatro peticiones GET en un pipeline solicitando los primeros T1/3 bytes de O1, los T2/3 primeros de O2, los T3/3 primeros de O3 y los T4/3 primeros de O4. De la misma forma y sin esperar, obviamente, la respuesta de S1, al servidor S2 le solicitaría en pipeline la tercera parte central de cada objeto y al S3 la parte final de los mismos. Nótese que, antes de realizar las peticiones GET, el programa debe averiguar el tamaño del recurso, lo que puede hacer enviando el mandato HEAD al primer servidor.

El programa a desarrollar recibirá como argumentos los nombres de los objetos a solicitar y la lista de los servidores replicados (sus nombres DNS, con un carácter : delante para diferenciarlos):
```bash
mpwget objeto1 objeto2 objeto3 :servidor1 :servidor2...
```
En cuanto al nombre de los objetos/recursos, corresponderá a la parte final de la URL. Por ejemplo, en `http://www.datsi.fi.upm.es/informacion.html` sería _informacion.html_, mientras que para `http://www.datsi.fi.upm.es/~coes/index.html` sería _~coes/index.html_.

El programa traerá los objetos correspondientes almacenándolos localmente en ficheros con el mismo nombre (si el objeto incluye un directorio y/o el nombre de un usuario, puede optar por distintas soluciones: se podría crear un fichero local que se corresponda con el basename del objeto o bien crear una estructura de directorios que refleje el nombre del recurso).
