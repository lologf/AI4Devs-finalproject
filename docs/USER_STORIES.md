# Historias de usuario — Tandem MVP

> **Fuente**: [PRD](./PRD.md) · **Modelo de datos**: [README §3](../readme.md#3-modelo-de-datos)
> **Formato**: *Como [perfil] quiero [intención] para [beneficio]*, con criterios de aceptación en Gherkin (de 1 a 5 escenarios por historia, según su complejidad).
> **Criterios de aceptación**: describen **comportamiento observable** por el usuario. Los detalles de implementación (eventos, tablas, estados internos, códigos HTTP) están en el [README](../readme.md) (modelo de datos, API y tickets) y en el catálogo de eventos del [PRD](./PRD.md#8-catálogo-de-eventos-contrato-entre-dominios).
> **Convención**: los supuestos iniciales (`[ASUMIDO]`) se revisaron y validaron y ya están incorporados como criterios.
> **Perfiles**: *miembro* (cualquiera de los dos usuarios), *miembro responsable* (el asignado a un elemento), *el otro miembro*, *operador* (quien instala y mantiene el sistema; en la práctica, uno de los miembros).
> **Estimación**: story points (Fibonacci), a modo orientativo para planificar las entregas.

## Épicas

| Épica | Objetivo | Criterio de cierre | Historias | Prioridad | Entrega |
|---|---|---|---|---|---|
| **E1 · Acceso e identidad** | Solo los dos miembros acceden, de forma segura, y cada acción queda atribuida a quien la hizo | Ambos miembros entran y salen, gestionan sus sesiones, su contraseña y su perfil y configuran sus avisos; toda ruta de la API salvo el login, los enlaces de acción y los endpoints de salud rechaza las peticiones sin sesión (comprobado por un test) | US-01 … US-04, US-39, US-46 | Must (US-39, US-46: Should) | 2 |
| **E2 · Tareas** | Que las tareas del hogar, puntuales o recurrentes, estén apuntadas y se regeneren solas | Se crean, editan, archivan, borran y resuelven tareas; las recurrentes generan su siguiente ocurrencia, las atrasadas se distinguen y "Hoy" y "Esta semana" reúnen tareas, citas y vencimientos | US-05 … US-10, US-40 | Must (US-09: Should) | 2 |
| **E3 · Asignación y reparto** | Que siempre esté claro a quién le toca y que el reparto sea visible | Cada ocurrencia tiene responsable según su regla, las ausencias reasignan (y se deshacen al cancelarlas) y el balance refleja quién hace y quién planifica | US-11 … US-14, US-42 | Must (US-42: Should) | 2 |
| **E4 · Citas y vencimientos** | Que ningún vencimiento ni cita se pase | Se gestionan vencimientos y citas con antelaciones, adjuntos y renovación anual; los vencimientos atrasados se recuerdan cada día y las citas pasadas se cierran solas | US-15 … US-18, US-36, US-37, US-41 | Must (US-18, US-36, US-37: Should) | 2 (adjuntos en 3) |
| **E5 · Motor temporal y avisos** | Que el sistema avise a los dos, a tiempo y sin ser molesto, y que se pueda actuar desde el aviso | Los avisos se entregan al servidor de correo en ≤ 2 min (p95) desde su momento previsto, también tras una caída y sin duplicados; respetan silencio y agrupación, y se pueden posponer y resolver desde el correo | US-19 … US-25 | Must (US-25: Should) | 2 |
| **E6 · Gastos** | Llevar las cuentas compartidas sin otra app | Se registran, corrigen y borran gastos (también recurrentes) con su reparto, se ve el saldo y se liquida | US-26 … US-30, US-38, US-43, US-44 | Should (US-30, US-38: Could) | 3 |
| **E7 · Compra** | Una lista compartida que, al cerrar la compra, se convierte en gasto | Ambos gestionan la lista por secciones, la marcan en la tienda y al cerrarla se registra el gasto | US-31 … US-33, US-38 | Could | 3 |
| **E8 · Listas de interés** | Guardar en común lo que queremos hacer juntos | Se crean y mantienen listas temáticas y sus elementos, que se marcan como hechos y se valoran | US-34, US-35, US-45 | Could | 3 |
| **E9 · Operación** | Saber que el sistema funciona y si cumple sus objetivos | El operador recibe una alerta si el motor temporal se para y puede calcular las métricas de éxito del PRD | US-47, US-48 | Must (US-48: Should) | 2 (US-48 en 3) |

US-38 (categorías) es compartida por E6 y E7. El test de rutas sin sesión de E1 forma parte de TCK-04. **Historias principales** (marcadas con ⭐): **US-06**, **US-16** y **US-24**. Este documento es su única fuente: el script `scripts/build_readme.py` las copia al [README §5](../readme.md#5-historias-de-usuario), así que se editan solo aquí.

---

## E1 · Acceso e identidad

### US-01 · Alta de miembros por CLI
**Como** operador **quiero** crear los dos miembros del hogar desde la línea de comandos **para** tener el sistema listo sin exponer un registro público.
`Must · 2 pts · RF-1.4, RNF-SEC-1 (NIST SP 800-63B-4)`

```gherkin
Escenario: Alta del primer miembro
  Dado que no existe ningún miembro
  Cuando ejecuto "tandem create-user --email lucia@example.com --name Lucía"
  Y introduzco la contraseña "tortilla con cebolla los domingos"
  Entonces se crea el miembro "Lucía"
  Y puede iniciar sesión con ese email y esa contraseña, aunque no tenga mayúsculas, números ni símbolos

Esquema del escenario: Contraseña que no cumple la política
  Dado que estoy dando de alta a Lucía (lucia@example.com)
  Cuando introduzco la contraseña "<contraseña>"
  Entonces el comando falla indicando que <motivo>
  Y no se crea el miembro

  Ejemplos:
    | contraseña          | motivo                                                 |
    | cebolla patata      | debe tener al menos 15 caracteres                      |
    | 123456789012345     | es demasiado común o ha aparecido en filtraciones      |
    | mi tandem de casa 1 | no puede contener el nombre del servicio               |
    | lucia es la mejor 2 | no puede contener tu nombre ni tu email                |

Escenario: No se admite un tercer miembro
  Dado que ya existen dos miembros
  Cuando intento crear otro
  Entonces el comando falla con "El hogar ya tiene dos miembros"
  Y no se crea ningún miembro

Escenario: Email duplicado
  Dado que existe un miembro con "lucia@example.com"
  Cuando intento crear otro con "LUCIA@example.com"
  Entonces el comando falla indicando que el email ya existe (sin distinguir mayúsculas)
```

### US-02 · Iniciar sesión
**Como** miembro **quiero** iniciar sesión con mi email y contraseña **para** acceder a la información del hogar de forma segura.
`Must · 3 pts · RF-1.1, RNF-SEC-2/3/4`

```gherkin
Escenario: Login correcto
  Dado que soy uno de los dos miembros del hogar
  Cuando introduzco mi email y mi contraseña correctos
  Entonces accedo a la vista "Hoy"
  Y sigo con la sesión iniciada mientras la use al menos una vez cada 30 días

Escenario: Credenciales incorrectas
  Dado que estoy en la pantalla de login
  Cuando introduzco un email o una contraseña incorrectos
  Entonces veo "Email o contraseña incorrectos" sin indicar cuál de los dos falla

Escenario: Bloqueo por intentos
  Dado que ha habido 5 intentos fallidos para mi email en los últimos 15 minutos
  Cuando intento iniciar sesión, aunque sea con la contraseña correcta
  Entonces no se me deja entrar
  Y veo cuánto tiempo debo esperar

Escenario: Acceso sin sesión
  Dado que no he iniciado sesión o mi sesión ha caducado
  Cuando intento abrir cualquier pantalla de Tandem
  Entonces se me lleva al login
```

### US-03 · Cerrar sesión y gestionar mis sesiones
**Como** miembro **quiero** ver dónde tengo la sesión abierta y cerrarla en este dispositivo, en otro concreto o en todos **para** proteger el acceso si pierdo o comparto un dispositivo.
`Must · 2 pts · RF-1.1, RNF-SEC-2`

```gherkin
Antecedentes:
  Dado que tengo la sesión iniciada en el móvil y en el portátil

Escenario: Cerrar sesión en el dispositivo actual
  Cuando pulso "Cerrar sesión" en el móvil
  Entonces el móvil vuelve al login
  Y esa sesión deja de dar acceso aunque alguien la hubiera copiado

Escenario: Ver mis sesiones activas
  Cuando abro "Sesiones" en mi perfil
  Entonces veo ambas con su navegador, su IP y su última actividad
  Y se indica cuál es la actual

Escenario: Cerrar una sesión concreta
  Cuando cierro desde el móvil la sesión del portátil
  Entonces el portátil pierde el acceso
  Y el móvil sigue con la sesión iniciada

Escenario: Cerrar todas las sesiones
  Cuando pulso "Cerrar todas las sesiones"
  Entonces se cierran todas, incluida la actual
```

### US-04 · Preferencias de aviso
**Como** miembro **quiero** configurar mi ventana de silencio y si recibo el digest y a qué hora **para** recibir los avisos cuando me son útiles.
`Must · 2 pts · RF-1.3, RF-8.2, RF-8.3`

```gherkin
Escenario: Valores por defecto
  Dado que soy un miembro recién creado
  Cuando abro mi perfil
  Entonces veo el silencio de 22:00 a 08:00 y el digest activado a las 08:00
  Y la combinación es válida, porque el silencio termina justo a las 08:00

Escenario: Cambiar la ventana de silencio
  Dado que tengo el silencio de 22:00 a 08:00
  Cuando lo cambio a 23:00–07:30 y guardo
  Entonces un aviso que se genere para mí a las 23:15 me llega a las 07:30

Escenario: El digest no puede caer en la ventana de silencio
  Dado que tengo el silencio de 23:00 a 07:30
  Cuando pongo el digest a las 06:00
  Entonces veo un error de validación y no se guarda

Escenario: Desactivar el digest
  Dado que tengo el digest activado
  Cuando lo desactivo y guardo
  Entonces dejo de recibir el correo resumen diario
  Y sigo recibiendo los avisos inmediatos
```

### US-39 · Cambiar mi contraseña
**Como** miembro **quiero** cambiar mi contraseña desde mi perfil, o que el operador me la restablezca si la olvido, **para** mantener mi cuenta segura sin depender de un email de recuperación.
`Should · 2 pts · RF-1.4, RNF-SEC-1, RNF-SEC-2`

```gherkin
Escenario: Cambio desde el perfil
  Dado que he iniciado sesión
  Cuando introduzco mi contraseña actual y una nueva que cumple la política
  Entonces la contraseña cambia
  Y se cierran mis sesiones en otros dispositivos, pero no la actual

Escenario: Contraseña actual incorrecta
  Dado que he iniciado sesión
  Cuando introduzco una contraseña actual incorrecta
  Entonces veo un error y la contraseña no cambia

Escenario: Nueva contraseña no válida
  Dado que he iniciado sesión
  Cuando la nueva contraseña no cumple la política de US-01 (15 caracteres como mínimo, no común ni filtrada, sin el nombre del servicio, mi nombre ni mi email)
  Entonces veo qué regla incumple y la contraseña no cambia

Escenario: Restablecimiento por CLI
  Dado que Álex ha olvidado su contraseña
  Cuando el operador ejecuta "tandem set-password --email alex@example.com" con una contraseña válida
  Entonces Álex puede entrar con la nueva contraseña
  Y todas sus sesiones anteriores se cierran
```

### US-46 · Cambiar mi nombre visible y mi email de avisos
**Como** miembro **quiero** cambiar mi nombre visible y el email donde recibo los avisos, confirmando el nuevo email **para** que una errata no me deje sin avisos sin darme cuenta.
`Should · 2 pts · RF-1.3, RF-8.7`

```gherkin
Escenario: Cambiar el nombre visible
  Dado que mi nombre visible es "Lucía"
  Cuando lo cambio a "Lu"
  Entonces los avisos y la web muestran "Lu"

Escenario: El nuevo email se confirma antes de usarse
  Dado que recibo los avisos en lucia@example.com
  Cuando cambio mi email de avisos a lucia@nuevo.example
  Entonces se envía a lucia@nuevo.example un correo con un enlace para confirmarlo
  Y hasta que lo confirme, los avisos siguen llegando a lucia@example.com

Escenario: Confirmar el nuevo email
  Dado el correo de confirmación enviado a lucia@nuevo.example
  Cuando abro su enlace y confirmo
  Entonces los avisos pasan a llegar a lucia@nuevo.example

Escenario: Confirmación caducada
  Dado un correo de confirmación recibido hace más de 48 horas
  Cuando abro su enlace
  Entonces veo que ya no es válido
  Y los avisos siguen llegando a lucia@example.com hasta que pida otro cambio

Escenario: Un enlace anterior no confirma otra dirección
  Dado que pedí cambiar a lucia@a.example y después a lucia@b.example
  Cuando abro el enlace enviado a lucia@a.example
  Entonces veo que ya no es válido
  Y solo el enlace enviado a lucia@b.example puede confirmar el cambio
```

---

## E2 · Tareas

### US-05 · Crear una tarea puntual
**Como** miembro **quiero** crear una tarea con fecha y hora **para** que el sistema la recuerde en lugar de mí.
`Must · 2 pts · RF-2.1, RF-1.2, RF-8.2`

```gherkin
Escenario: Crear tarea puntual
  Dado que he iniciado sesión como Lucía
  Cuando creo "Llamar al fontanero" para el 03/10 a las 18:00 asignada a Álex
  Entonces aparece como pendiente para esa fecha, con Álex como responsable
  Y consta que la creé yo
  Y Álex recibe un aviso de que le he asignado una tarea

Escenario: Título, fecha y hora obligatorios
  Dado que estoy creando una tarea
  Cuando intento guardarla sin título, sin fecha o sin hora
  Entonces veo un error de validación y no se crea

Escenario: Hora ya pasada de hoy
  Dado que son las 12:00 del 03/10
  Cuando creo una tarea para el 03/10 a las 09:00
  Entonces aparece como pendiente de hoy, no como atrasada
  Y no se envía el aviso "Hoy te toca", porque su hora ya ha pasado

Escenario: Día ya terminado
  Dado que son las 12:00 del 03/10
  Cuando creo una tarea para el 02/10 a las 18:00
  Entonces se crea directamente como atrasada y aparece arriba en "Hoy"
```

### US-06 · Crear una tarea recurrente ⭐
**Como** miembro **quiero** crear tareas que se repiten por calendario o cada N días tras hacerlas **para** no tener que volver a apuntar las tareas domésticas habituales.
`Must · 5 pts · RF-2.2, RF-2.3`

```gherkin
Escenario: Recurrencia por calendario
  Dado que hoy es miércoles 30/09
  Cuando creo "Sacar la basura" para los lunes y jueves a las 21:00
  Entonces su primera ocurrencia es el jueves 01/10 a las 21:00 (hora de Madrid)
  Y al completarla, la siguiente es el lunes 05/10 a las 21:00

Escenario: Recurrencia tras completar
  Dado "Cambiar sábanas" a las 10:00, cada 14 días tras completarla
  Y que su ocurrencia actual vence el 01/10
  Cuando se completa el 03/10 a las 23:47
  Entonces la siguiente ocurrencia vence el 17/10 a las 10:00

Escenario: Solo una ocurrencia abierta
  Dado "Sacar la basura" con la ocurrencia del jueves 01/10 sin hacer
  Cuando llega el lunes 05/10
  Entonces en "Hoy" solo aparece la del jueves, como atrasada
  Y la del lunes 05/10 no se genera ni cuenta como omitida
  Y cuando se resuelve el martes 06/10, la siguiente es el jueves 08/10

Escenario: Cambio de hora de octubre
  Dada una tarea diaria a las 09:00
  Cuando cambia la hora el último domingo de octubre
  Entonces la ocurrencia de ese día sigue siendo a las 09:00 hora local
```

### US-07 · Ver lo que toca hoy y esta semana
**Como** miembro **quiero** ver en una pantalla las tareas, citas y vencimientos de ambos para hoy y para esta semana **para** saber qué hay que hacer y quién lo hace sin mirar en varios sitios.
`Must · 3 pts · RF-2.6`

```gherkin
Escenario: Vista Hoy
  Dadas ocurrencias pendientes para hoy de Lucía y de Álex, otra atrasada y la cita "Dentista Álex" a las 17:00
  Cuando abro "Hoy"
  Entonces veo primero la atrasada y después lo de hoy, ordenado por hora, incluida la cita
  Y cada elemento muestra su responsable

Escenario: Vista Esta semana
  Dado tareas, citas y vencimientos repartidos entre hoy y el domingo
  Cuando abro "Esta semana"
  Entonces los veo agrupados por día

Escenario: Filtrar por mí
  Dados elementos de Lucía, de Álex y de "cualquiera"
  Cuando Lucía activa "Solo las mías"
  Entonces solo ve los suyos y los de "cualquiera"

Escenario: Estado vacío
  Dado que no hay nada pendiente hoy
  Cuando abro "Hoy"
  Entonces veo "Nada pendiente hoy" y un acceso para crear una tarea
```

### US-08 · Completar u omitir una ocurrencia
**Como** miembro **quiero** marcar una ocurrencia como hecha u omitida **para** que el sistema sepa que está resuelta y deje de avisar.
`Must · 2 pts · RF-2.4`

```gherkin
Escenario: Completar la tarea de otro
  Dada una ocurrencia asignada a Álex
  Cuando Lucía la marca como hecha
  Entonces queda hecha y consta que la hizo Lucía
  Y ninguno de los dos recibe ya avisos de esa ocurrencia

Escenario: Omitir
  Dada una ocurrencia pendiente
  Cuando la marco como omitida
  Entonces deja de estar pendiente
  Y no cuenta en el balance de nadie

Escenario: Ya resuelta
  Dada una ocurrencia que Álex ya completó
  Cuando Lucía intenta completarla desde una pantalla sin actualizar
  Entonces ve "Ya estaba hecha por Álex" y no cambia nada
```

### US-09 · Historial de una tarea
**Como** miembro **quiero** ver el historial de ocurrencias de una tarea **para** saber cuándo se hizo por última vez y quién la hizo.
`Should · 2 pts · RF-2.5`

```gherkin
Escenario: Ver historial
  Dado "Limpiar el baño" con 6 ocurrencias pasadas
  Cuando abro su detalle
  Entonces veo cada ocurrencia con fecha prevista, estado, responsable y quién la resolvió, de la más reciente a la más antigua

Escenario: Última vez
  Dado que la última vez la hizo Álex hace 5 días
  Cuando abro el detalle de "Limpiar el baño"
  Entonces se destaca "Última vez: hace 5 días, por Álex"
```

### US-10 · Editar, archivar o borrar una tarea
**Como** miembro **quiero** editar, archivar o borrar una tarea **para** adaptarla cuando cambian nuestras rutinas sin perder el historial de lo que ya se hizo.
`Must · 3 pts · RF-2.1`

```gherkin
Escenario: Editar la recurrencia
  Dada una tarea semanal con una ocurrencia pendiente para el jueves
  Cuando la cambio a los viernes
  Entonces la ocurrencia pendiente se mueve al próximo viernes
  Y el historial no cambia

Escenario: Archivar
  Dada una tarea con una ocurrencia pendiente
  Cuando la archivo
  Entonces su ocurrencia pendiente se cancela y no se generan más
  Y desaparece de "Hoy" pero sigue en el historial

Escenario: Borrar una tarea sin historial
  Dado "Montar la estantería", creada por error y sin ninguna ocurrencia hecha ni omitida
  Cuando la borro y confirmo
  Entonces desaparece por completo

Escenario: Una tarea con historial no se borra
  Dado "Limpiar el baño" con ocurrencias ya hechas u omitidas
  Cuando intento borrarla
  Entonces se me ofrece archivarla en su lugar, para no perder el historial ni el balance
```

### US-40 · Tareas atrasadas
**Como** miembro **quiero** que una tarea que no se hizo en su día quede marcada como atrasada **para** verla destacada hasta que alguien la haga u omita.
`Must · 2 pts · RF-2.3, RF-8.2`

```gherkin
Escenario: Sigue pendiente durante su día
  Dado "Poner lavadora" para hoy a las 19:00, sin hacer
  Cuando son las 21:00
  Entonces sigue apareciendo como pendiente de hoy

Escenario: Pasa a atrasada al terminar el día
  Dado "Poner lavadora" para ayer a las 19:00, sin hacer
  Cuando abro "Hoy"
  Entonces aparece como atrasada, arriba del todo

Escenario: En el digest
  Dada una tarea atrasada
  Y un miembro con el digest activo
  Cuando llega su hora de digest
  Entonces la tarea aparece en el apartado de atrasadas, cada día hasta que se resuelva

Escenario: Sin avisos repetidos
  Dada una tarea atrasada
  Cuando pasan los días sin resolverla
  Entonces no se envían avisos inmediatos adicionales por estar atrasada
```

---

## E3 · Asignación y reparto

### US-11 · Definir cómo se asigna una tarea
**Como** miembro **quiero** elegir si una tarea es siempre de uno, se alterna o es de cualquiera, y cambiarlo después, **para** que el reparto quede acordado y no dependa de la memoria.
`Must · 3 pts · RF-3.1, RF-8.2`

```gherkin
Escenario: Alternar
  Dado "Sacar la basura" en modo "alternar" empezando por Álex
  Cuando se generan tres ocurrencias consecutivas
  Entonces se asignan a Álex, Lucía y Álex

Escenario: Fija
  Dada una tarea en modo "fija" para Lucía
  Cuando se generan sus ocurrencias
  Entonces todas se asignan a Lucía

Escenario: Cualquiera
  Dada una tarea en modo "cualquiera"
  Cuando se generan sus ocurrencias
  Entonces no tienen responsable
  Y los avisos se envían a ambos sin destacar a nadie

Escenario: Cambiar el modo de una tarea existente
  Dado "Sacar la basura" en modo "alternar", con la ocurrencia pendiente asignada a Álex
  Cuando Álex la cambia a "fija" para Lucía
  Entonces la ocurrencia pendiente y las siguientes son de Lucía
  Y el historial no cambia
  Y Lucía recibe un aviso
```

### US-12 · Registrar una ausencia
**Como** miembro **quiero** registrar que estaré fuera unos días **para** que mis tareas pasen automáticamente al otro miembro.
`Must · 3 pts · RF-3.2, RF-8.2`

```gherkin
Escenario: Reasignación por ausencia
  Dado que Álex tiene una ausencia del 10/10 al 12/10
  Y que una ocurrencia alternada le toca el 11/10
  Cuando se genera esa ocurrencia
  Entonces se asigna a Lucía
  Y la siguiente ocurrencia alternada también es de Lucía, porque la rotación sigue como si la del 11/10 hubiera sido de Álex

Escenario: Ausencia sobre ocurrencias ya asignadas
  Dado que Álex tiene asignada una ocurrencia pendiente el 11/10
  Cuando registra una ausencia del 10/10 al 12/10
  Entonces esa ocurrencia se reasigna a Lucía
  Y Lucía recibe un aviso

Escenario: Ausencias solapadas
  Dado que Álex tiene una ausencia del 10/10 al 12/10
  Cuando registra otra del 12/10 al 15/10
  Entonces veo un error de solapamiento

Escenario: Ambos ausentes
  Dado que los dos están ausentes el 11/10
  Cuando se genera una ocurrencia ese día
  Entonces se asigna según la regla normal
  Y el aviso indica que ambos están ausentes
```

### US-13 · Quedarme o ceder una ocurrencia
**Como** miembro **quiero** asumir o ceder una ocurrencia concreta **para** ajustar el reparto puntualmente sin romper la rotación.
`Must · 2 pts · RF-3.3, RF-8.2`

```gherkin
Escenario: Me lo quedo
  Dada una ocurrencia asignada a Álex
  Cuando Lucía pulsa "Me lo quedo"
  Entonces pasa a Lucía
  Y la siguiente ocurrencia de la rotación sigue siendo de quien le tocaba
  Y Álex recibe un aviso

Escenario: Me lo quedo en una tarea de cualquiera
  Dada una ocurrencia de "cualquiera", sin responsable
  Cuando Lucía pulsa "Me lo quedo"
  Entonces Lucía pasa a ser su responsable
  Y Álex recibe un aviso

Escenario: Ceder
  Dada una ocurrencia asignada a mí
  Cuando la cedo
  Entonces se asigna al otro miembro y se le avisa

Escenario: Los dos a la vez
  Dada una ocurrencia de "cualquiera"
  Cuando Lucía y Álex pulsan "Me lo quedo" casi a la vez
  Entonces se queda la ocurrencia quien lo pulsó primero
  Y el otro ve "Ya la ha asumido Lucía" (o Álex) sin que cambie nada
```

### US-14 · Ver el balance de tareas
**Como** miembro **quiero** ver cuántas tareas ha completado y cuántas tareas, vencimientos y citas ha creado cada uno **para** tener una visión objetiva del reparto de la carga, también la de planificar.
`Must · 2 pts · RF-3.4`

```gherkin
Escenario: Balance mensual
  Dado que en septiembre Lucía completó 18 ocurrencias y Álex 12
  Cuando abro "Balance" en el periodo "Este mes"
  Entonces veo Lucía 18 (60 %) y Álex 12 (40 %)

Escenario: Las omitidas no cuentan
  Dado que en septiembre hubo ocurrencias omitidas
  Cuando abro el balance de septiembre
  Entonces no suman para ninguno

Escenario: Cuenta quien la hace
  Dada una ocurrencia asignada a Álex que completó Lucía
  Cuando abro el balance
  Entonces suma para Lucía

Escenario: Quién planifica
  Dado que en septiembre Lucía creó 9 tareas, vencimientos y citas, Álex 3 y se renovó automáticamente el seguro del hogar
  Cuando abro el balance de septiembre
  Entonces veo también "Planificado: Lucía 9 (75 %), Álex 3 (25 %)"
  Y la renovación automática no cuenta para nadie
```

### US-42 · Modificar o cancelar una ausencia
**Como** miembro **quiero** acortar, ampliar o cancelar una ausencia **para** que el reparto se ajuste si mis planes cambian.
`Should · 2 pts · RF-3.2, RF-8.2`

```gherkin
Escenario: Acortar una ausencia
  Dado que Álex tiene una ausencia del 10/10 al 15/10 y sus ocurrencias de esos días pasaron a Lucía
  Cuando la acorta hasta el 12/10
  Entonces las ocurrencias pendientes del 13/10 al 15/10 vuelven a quien le tocaban según su regla
  Y Lucía recibe un aviso con los cambios

Escenario: Cancelar una ausencia
  Dado que Álex tiene una ausencia futura
  Cuando la cancela
  Entonces todas las ocurrencias pendientes que se reasignaron por ella vuelven a quien le tocaban
  Y Lucía recibe un aviso con los cambios

Escenario: Ampliar una ausencia
  Dado que Álex tiene una ausencia del 10/10 al 12/10
  Cuando la amplía hasta el 14/10
  Entonces sus ocurrencias pendientes del 13/10 y 14/10 pasan a Lucía, como en US-12
  Y Lucía recibe un aviso con los cambios

Escenario: Las reasignaciones manuales se respetan
  Dada una ocurrencia que Lucía se quedó con "Me lo quedo" durante la ausencia
  Cuando Álex cancela la ausencia
  Entonces esa ocurrencia sigue siendo de Lucía

Escenario: Ausencia ya terminada
  Dada una ausencia cuyo último día ya pasó
  Cuando intento modificarla o cancelarla
  Entonces no se permite: queda en el historial
```

---

## E4 · Citas y vencimientos

### US-15 · Crear un vencimiento o una cita
**Como** miembro **quiero** registrar vencimientos (ITV, seguros) y citas (médico) con fecha y responsable **para** tenerlos en un único sitio compartido.
`Must · 3 pts · RF-4.1, RF-4.2`

```gherkin
Escenario: Vencimiento de día completo con antelaciones por defecto
  Dado que estoy creando el vencimiento "Seguro del coche" para el 20/11, sin hora
  Cuando lo guardo sin indicar antelaciones
  Entonces se nos recordará a los dos 7 días y 1 día antes, a la hora de digest de cada uno
  Y si el 20/11 termina sin resolverlo, pasa a atrasado

Escenario: Cita con antelaciones por defecto
  Dado que estoy creando la cita "Dentista Álex" para el 05/10 a las 17:00
  Cuando la guardo sin indicar antelaciones
  Entonces se nos recordará a los dos 1 día y 2 horas antes

Escenario: Una cita necesita hora
  Dado que estoy creando una cita
  Cuando intento guardarla sin hora
  Entonces veo un error de validación

Escenario: Antelaciones personalizadas
  Dado que estoy creando el vencimiento "Renovar DNI"
  Cuando indico antelaciones de 30, 7 y 1 días
  Entonces se guardan las tres
  Y si repito una antelación, veo un error

Escenario: Responsable avisado
  Dado que soy Lucía
  Cuando creo "ITV coche" con Álex como responsable
  Entonces Álex recibe un aviso de que es el responsable
```

### US-16 · Recibir recordatorios de vencimientos y citas ⭐
**Como** miembro **quiero** que el sistema nos avise a los dos con la antelación configurada **para** que ningún vencimiento se nos pase y no tenga que recordárselo al otro.
`Must · 5 pts · RF-4.2, RF-8.1, RF-8.2, RF-8.6, principio 2`

```gherkin
Escenario: Recordatorio a ambos
  Dado "ITV coche" para el 20/11 a las 10:00, con Álex como responsable y un recordatorio 7 días antes
  Cuando llega el 13/11 a las 10:00
  Entonces Lucía y Álex reciben un aviso
  Y en el correo de ambos se destaca "Responsable: Álex"

Escenario: Sin duplicados
  Dado que ya recibimos el recordatorio de 7 días
  Cuando el sistema vuelve a revisar los vencimientos
  Entonces nadie recibe ese recordatorio otra vez

Escenario: Tras una caída
  Dado que el servicio estuvo parado de 09:55 a 10:20 del 13/11
  Cuando vuelve a funcionar
  Entonces se envían los recordatorios que debían salir en ese intervalo

Escenario: Vencimiento resuelto antes del aviso
  Dado que "ITV coche" se resolvió el 10/11
  Cuando llega el 13/11
  Entonces no se envía el recordatorio de 7 días

Escenario: Antelación ya vencida al crear
  Dado que son las 15:00
  Cuando creo la cita "Médico" para hoy a las 16:30, con recordatorios de 1 día y 2 horas
  Entonces ambos reciben enseguida un único aviso "Hoy a las 16:30: Médico"
```

### US-17 · Resolver un vencimiento y renovación anual
**Como** miembro **quiero** marcar un vencimiento como resuelto, que los anuales se renueven solos y que las citas pasadas se cierren solas **para** no tener que gestionar a mano lo que ya ha pasado.
`Must · 2 pts · RF-4.3, RF-4.4`

```gherkin
Escenario: Resolver
  Dado "ITV coche" pendiente
  Cuando lo marco como resuelto
  Entonces queda resuelto y consta que lo resolví yo
  Y no se envían más recordatorios suyos

Escenario: Renovación anual
  Dado "Seguro hogar" anual que vence el 15/03/2027
  Cuando lo resuelvo
  Entonces se crea "Seguro hogar" para el 15/03/2028 con las mismas antelaciones

Escenario: Una cita pasada se cierra sola
  Dada la cita "Dentista Álex" el 05/10 a las 17:00
  Cuando pasan las 17:00
  Entonces pasa a "Pasadas" sin que nadie haga nada
  Y no genera recordatorios de atraso
```

### US-18 · Aviso diario de vencimientos atrasados
**Como** miembro **quiero** recibir un aviso diario mientras un vencimiento siga sin resolver después de su fecha **para** no olvidarlo por haber ignorado un correo.
`Should · 2 pts · RF-4.3`

```gherkin
Escenario: Pasa a atrasado
  Dado "ITV coche" sin resolver con fecha hoy a las 10:00
  Cuando pasan las 10:00
  Entonces aparece como atrasado

Escenario: Recordatorio diario con digest activo
  Dado un vencimiento atrasado
  Y un miembro con el digest activo
  Cuando llega su hora de digest
  Entonces el vencimiento aparece en su digest, cada día hasta que se resuelva

Escenario: Recordatorio diario con digest desactivado
  Dado un vencimiento atrasado
  Y un miembro con el digest desactivado
  Cuando llega su hora de digest
  Entonces recibe un aviso independiente "Sigue pendiente: ITV coche"
  Y no recibe más de uno al día por vencimiento
```

### US-41 · Editar o borrar un vencimiento o una cita
**Como** miembro **quiero** cambiar la fecha, las antelaciones o el responsable de un vencimiento o una cita, o borrarlo, **para** que los recordatorios sigan siendo correctos cuando algo cambia.
`Must · 2 pts · RF-4.1, RF-4.2`

```gherkin
Escenario: Cambiar la fecha
  Dado "Dentista Álex" el 05/10 a las 17:00, con el recordatorio de 1 día ya enviado
  Cuando la cambio al 12/10 a las 17:00
  Entonces los recordatorios se recalculan para la nueva fecha
  Y el de 1 día antes se vuelve a enviar el 11/10 a las 17:00

Escenario: Quitar una antelación
  Dada una cita con recordatorios 1 día y 2 horas antes
  Cuando quito el de 2 horas
  Entonces ese recordatorio ya no se envía

Escenario: Cambiar el responsable
  Dado "ITV coche" con Álex como responsable
  Cuando Álex cambia el responsable a Lucía
  Entonces los próximos recordatorios destacan a Lucía
  Y Lucía recibe un aviso de que ahora es la responsable

Escenario: Borrar
  Dada la cita "Concierto" con recordatorios pendientes
  Cuando la borro y confirmo
  Entonces desaparece
  Y no se envía ninguno de sus recordatorios
```

### US-36 · Adjuntar archivos a una cita o vencimiento
**Como** miembro **quiero** adjuntar reservas, billetes o entradas a una cita (o la póliza a un vencimiento) **para** tener toda la documentación en el mismo sitio que la fecha.
`Should · 3 pts · RF-4.5, RNF-SEC-10 · Entrega 3`

```gherkin
Escenario: Subir un billete
  Dada la cita "Concierto" del 15/11
  Cuando subo "entradas.pdf" de 800 KB
  Entonces queda asociada a la cita con su nombre original, su tamaño y quién la subió

Escenario: Tipo no permitido
  Dada la cita "Concierto"
  Cuando subo "factura.exe" renombrado a "factura.pdf"
  Entonces el sistema detecta por su contenido que no es un PDF
  Y lo rechaza con "Formato no permitido (PDF, JPEG, PNG o WebP)"

Escenario: Tamaño excesivo
  Dada la cita "Concierto"
  Cuando subo un archivo de 12 MB
  Entonces se rechaza con "El archivo supera los 10 MB"

Escenario: Límite de adjuntos
  Dada una cita con 10 adjuntos
  Cuando subo otro
  Entonces se rechaza indicando el máximo de 10 por elemento
```

### US-37 · Consultar, descargar y borrar adjuntos
**Como** miembro **quiero** ver y descargar los adjuntos de una cita desde la web y llegar a ellos desde el aviso **para** tenerlos a mano justo cuando los necesito.
`Should · 2 pts · RF-4.5, RNF-SEC-10 · Entrega 3`

```gherkin
Escenario: Descargar
  Dada la cita "Concierto" con "entradas.pdf"
  Cuando lo descargo con la sesión iniciada
  Entonces recibo el archivo con su nombre original

Escenario: Acceso sin sesión
  Dado el enlace de descarga de "entradas.pdf"
  Cuando alguien sin sesión lo abre
  Entonces se le pide iniciar sesión
  Y no se revela si el archivo existe

Escenario: Aviso con adjuntos
  Dada la cita "Concierto" con 2 adjuntos
  Cuando llega el recordatorio de 1 día antes
  Entonces el correo indica "2 adjuntos" con un enlace a la cita en la web
  Y los archivos no se incluyen en el correo

Escenario: Borrar un adjunto
  Dada la cita "Concierto" con "entradas.pdf"
  Cuando borro el adjunto
  Entonces desaparece de la cita y ya no se puede descargar

Escenario: Borrar la cita borra sus adjuntos
  Dada la cita "Concierto" con 2 adjuntos
  Cuando borro la cita (US-41)
  Entonces sus adjuntos ya no se pueden descargar
```

---

## E5 · Motor temporal y avisos

### US-19 · Todo lo programado ocurre a su hora, también tras una caída
**Como** miembro **quiero** que los avisos, los atrasos y (cuando exista la gestión de gastos) los gastos recurrentes lleguen a su hora sin que nadie tenga que hacer nada, incluso si el servicio se ha reiniciado, **para** poder confiar en que el sistema se acuerda por nosotros.
`Must · 5 pts · RF-9.1…RF-9.5, RNF-REL-1`

```gherkin
Escenario: Puntualidad
  Dado un aviso previsto para las 10:00, fuera de mi ventana de silencio
  Cuando llegan las 10:00
  Entonces se entrega al servidor de correo antes de las 10:02

Escenario: Recuperación tras una caída
  Dado que el servicio estuvo parado cuando tocaba el aviso de "Sacar la basura" y el recordatorio de la ITV
  Cuando vuelve a funcionar
  Entonces se envían ambos avisos

Escenario: Sin duplicados
  Dado que el motor temporal repite una ejecución, o se lanzan dos a la vez
  Cuando termina
  Entonces nada se genera ni se envía dos veces

Escenario: Fallo aislado
  Dado que una ejecución del motor temporal falla a mitad
  Cuando se lanza la siguiente
  Entonces no queda nada a medias de la ejecución fallida
  Y la siguiente completa todo lo pendiente
```

### US-20 · Aviso cuando toca una tarea
**Como** miembro **quiero** que, cuando llega la hora de una tarea, el sistema nos avise a los dos destacando a quién le toca **para** hacerla sin consultar la app y sin tener que recordársela al otro.
`Must · 3 pts · RF-8.2, principio 2`

```gherkin
Escenario: Tarea con responsable
  Dado "Poner lavadora" asignada a Lucía para hoy a las 19:00
  Cuando llegan las 19:00
  Entonces Lucía recibe "Hoy te toca: Poner lavadora"
  Y Álex la recibe como "Hoy le toca a Lucía: Poner lavadora"

Escenario: Tarea de cualquiera
  Dado "Regar las plantas", de "cualquiera", para hoy a las 20:00
  Cuando llegan las 20:00
  Entonces ambos reciben "Hoy toca: Regar las plantas" sin destacar a nadie

Escenario: Tarea ya hecha antes de su hora
  Dado "Poner lavadora" para hoy a las 19:00
  Y que Lucía la marcó como hecha a las 18:00
  Cuando llegan las 19:00
  Entonces nadie recibe el aviso
```

### US-21 · Digest diario
**Como** miembro **quiero** poder recibir (si lo tengo activado) un único correo por la mañana con el resumen del día **para** planificarme sin recibir muchos correos sueltos.
`Must · 3 pts · RF-8.2`

```gherkin
Escenario: Contenido del digest
  Dado que tengo el digest activado a las 08:00
  Cuando llegan las 08:00
  Entonces recibo un correo con: lo de hoy de ambos, lo atrasado, los vencimientos y citas de los próximos 7 días, el saldo de gastos (cuando exista la gestión de gastos) y las novedades desde el último digest: lo que ha creado el otro miembro (tareas, vencimientos, citas, gastos, liquidaciones, elementos de listas) y los gastos generados automáticamente

Escenario: Digest sin contenido
  Dado que tengo el digest activado
  Y que no hay nada de hoy, ni atrasado, ni novedades
  Cuando llega mi hora de digest
  Entonces no recibo el digest

Escenario: Digest desactivado
  Dado que tengo el digest desactivado
  Cuando llega mi hora de digest
  Entonces no recibo el resumen

Escenario: Un digest al día
  Dado que ya recibí el digest de hoy
  Cuando el sistema vuelve a procesar las 08:00 (por ejemplo, tras un reinicio)
  Entonces no recibo un segundo digest

Escenario: Avisos que coinciden con el digest
  Dado que tengo el digest a las 08:00
  Y que a las 08:00 coinciden un aviso retenido por el silencio, un recordatorio de un vencimiento de día completo y un aviso pospuesto a "mañana"
  Cuando llegan las 08:00
  Entonces los tres llegan dentro del digest, en un único correo
```

### US-22 · Ventana de silencio y agrupación
**Como** miembro **quiero** que no me lleguen avisos de noche y que los simultáneos lleguen juntos **para** que los avisos no sean una molestia.
`Must · 3 pts · RF-8.3, RF-8.4`

```gherkin
Escenario: Retención en la ventana de silencio
  Dado que mi silencio es de 22:00 a 08:00
  Cuando se genera un aviso inmediato para mí a las 23:30
  Entonces me llega a las 08:00 del día siguiente

Escenario: Agrupación
  Dado que hay 3 avisos inmediatos para mí que deben salir a la vez
  Cuando se envían
  Entonces recibo un solo correo con los 3 y un asunto del tipo "3 avisos de Tandem"

Escenario: Recordatorio que llegaría después del evento
  Dado que mi silencio es de 22:00 a 08:00
  Y una cita a las 07:30 con recordatorio de 2 horas
  Cuando se programa su recordatorio
  Entonces lo recibo a las 21:59 del día anterior, antes de que empiece el silencio
```

### US-23 · Posponer un aviso
**Como** miembro **quiero** posponer un aviso 1 hora, a mañana o 3 días **para** que me lo recuerde cuando pueda atenderlo.
`Must · 2 pts · RF-8.5`

```gherkin
Escenario: Posponer a mañana
  Dado un aviso sobre "Pedir cita pediatra"
  Cuando elijo "Mañana"
  Entonces vuelvo a recibir el aviso mañana a mi hora de digest (aunque tenga el digest desactivado)

Escenario: Resuelto mientras está pospuesto
  Dado un aviso pospuesto
  Cuando el elemento se resuelve antes de que vuelva a salir
  Entonces el aviso pospuesto ya no llega
```

### US-24 · Actuar desde el correo con un enlace de un solo uso ⭐
**Como** miembro **quiero** marcar como hecha u omitir una tarea, posponer un aviso, quedarme una tarea o resolver un vencimiento desde el propio correo **para** resolverlo en segundos sin abrir la app ni iniciar sesión.
`Must · 5 pts · RF-2.4, RF-8.7, RNF-SEC-6`

```gherkin
Escenario: Marcar como hecha desde el email
  Dado un correo con el enlace "Hecho" para la ocurrencia de "Poner lavadora"
  Cuando lo abro
  Entonces veo una página de confirmación "¿Marcar 'Poner lavadora' como hecha?" sin que haya cambiado nada
  Cuando pulso "Confirmar"
  Entonces la ocurrencia queda hecha en nombre del miembro al que se envió el correo
  Y el enlace deja de valer

Esquema del escenario: Otras acciones desde el correo
  Dado un correo con el enlace "<botón>"
  Cuando lo abro y confirmo
  Entonces <resultado>

  Ejemplos:
    | botón        | resultado                                                      |
    | Omitir       | la ocurrencia queda omitida y no cuenta en el balance          |
    | Posponer     | elijo "Mañana" y el aviso vuelve mañana a mi hora de digest    |
    | Me lo quedo  | la ocurrencia pasa a ser mía y el otro miembro recibe un aviso |
    | Resuelto     | el vencimiento queda resuelto y no se envían más recordatorios |

Escenario: Escáner de enlaces del cliente de correo
  Dado que mi correo pasa por un programa de seguridad que abre los enlaces automáticamente
  Cuando abre el enlace "Hecho"
  Entonces no se ejecuta ninguna acción
  Y el enlace sigue sirviéndome a mí

Escenario: El objeto ya se resolvió
  Dado que Álex completó la tarea desde la web
  Cuando Lucía confirma "Hecho" desde su correo
  Entonces ve "Ya estaba hecha por Álex" y no se modifica nada

Esquema del escenario: Enlace no válido
  Dado un enlace <estado>
  Cuando lo abro
  Entonces veo "Este enlace ya no es válido" y un enlace a la web, sin más detalles

  Ejemplos:
    | estado                                  |
    | ya usado                                |
    | recibido hace más de 48 horas           |
    | alterado a mano                         |
```

### US-25 · Reintentos de envío y estado de los avisos
**Como** miembro **quiero** que un fallo del correo no haga perder avisos y ver si alguno falló **para** confiar en que el sistema no se olvida.
`Should · 2 pts · RF-8.8, RNF-REL-1`

```gherkin
Escenario: Reintento
  Dado que el servicio de correo falla temporalmente
  Cuando toca enviar un aviso
  Entonces se reintenta más tarde, cada vez con más margen, sin que el aviso se pierda

Escenario: Fallo definitivo
  Dado un aviso que no se ha podido enviar tras 5 intentos
  Cuando abro la web
  Entonces veo un banner "Hay avisos que no se han podido enviar"
```

---

## E6 · Gastos

### US-26 · Registrar un gasto
**Como** miembro **quiero** registrar un gasto indicando quién pagó y cómo se reparte **para** llevar las cuentas compartidas sin otra app.
`Should · 3 pts · RF-5.1, RF-5.2, RF-8.2`

```gherkin
Escenario: Gasto con el reparto por defecto
  Dado que soy Lucía y el reparto por defecto del hogar es 50/50
  Cuando registro "Cena" de 60,00 € en la categoría "Ocio", pagada por mí, sin indicar reparto
  Entonces se reparte a medias: Álex me debe 30,00 € por este gasto
  Y Álex recibe un aviso "Lucía ha añadido un gasto: Cena 60,00 €"

Escenario: Reparto personalizado
  Dado que soy Lucía
  Cuando registro "Regalo madre Álex" de 40 €, pagado por mí, con "todo del otro"
  Entonces Álex me debe los 40 € de ese gasto

Escenario: Importe no válido
  Dado que estoy registrando un gasto
  Cuando introduzco 0 o un importe negativo
  Entonces veo un error de validación

Escenario: Categoría obligatoria y activa
  Dado que estoy registrando un gasto
  Cuando lo guardo sin categoría o con una categoría archivada
  Entonces veo un error de validación
```

### US-27 · Ver el saldo
**Como** miembro **quiero** ver en todo momento quién debe a quién **para** evitar hacer cuentas a mano.
`Should · 2 pts · RF-5.3`

```gherkin
Escenario: Cálculo del saldo
  Dado que Lucía pagó 100 € a medias y Álex pagó 20 € a medias
  Cuando consulto el saldo
  Entonces veo "Álex debe 40,00 € a Lucía"

Escenario: Gastos borrados
  Dado un gasto que se borró
  Cuando consulto el saldo
  Entonces ese gasto no cuenta

Escenario: Céntimo sobrante
  Dado que Lucía pagó 10,01 € a medias
  Cuando consulto el saldo
  Entonces veo "Álex debe 5,00 € a Lucía": el céntimo sobrante lo asume quien paga
```

### US-28 · Liquidar
**Como** miembro **quiero** registrar que hemos saldado cuentas **para** empezar de cero sin borrar el historial.
`Should · 2 pts · RF-5.4, RF-8.2`

```gherkin
Escenario: Liquidación total
  Dado que Álex debe 40 € a Lucía
  Cuando pulso "Liquidar"
  Entonces queda registrado en el historial un pago de Álex a Lucía de 40 €
  Y el saldo queda en 0
  Y el otro miembro recibe un aviso

Escenario: Sin saldo pendiente
  Dado un saldo de 0
  Cuando abro "Gastos"
  Entonces el botón "Liquidar" está deshabilitado

Escenario: El saldo cambió mientras liquidaba
  Dado que Lucía ve "Álex debe 40 €"
  Y que Álex acaba de registrar un gasto de 10 €, a medias, que pagó Lucía, y el saldo es ahora de 45 €
  Cuando Lucía confirma "Liquidar 40 €"
  Entonces no se registra nada
  Y Lucía ve "El saldo ha cambiado: ahora son 45 €"
```

### US-29 · Gestionar gastos recurrentes
**Como** miembro **quiero** definir, editar, pausar y eliminar gastos que se repiten cada mes **para** que el alquiler o la luz se apunten solos y se adapten cuando cambian.
`Should · 3 pts · RF-5.5`

```gherkin
Escenario: Generación mensual
  Dado "Alquiler" de 900 € el día 1 de cada mes, pagado por Lucía, a medias
  Cuando llega el día 1
  Entonces se registra el gasto "Alquiler" automáticamente
  Y ambos lo ven en su digest si lo tienen activado

Escenario: Sin duplicados
  Dado que el alquiler de octubre ya se registró
  Cuando el sistema vuelve a revisar ese día
  Entonces no se registra otra vez

Escenario: Editar
  Dado "Alquiler" de 900 €
  Cuando cambio el importe a 950 €
  Entonces los próximos meses se registran con 950 €
  Y los gastos ya registrados no cambian

Escenario: Pausar y reanudar
  Dado "Gimnasio" como gasto recurrente
  Cuando lo pauso
  Entonces deja de registrarse hasta que lo reanude

Escenario: Eliminar
  Dado "Netflix" como gasto recurrente
  Cuando lo elimino
  Entonces no se registran más gastos suyos
  Y los ya registrados se mantienen
```

### US-30 · Listado de gastos por mes
**Como** miembro **quiero** filtrar los gastos por mes y categoría con totales **para** entender en qué gastamos.
`Could · 2 pts · RF-5.6`

```gherkin
Escenario: Filtro
  Dados gastos de varios meses y categorías
  Cuando filtro por "septiembre" y la categoría "Supermercado"
  Entonces veo solo esos gastos y el total de la selección
```

### US-43 · Corregir o borrar un gasto
**Como** miembro **quiero** corregir o borrar un gasto mal registrado **para** que el saldo sea siempre correcto.
`Should · 2 pts · RF-5.1, RF-5.3, RF-8.2`

```gherkin
Escenario: Corregir un gasto
  Dado "Cena" de 60 € a medias, pagada por Lucía
  Cuando Lucía corrige el importe a 66 €
  Entonces el saldo se recalcula con el nuevo importe
  Y Álex recibe un aviso del cambio

Escenario: Cualquiera de los dos puede corregir
  Dado un gasto que registró Lucía
  Cuando Álex lo corrige
  Entonces se guarda el cambio y consta que lo hizo Álex
  Y Lucía recibe un aviso del cambio

Escenario: Borrar un gasto
  Dado "Cena" registrada por error
  Cuando la borro y confirmo
  Entonces deja de contar en el saldo y en los listados
  Y el otro miembro recibe un aviso

Escenario: Gasto anterior a una liquidación
  Dado que liquidamos a finales de septiembre
  Cuando corrijo un gasto de agosto
  Entonces el saldo actual refleja la diferencia
  Y la liquidación registrada no cambia
```

### US-44 · Reparto por defecto del hogar
**Como** miembro **quiero** fijar el reparto por defecto de los gastos (por ejemplo, 60/40) **para** no tener que indicarlo en cada gasto si nuestros ingresos son distintos.
`Should · 1 pt · RF-5.2, RF-8.2`

```gherkin
Escenario: Cambiar el reparto por defecto
  Dado que el reparto por defecto es 50/50
  Cuando lo cambio a 60 % Lucía y 40 % Álex
  Entonces los gastos nuevos sin reparto explícito se reparten 60/40
  Y el otro miembro recibe un aviso del cambio

Escenario: No afecta a lo ya registrado
  Dados gastos ya registrados con el reparto anterior
  Cuando cambio el reparto por defecto
  Entonces conservan su reparto y el saldo no cambia

Escenario: No afecta a los gastos recurrentes existentes
  Dado "Alquiler" recurrente definido a medias
  Cuando cambio el reparto por defecto a 60/40
  Entonces "Alquiler" sigue a medias hasta que se edite (US-29)

Escenario: Valor no válido
  Dado que estoy cambiando el reparto por defecto
  Cuando introduzco un porcentaje fuera de 0-100
  Entonces veo un error de validación
```

---

## E7 · Compra

### US-31 · Añadir, editar y quitar artículos de la lista de la compra
**Como** miembro **quiero** apuntar lo que falta en una lista compartida por categorías, y corregirla, **para** que quien vaya a comprar lo tenga todo a mano.
`Could · 2 pts · RF-6.1`

```gherkin
Escenario: Añadir artículo
  Dada la lista de la compra
  Cuando añado "Leche" con cantidad "x2" en la categoría "Lácteos"
  Entonces aparece en la lista dentro de Lácteos, en el orden de las categorías

Escenario: Categoría por defecto
  Dada la lista de la compra
  Cuando añado "Pilas" sin categoría
  Entonces se guarda en "Otros"

Escenario: Duplicado
  Dado que "Leche" ya está pendiente
  Cuando añado "leche"
  Entonces se me avisa y puedo actualizar la cantidad en lugar de duplicarla

Escenario: Editar o quitar un artículo
  Dado "Leche x2" en la lista
  Cuando cambio la cantidad a "x3" o quito el artículo
  Entonces se guarda el cambio
  Y el otro miembro lo ve al abrir o recargar la lista
```

### US-32 · Marcar artículos durante la compra
**Como** miembro **quiero** marcar lo que voy cogiendo **para** saber qué me falta mientras estoy en la tienda.
`Could · 1 pt · RF-6.2`

```gherkin
Escenario: Marcar y desmarcar
  Dado "Leche" pendiente en la lista
  Cuando la marco
  Entonces queda marcada y se muestra tachada al final de su categoría
  Cuando la desmarco
  Entonces vuelve a estar pendiente
```

### US-33 · Cerrar la compra y registrar el gasto
**Como** miembro **quiero** cerrar la compra indicando el importe **para** que lo comprado salga de la lista y el gasto se apunte solo.
`Could · 3 pts · RF-6.3, RF-6.4, RF-8.2`

```gherkin
Escenario: Cerrar con importe
  Dados 5 artículos en la lista, 4 marcados
  Cuando cierro la compra con un total de 47,30 €
  Entonces los 4 marcados salen de la lista y quedan en el historial de esa compra
  Y el artículo no marcado sigue en la lista
  Y se registra el gasto "Compra" de 47,30 € en la categoría "Supermercado", pagado por mí, con el reparto por defecto
  Y el otro miembro recibe un aviso del gasto

Escenario: Cerrar sin importe
  Dados artículos marcados en la lista
  Cuando cierro la compra sin total
  Entonces no se registra ningún gasto

Escenario: Sin artículos marcados
  Dado que no hay ningún artículo marcado
  Cuando intento cerrar la compra
  Entonces no se permite
```

### US-38 · Gestionar categorías de gastos y de la compra
**Como** miembro **quiero** crear, renombrar, ordenar y archivar las categorías de gastos y de la compra **para** adaptarlas a nuestro hogar y al recorrido de nuestro supermercado.
`Could · 2 pts · RF-5.7, RF-6.5, ADR-10`

```gherkin
Escenario: Categorías precargadas
  Dada una instalación nueva
  Cuando abro las categorías de gasto
  Entonces veo Hogar, Supermercado, Suministros, Ocio, Transporte, Salud y Otros

Escenario: Crear una categoría
  Dado que no existe la categoría de gasto "Mascota"
  Cuando la creo
  Entonces está disponible al registrar un gasto

Escenario: Reordenar la compra
  Dado que "Frutería" va antes que "Panadería"
  Cuando muevo "Panadería" por delante de "Frutería"
  Entonces la lista de la compra muestra Panadería primero

Escenario: Archivar una categoría en uso
  Dada la categoría "Transporte" con gastos registrados
  Cuando la archivo
  Entonces deja de ofrecerse para nuevos gastos
  Y los gastos existentes la conservan en el historial

Escenario: Nombre duplicado
  Dado que existe la categoría "Ocio"
  Cuando creo "ocio"
  Entonces veo un error de nombre duplicado
```

---

## E8 · Listas de interés

### US-34 · Crear listas y añadir elementos
**Como** miembro **quiero** crear listas temáticas (pelis, bares, viajes) y añadir elementos **para** guardar en un sitio común lo que queremos hacer juntos.
`Could · 2 pts · RF-7.1, RF-7.2, RF-7.3`

```gherkin
Escenario: Crear lista
  Dado que no existe la lista "Pelis"
  Cuando la creo con el emoji 🎬
  Entonces aparece en "Listas"

Escenario: Nombre duplicado
  Dado que existe la lista "Pelis"
  Cuando creo otra lista "pelis"
  Entonces veo un error de nombre duplicado

Escenario: Añadir elemento y aviso en el digest
  Dada la lista "Pelis"
  Cuando Álex añade "Perfect Days" con un enlace
  Entonces aparece en la lista como pendiente
  Y Lucía lo verá en su próximo digest como novedad
```

### US-35 · Marcar un elemento como hecho y valorarlo
**Como** miembro **quiero** marcar un elemento como visto o visitado y valorarlo **para** recordar qué nos gustó.
`Could · 1 pt · RF-7.2`

```gherkin
Escenario: Marcar con valoración
  Dado "Perfect Days" pendiente en "Pelis"
  Cuando la marco como hecha con 5 estrellas
  Entonces pasa a "Hechas" con su valoración y consta que la marqué yo

Escenario: Valoración fuera de rango
  Dado que estoy valorando "Perfect Days"
  Cuando indico una valoración de 6
  Entonces no se acepta: la valoración va de 1 a 5 estrellas
```

### US-45 · Editar, archivar y borrar listas y elementos
**Como** miembro **quiero** corregir, archivar o borrar listas y sus elementos **para** mantenerlas útiles con el tiempo.
`Could · 2 pts · RF-7.1, RF-7.2`

```gherkin
Escenario: Editar un elemento
  Dado "Perfect Days" en "Pelis"
  Cuando cambio su nota o su enlace
  Entonces se guarda el cambio

Escenario: Borrar un elemento
  Dado "Perfect Days" en "Pelis"
  Cuando lo borro
  Entonces desaparece de la lista

Escenario: Renombrar una lista
  Dada la lista "Pelis"
  Cuando la renombro a "Cine"
  Entonces conserva todos sus elementos
  Y no se admite un nombre que ya use otra lista

Escenario: Archivar una lista
  Dada la lista "Viaje a Japón", ya terminada
  Cuando la archivo
  Entonces deja de mostrarse en "Listas"
  Y puedo consultarla en "Archivadas"

Escenario: Borrar una lista
  Dada una lista creada por error
  Cuando la borro y confirmo
  Entonces desaparece junto con todos sus elementos
```

---

## E9 · Operación

### US-47 · Alerta si el motor temporal se para
**Como** operador **quiero** recibir una alerta si el motor temporal deja de ejecutarse **para** arreglarlo antes de que se pierdan avisos sin que nadie lo note.
`Must · 2 pts · RF-9.6 · Entrega 2`

```gherkin
Escenario: Todo funciona
  Dado que la última ejecución correcta del motor temporal fue hace 1 minuto
  Cuando el monitor externo consulta el estado del motor temporal
  Entonces el estado es correcto y no se envía ninguna alerta

Escenario: El motor temporal se ha parado
  Dado que el motor temporal no se ha ejecutado correctamente en más de 10 minutos
  Cuando el monitor externo consulta el estado
  Entonces el operador recibe una alerta por correo

Escenario: Falla en cada ejecución
  Dado que el motor temporal se lanza, pero todas sus ejecuciones de los últimos 10 minutos han fallado
  Cuando el monitor externo consulta el estado
  Entonces el operador recibe la misma alerta

Escenario: Recuperación
  Dada una alerta activa
  Cuando vuelve a haber una ejecución correcta
  Entonces el monitor da la alerta por resuelta y lo notifica
```

### US-48 · Consultar las métricas de éxito
**Como** operador **quiero** calcular las métricas de éxito del producto **para** comprobar si Tandem cumple sus objetivos (PRD §4.1).
`Should · 3 pts · RF-10.1 · Entrega 3`

```gherkin
Esquema del escenario: Métrica calculada
  Dadas al menos cuatro semanas de uso real
  Cuando ejecuto "tandem metrics --since 2026-10-26"
  Entonces veo <métrica> con su valor y si cumple el umbral <umbral>

  Ejemplos:
    | métrica                                                  | umbral            |
    | vencimientos que llegan a su fecha sin resolverse        | 0                 |
    | citas que empiezan sin ningún recordatorio enviado       | 0                 |
    | reparto de ocurrencias completadas por miembro           | entre 40 % y 60 % |
    | avisos sobre los que se actuó antes del vencimiento      | ≥ 70 %            |
    | semanas en que ambos miembros hicieron alguna acción     | 100 %             |
    | retraso de envío de los avisos (p95)                     | ≤ 2 min           |

Escenario: Sin datos suficientes
  Dada una instalación con menos de cuatro semanas de uso
  Cuando ejecuto "tandem metrics"
  Entonces veo las métricas con la advertencia de que el periodo es insuficiente (PRD §4.1)
```

---

## Trazabilidad RF → historias

| RF | Historias |
|---|---|
| RF-1.x | US-01 … US-05, US-39, US-46 |
| RF-2.x | US-05 … US-10, US-24, US-40 |
| RF-3.x | US-11 … US-14, US-42 |
| RF-4.x | US-15 … US-18, US-36, US-37, US-41 |
| RF-5.x | US-26 … US-30, US-38, US-43, US-44 |
| RF-6.x | US-31 … US-33, US-38 |
| RF-7.x | US-34, US-35, US-45 |
| RF-8.x | US-04, US-05, US-11, US-12, US-13, US-16, US-20 … US-26, US-28, US-33, US-40, US-42 … US-44, US-46 |
| RF-9.x | US-19, US-47 |
| RF-10.x | US-48 (RF-10.2, datos de demo, es técnico: TCK-23) |
