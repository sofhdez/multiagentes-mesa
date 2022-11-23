# Actividad Integradora

Modelar y desplegar de manera gráfica un almacén que contenga 5 robots que recogen cajas.

## Descripción del problema

¡Felicidades! Eres el orgulloso propietario de 5 robots nuevos y un almacén lleno de cajas. El dueño anterior del almacén lo dejó en completo desorden, por lo que depende de tus robots organizar las cajas en algo parecido al orden y convertirlo en un negocio exitoso.

Cada robot está equipado con ruedas omnidireccionales y, por lo tanto, puede conducir en las cuatro direcciones. Pueden recoger cajas en celdas de cuadrícula adyacentes con sus manipuladores, luego llevarlas a otra ubicación e incluso construir pilas de hasta cinco cajas. Todos los robots están equipados con la tecnología de sensores más nueva que les permite recibir datos de sensores de las cuatro celdas adyacentes. Por tanto, es fácil distinguir si un campo está libre, es una pared, contiene una pila de cajas (y cuantas cajas hay en la pila) o está ocupado por otro robot. Los robots también tienen sensores de presión equipados que les indican si llevan una caja en ese momento.

Lamentablemente, tu presupuesto resultó insuficiente para adquirir un software de gestión de agentes múltiples de última generación. Pero eso no debería ser un gran problema ... ¿verdad? Tu tarea es enseñar a sus robots cómo ordenar su almacén. La organización de los agentes depende de ti, siempre que todas las cajas terminen en pilas ordenadas de cinco.

## Parte 1

Realiza la siguiente simulación:

- Inicializa las posiciones iniciales de las K cajas. Todas las cajas están a nivel de piso, es decir, no hay pilas de cajas.
- Todos los agentes empiezan en posición aleatorias vacías.
- Se ejecuta el tiempo máximo establecido.

Deberás recopilar la siguiente información durante la ejecución:

- Tiempo necesario hasta que todas las cajas están en pilas de máximo 5 cajas.
- Número de movimientos realizados por todos los robots.
- Analiza si existe una estrategia que podría disminuir el tiempo dedicado, así como la cantidad de movimientos realizados. ¿Cómo sería? Descríbela.

### Agentes

Para esta actividad se utilizaron 4 agentes diferentes.

#### Box

Este agente no tiene ningún método, sirve para representar las cajas a almacenar.

#### Obstacle

Este agente no cuenta con métodos, sirve para representar los estantes del almacén.

#### BoxStack

Este agente funciona como las pilas de cajas, uno de sus atributos son el número de cajas que se encuentrán en él, si este número es menor a 5 su estado será activo.

#### Robot

Este agente contará con un contador de movimientos y de cajas recogidas, de la misma manera guardará el BoxStack más cercano a su posición.

### Modelo

### Tonto

El modelo básico cuenta con 5 robots que se mueven de manera aleatoria hacia arriba, abajo, izquierda o derecha. Estos agentes no pueden moverse en celdas que estén ocupadas por obstaculos u otros robots.

Después de recoger una gráfica, este se mueve hacia la pila más cercana para 'depositar' la caja y regresar a buscar en el resto del almacén.

[Video de demostración](https://drive.google.com/file/d/1wiSOyhpr2vfoFqKS43xY8yjRBlGlxilq/view?usp=sharing)

### Inteligente

En este modelo cada agenet se dedica a recorrer exclusivamente un area del mapa además de que al hacer su recorrido almacena las posiciones que ya ha visitado, para poder darle prioridad y vistar aquellas que no conoce, esto con el fin de que pueda tomar decisiones más acertadas sobre a donde ir.

**Descripción**

[Video de demostración](https://drive.google.com/file/d/1VcvI71xLhD6RHvlzhsE_8qXu-0iIk2G-/view?usp=sharing)

## Parte 2

El diseño y despliegue debe incluir:

- Modelos con materiales (colores) y texturas (usando mapeo UV):
  - Estante (con repetición de instancias o prefabs por código).
  - Caja (con repetición de instancias o prefabs por código).
  - Robot (con repetición de instancias o prefabs por código, al menos 5 robots).
  - Almacén (piso, paredes y puerta).
- Animación
  - Los robots deberán desplazarse sobre el piso del almacén, en los pasillos que forman los estantes.
  - Para esta actividad, no es necesario conectar la simulación con el despliegue.
- Iluminación
  - Al menos una fuente de luz direccional.
  - Al menos una fuente de luz puntual sobre cada robot (tipo sirena). Dicha luz se moverá con cada robot.
- Detección de colisiones básica
  - Los robots se moverán en rutas predeterminadas.
  - Los robots se moverán con velocidad predeterminada (aleatoria).
  - Los robots comenzarán a operar en posiciones predeterminadas (aleatorias).
  - Los robots detectarán y reaccionarán a colisiones entre ellos. Determina e implementa un sistema básico para esto (por ejemplo, detenerse previo a una colisión y asignar el paso a uno de los robots).

### Almacén

Para el lugar en el que se estaran implementando los robots se diseño un alamacen en el cual, se personalizaron la estetica de este mismo, tanto el piso del almacen al igual que las paredes del mismo.
Dentro del mismo almacen se diseñaron estantes personalizados, al igual que los materiales y texturas del mismo.

### Modelos de caja

Para el mismo alamcen se diseñaron un modelo de caja que estarian en las estanterias del los mismos estantes, dando un diseño mucho más realista del alamacen.

### Modelos de Robots

Se diseñaron 5 modelos de robots personalizados que tienen la funcionalidad de servir como agente que recogera las cajas.
Cada robot cuenta con diferentes tipo de iluminación, material y texturas diseñadas para darle personalidad a cada robot.
Los robots dentro de Unity son GameObjects con componentes que le permiten tener una interación con el ambiente.

### Movimiento

Cada robot al igual que todo el alamcen cuenta con un boxcolider, para poder detectar coliciónes entre los mismos. A cada modelo del robot se le implemento un componte de script para el funcionamiento de sus movimientos y en diferentes angulos de movimiento. El script cuenta con una funcionalidad de empezar con un movimiento aleatorio en una dirección, al detectar o colisionar un box colider ya sea de una pared, estante o algun otro robot, eligira e manera aleaotoria una nueva trayecgtoria.

### Velocidad 

Cada robot tiene una unidad de velocidad personalizada, la cual se le puede modificar manualmente para cada robot.

### Inteligencia

Para evitar conflictos de eficiencia al recorrer el alamcen, cada robot cuenta con un sistema de prioridad el cual funciona de manera que, al colicionar con algun otro robot, el robot con mayor velocidad de movimiento seguira con su dirección de movimiento, por otra parte, aquel robot con menor velocidad de movimiento tendra que ceder el paso y cambiar de dirección.

### Posiciónes

Para la implementación del posicionamiento de cada de los robots se creo un robot manager que permite distribuir a los robot en el almacén de manera aleatoria en todo el almacén.

## Autores

- Abiel Moisés Borja García A01654937
- Gael Eduardo Pérez Gómez A01753336
- Marco Uriel Pérez Gutiérrez A01660337
- Sofía Margarita Hernández Muñoz A01655084
