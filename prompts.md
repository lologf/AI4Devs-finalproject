> Detalla en esta sección los prompts principales utilizados durante la creación del proyecto, que justifiquen el uso de asistentes de código en todas las fases del ciclo de vida del desarrollo. Esperamos un máximo de 3 por sección, principalmente los de creación inicial o  los de corrección o adición de funcionalidades que consideres más relevantes.
Puedes añadir adicionalmente la conversación completa como link o archivo adjunto si así lo consideras

## Herramientas y modelos

| Fase | Herramienta | Modelo | Uso |
|---|---|---|---|
| Entrega 1: descubrimiento, PRD, arquitectura, modelo de datos, historias, API, tickets | Claude Code (CLI) | Claude Opus 5.5 | Entrevista guiada con preguntas de opción múltiple para tomar decisiones, redacción de documentos en `docs/`, revisiones con subagentes independientes, validación de diagramas y de la especificación OpenAPI, organización de la documentación con una única fuente por contenido |
| Entrega 2: implementación | *(se completará)* | | |
| Entrega 3: tests y despliegue | *(se completará)* | | |

### Forma de trabajo con la IA (entrega 1)

1. **Contexto primero**: le paso las instrucciones del proyecto y mi idea (dominio, restricciones, arquitectura deseada y dudas) sin pedir todavía ningún entregable.
2. **Decisiones mediante preguntas**: la IA agrupa las dudas en rondas de preguntas cerradas (alcance, motor temporal, autenticación, acciones desde el correo, política de avisos, bus de eventos, frontend, despliegue, reglas de negocio, nombre), cada una con una opción recomendada y su justificación. Yo elijo.
3. **Borrador con supuestos marcados**: todo lo que la IA infiere sin que yo lo haya dicho se marca como `[ASUMIDO]`.
4. **Revisión humana**: reviso cada documento, valido o corrijo los supuestos y añado lo que falta. La IA propaga los cambios de forma coherente a PRD → modelo de datos → historias.
5. **Revisiones independientes**: pido revisiones completas; la IA lanza subagentes sin el contexto de la conversación (coherencia entre documentos, calidad de producto, revisión técnica, revisión del entregable) y comprueba contra el texto cada hallazgo antes de presentármelo, separando errores de decisiones.
6. **Verificación automática, en local** (el CI la ejecutará desde TCK-01): `npx @mermaid-js/mermaid-cli` para renderizar los diagramas, `npx @redocly/cli lint` y `jsonschema` para la OpenAPI y sus ejemplos, un Postgres 16 efímero para probar el SQL de las restricciones, `python3 scripts/build_readme.py --check` y scripts de coherencia (numeración, épicas, prioridades, trazabilidad, dependencias entre tickets, enlaces).

### Decisiones propias

Decisiones que tomé yo o que partieron de una pregunta mía:

- **Nombre del producto**: la IA propuso opciones (HestiaOS, Hearth, Tandem, Roost…); elegí **Tandem**.
- **Alcance**: la IA recomendaba dejar `shopping` y `lists` fuera del MVP; decidí incluir **todos los dominios**. En la tercera revisión acepté la recomendación de expresarlo como "MVP comprometido: Must y Should; Could si el plan lo permite".
- **Digest opcional por miembro** (no estaba en la primera versión). Consecuencia detectada por la IA: los vencimientos atrasados necesitan un aviso diario independiente si el digest está desactivado.
- **Política de contraseñas**: primero pedí reglas de composición (mayúscula, minúscula y carácter especial). En la tercera revisión la IA señaló que van en contra de NIST SP 800-63B-4 y propuso mantenerlas documentándolo como decisión mía; en su lugar decidí **seguir NIST**: 15 caracteres como mínimo (la contraseña es el único factor), sin reglas de composición y con lista de contraseñas comunes o filtradas.
- **Categorías**: pregunté si debían ser tablas o enums. La IA propuso quitarlas en tareas y elementos de listas y usar tablas editables en gastos y compra (ADR-10); lo acepté.
- **Adjuntos en citas** (reservas, billetes, entradas): funcionalidad que añadí en la revisión, con su modelo de datos, requisitos de seguridad (RNF-SEC-10) e historias (US-36, US-37).
- **Descartado**: aviso de "desequilibrio" del balance de tareas.
- **Una sola fuente por contenido**: al revisar detecté que el README repetía lo que había en `docs/`. Prompt: *"Aplicamos [la opción] 1 con cuidado de que no se pierda información ni se repita. Mucho cuidado y rigor"*. Resultado: el README contiene lo que pide la plantilla y `docs/` solo lo complementario, con enlaces en lugar de copias. Antes de borrar nada, la IA comprobó línea a línea que el contenido eliminado estaba en el README. Después elegí, entre las opciones que me dio, una excepción para las historias: `docs/USER_STORIES.md` es la única fuente de todas ellas y `scripts/build_readme.py` copia las 3 principales (⭐) al README §5; el CI lo verificará con `--check` (TCK-01).
- **Validación de supuestos**: zona horaria, horarios por defecto, caducidades de sesión y token, backups, rotación tras ausencia, duplicados en la compra, fechas pasadas.
- **FK entre dominios**: pregunté si eran incompatibles con la arquitectura hexagonal, porque quería que la integridad la garantizara el motor de BD. La IA explicó que la hexagonal separa el código y no el esquema, y propuso FK `DEFERRABLE INITIALLY DEFERRED` sin cascada; lo verificó en Postgres 16 antes de documentarlo (ADR-11). También se partió `expenses.source_ref` en dos columnas con FK.
- **Revisiones**: pedí cinco rondas de revisión completa y en cada una elegí qué aplicar. Las tres primeras se describen en las secciones 5 y 6. En la cuarta, centrada en los cambios recientes, un revisor implementó el modelo completo documentado en un Postgres 16 real (27 tablas, 40 escenarios) sin errores; solo quedaron correcciones menores, como que editar una cita sin cambiar la fecha no debe generar un aviso inmediato. La quinta fue un último repaso antes de entregar, con tres revisores independientes (coherencia, entregable frente a la plantilla y técnica): corrigió detalles de trazabilidad (un ticket para la tabla `action_tokens`, dependencias de TCK-05 y TCK-11c), un criterio de TCK-02 que no probaba lo que decía y un índice único parcial escrito como restricción, jerga técnica que quedaba en algunos criterios y la redacción; y, con mi visto bueno, añadió la FK de `balance_entries.source_event_id` (ADR-11) y definió la primera ocurrencia de las tareas de calendario.

Salvo lo indicado aquí, los cambios que describen las secciones siguientes son propuestas de la IA que revisé y acepté.

---

## Índice

0. [Herramientas, modelos y forma de trabajo](#herramientas-y-modelos)
1. [Descripción general del producto](#1-descripción-general-del-producto)
2. [Arquitectura del sistema](#2-arquitectura-del-sistema)
3. [Modelo de datos](#3-modelo-de-datos)
4. [Especificación de la API](#4-especificación-de-la-api)
5. [Historias de usuario](#5-historias-de-usuario)
6. [Tickets de trabajo](#6-tickets-de-trabajo)
7. [Pull requests](#7-pull-requests)

---

## 1. Descripción general del producto

**Prompt 1:** contexto del proyecto

> Esto es un fork de una plantilla para un proyecto final. En este repositorio tienes info, pero también te paso la info que nos han dado para que tengas un primer contexto: *(pego las instrucciones del proyecto final: entregas, fechas, ramas, README y prompts.md)*

*Resultado*: la IA analizó el repositorio (README y `prompts.md` vacíos), resumió los requisitos de cada entrega, advirtió de que la entrega 1 vencía al día siguiente y pidió la idea, el stack y mis iniciales.

**Prompt 2:** la idea y las restricciones (prompt principal de descubrimiento)

> He pensado en hacer una app para gestionar cuestiones del hogar entre una pareja (gastos, citas, tareas, compras, listas de intereses, reservas, etc.) que actualmente está en varias apps y ninguna empuja notificaciones, por lo que la carga mental es asimétrica.
>
> Los usuarios serían dos personas convivientes, ambas trabajando, se conocen de antemano y son usuarias únicas del sistema. No sería un producto multiusuario ni multihogar, esa restricción es deliberada y elimina de raíz el registro, el onboarding y el aislamiento, etc. […]
>
> En cuanto a principios de diseño, los datos hay que persistirlos y poder modificarlos, y algunos de esos datos generan notificaciones/avisos. El aviso, aunque sea para un usuario, debería notificarse a ambos […]. Las notificaciones a veces también pueden servir como entrada de datos […].
>
> *(sigue con la arquitectura, el stack, la autenticación y el canal de notificación: ver prompts de la sección 2)*
>
> […] Con toda esta info y mis dudas, ¿me puedes hacer preguntas y tomamos decisiones de cara a generar por lo menos un PRD?

*Resultado*: tres rondas de preguntas cerradas con una recomendación en cada una, más un brainstorming de nombres; después, `docs/PRD.md` (problema, lean canvas, métricas, MoSCoW, requisitos funcionales numerados, catálogo de eventos, requisitos no funcionales, ADR, riesgos, glosario). Más tarde, la arquitectura, los ADR y la seguridad pasaron al README para no duplicarlos.

**Prompt 3:** revisión del PRD

> Estoy revisando. En cuanto al PRD: lo asumido: la zona horaria para el hogar está bien asumida. La hora de las notificaciones (08:00) está bien como asumida por defecto. Entiendo que el digest diario es opcional. […] Preguntas abiertas: no hace falta ningún aviso de desequilibrio. El proveedor aún no lo sé, será el que contrate con el VPS. […]
>
> Y una cosa que se me olvidó: para una cita, creo que estaría bien tener la oportunidad de almacenar archivos (reservas, billetes, entradas, etc.). Esto habría que contemplarlo tanto en modelo de datos, PRD como historias de usuario.

*Resultado*: los supuestos validados pasaron a ser decisiones; se añadieron los adjuntos (RF-4.5, RNF-SEC-10, tabla `deadline_attachments`, US-36 y US-37) y el digest opcional por miembro, y se cerraron las preguntas abiertas del PRD.

---

## 2. Arquitectura del Sistema

### **2.1. Diagrama de arquitectura:**

**Prompt 1:** arquitectura deseada (parte del prompt de descubrimiento)

> En cuanto a arquitectura se me había ocurrido que fuera hexagonal y, si no es muy complicado, por eventos. Habría una serie de dominios, como por ejemplo tasks (tareas recurrentes o no, con periodicidad o no, historial), assignment (a quién le toca, rotación, balance, ausencias, etc.), expenses […], shopping […], deadlines o dates […], lists […], notifications (entrega: ventanas de silencio, agrupación, snooze, idempotencia), scheduler (motor temporal: recorre dominios y alimenta notifications).
>
> En principio los dominios emiten eventos, no se llaman entre sí. No sé si esto puede complicar demasiado el MVP, pero sería lo ideal. […] Cada spec declararía qué eventos emite y a cuáles reacciona: contrato explícito, dominios testeables en aislamiento. Al correr todo en un proceso basta un bus en memoria: se gana disciplina arquitectónica sin pagar infraestructura de colas. […] El canal de notificación es un adaptador: notifications decide qué, a quién y cuándo, y el adaptador decide cómo se entrega. […] El cliente sería desechable por diseño: la API HTTP sería el contrato estable.

**Prompt 2:** decisiones técnicas (respuestas a las preguntas de la IA)

La IA planteó las alternativas con su recomendación y yo elegí:

| Pregunta | Opciones planteadas | Elección |
|---|---|---|
| Motor temporal | Cron + comando `tick` / worker Python / APScheduler dentro de FastAPI | Cron + `tick` idempotente |
| Consistencia del bus | Bus síncrono + outbox / bus asíncrono | Síncrono + `notifications` como outbox |
| Frontend | Vue 3 + Vite + TS / vanilla o Alpine / React | Vue 3 + Vite + TS |
| Despliegue | Docker Compose + Caddy / systemd nativo / PaaS | Docker Compose + Caddy |

*Ajuste de la IA que acepté*: que el motor temporal no conozca a los dominios, sino que publique `ClockTicked(now, since)` y cada dominio reaccione. En aquel momento, la ventana `(since, now]` hacía el tick reanudable tras una caída. En la segunda revisión se cambió: los recordatorios se programan por adelantado y el tick es reanudable porque comprueba estados; `since` solo delimita el digest.

### **2.2. Descripción de componentes principales:**

**Prompt 1:** los componentes se derivaron del prompt de arquitectura (2.1) y de las decisiones del PRD; no hubo un prompt específico.

### **2.3. Descripción de alto nivel del proyecto y estructura de ficheros**

**Prompt 1:** la estructura prevista se generó con el README, a partir del prompt "Vale, sigue con la API, los tickets y el README" (sección 4). Se revisará al crear el esqueleto en la entrega 2 (TCK-01).

### **2.4. Infraestructura y despliegue**

**Prompt 1:** stack y despliegue (parte del prompt de descubrimiento)

> Había pensado un server HTTP rápido y seguro en Python (¿FastAPI?) y para persistir los datos un Postgres. El motor temporal no sé si hacer un scheduler recurrente en Python, Go, etc. o tirar para el MVP de un cron del sistema. Hay que evaluar. En cuanto a salida de notificaciones, SMTP. La web mínima […] y un despliegue en VPS.

### **2.5. Seguridad**

**Prompt 1:** autenticación y acciones desde el correo (parte del prompt de descubrimiento)

> En cuanto a autenticación, quiero que sea seguro pero no hace falta ni formulario de registro ni recuperación de contraseña. No sé si formulario de login + cookie de sesión o JWT. Había pensado en un Django que te trae muchas cosas por defecto de seguridad pero igual es demasiado […]. Pero quiero que sea seguro, es importante. Hay que identificar quién hace cada acción, a quién avisar, etc. […] Las acciones que puedan hacerse desde las notificaciones igual serían de momento mínimas con un token de un solo uso, o que requieran un login.

*Resultado*: sesión opaca en cookie en lugar de JWT (revocable, y en navegador acaba en cookie igualmente), tokens de acción de un solo uso con confirmación explícita. La IA propuso por iniciativa propia llevar el token en el fragmento de la URL y exigir un POST de confirmación, para que los escáneres de enlaces de Gmail u Outlook no ejecuten acciones al previsualizar el correo.

**Prompt 2:** política de contraseñas (en el prompt de revisión)

> Está bien asumida la contraseña de 12 caracteres, y debería cumplir mínimos de seguridad (mayúscula, minúscula, caracteres especiales).

*Cambio posterior*: en la tercera revisión decidí seguir NIST SP 800-63B-4 (ver "Decisiones propias"): RNF-SEC-1, US-01 y US-39 se reescribieron.

### **2.6. Tests**

**Prompt 1:** la estrategia de tests prevista se generó con el README (mismo prompt de la sección 4). Los tests reales y sus prompts se documentarán en la entrega 3.

---

### 3. Modelo de Datos

**Prompt 1:**

> Vale los tres puntos, sigue con historias y modelo de datos.

*Resultado*: el modelo de datos (hoy en el README §3) con el diagrama entidad-relación en Mermaid (claves PK/FK/UK y restricciones) y una tabla por entidad. La IA propuso garantizar en la BD las reglas críticas (máximo dos miembros con `slot`, idempotencia con claves únicas, ausencias sin solapes con una exclusion constraint) y **no usar FK entre dominios** para respetar su independencia. Más tarde lo cambié (ver "Decisiones propias"): FK diferidas también entre dominios (ADR-11).

**Prompt 2:** revisión de categorías

> En tasks: la category no debería ser otra tabla? ¿Es necesario agrupar por categorías? En list items e interest items: ¿no vendría bien categorizarlas o no lo ves necesario porque hay emoji? En expenses: ¿las categories están bien que sean un enum u otra tabla? En shopping_items: ¿las categorías están bien que sean un enum u otra tabla?

*Resultado*: sin categoría en tareas (se consultan por fecha y responsable) ni en elementos de listas (la lista es la categoría); tablas editables `expense_categories` y `shopping_categories` (esta con `sort_order` para el recorrido del súper), una por dominio.

**Prompt 3:** adjuntos (ver prompt 3 de la sección 1) → tabla `deadline_attachments` y puerto `FileStorage`.

---

### 4. Especificación de la API

**Prompt 1:**

> Vale, sigue con la API, los tickets y el README.

*Resultado*: la especificación OpenAPI 3.1 (hoy en el README §4) de los 3 endpoints del flujo principal (`POST /tasks`, `POST /occurrences/{id}/complete`, `POST /action-tokens/redeem`), errores en formato RFC 9457 y ejemplos. Validado con `redocly lint`; la IA corrigió un `oneOf` ambiguo que detectó el linter.

---

### 5. Historias de Usuario

**Prompt 1:** formato de referencia

Para el formato reutilicé el prompt del ejercicio de la sesión 4 (PR `S4: backlog inicial FlowSync + poke-holes`), que la IA leyó del repositorio de la sesión:

> […] El formato de estas User Stories debería ser: "Como [perfil] quiero [intención] para [finalidad/beneficio/problema a resolver]". No quiero que introduzcas features que no están definidas en el documento […]. Debería tener también una sección de criterios de aceptación en formato Gherkin (Given/When/Then) con 3-5 criterios de aceptación verificables y concretos. […] Estas user stories deben estar agrupadas por casos de uso, épicas o lo que tenga más sentido. Además, marca con un [ASUMIDO] todo aquello que infieras del contenido del documento pero no esté literalmente descrito.

**Prompt 2:** revisión de los supuestos

> Está bien asumido que el digest no puede caer en ventana de silencio. El digest además debe ser opcional. Está bien asumido que la notificación llegue a ambos de una tarea. […] Está bien asumido lo de la rotación: continúa después como si la hubiera hecho. Podrías resolver los asumidos, ver las dudas que te he comentado de las categorías y lo de los archivos antes de seguir adelante.

*Resultado*: 38 historias en 8 épicas con trazabilidad a los requisitos del PRD, sin supuestos pendientes. Tras las revisiones posteriores el backlog quedó en **48 historias en 9 épicas**.

**Prompt 3:** segundo análisis del backlog

> Una pregunta: ¿tenemos todas las user stories que se necesitan? ¿Están bien? ¿Necesitan ser analizadas de nuevo? Y los tickets, ¿por qué sólo se desarrollan tres? ¿Habría necesidad de épica?

La IA contrastó las historias con los requisitos del PRD y encontró huecos de CRUD y configuración (cambiar contraseña, gestionar sesiones, borrar tareas, tareas atrasadas, editar y borrar citas y gastos, reparto por defecto, gestionar recurrentes, modificar ausencias, editar listas). También vio problemas de calidad: criterios con detalles de implementación (eventos, campos, códigos HTTP), una historia "Como sistema" y escenarios sin "Dado". Tras mi *"Haz la opción 1 ahora, con cuidado y rigor"*:

- Se añadieron 7 historias (US-39 … US-45) y se ampliaron 4 (US-03, US-10, US-29, US-31), con sus requisitos en el PRD.
- Todos los criterios se reescribieron como comportamiento observable. Los detalles técnicos que salieron de ellos se comprobaron uno a uno en el README o el PRD; el formato de la clave del digest, que solo estaba en una historia, pasó al modelo de datos.
- US-19 se reformuló desde el punto de vista del miembro.
- Se añadieron fichas de épica (objetivo y criterio de cierre) y una columna de épica en el backlog de tickets.
- Una verificación automática comprobó numeración, épicas, prioridades, escenarios con "Dado", cobertura de historias por tickets y trazabilidad.
- Al escribir las historias de edición, la IA detectó dos fallos de diseño en el modelo de datos y los corrigió: la clave de idempotencia de los recordatorios no incluía la fecha, así que cambiar una cita habría silenciado sus avisos, y la regla de la siguiente ocurrencia generaba ocurrencias ya vencidas si la tarea se hacía tarde.

---

### 6. Tickets de Trabajo

**Prompt 1:** mismo prompt que en la sección 4 ("sigue con la API, los tickets y el README").

*Resultado*: backlog de 20 tickets repartidos por entregas y 3 tickets detallados (BD: migración inicial con restricciones; BE: motor temporal `tandem tick`; FE: página de acción desde el correo), con contexto, tareas técnicas, criterios Gherkin, tests, Definition of Done y fuera de alcance. Solo se detallan 3 porque es lo que pide la plantilla; el resto se refinará justo antes de implementarlo en cada entrega. Más tarde el backlog pasó de 46 h a 53 h (aún 20 tickets), con la columna de épica y las historias nuevas (ver sección 5, prompt 3).

**Prompt 2:** segunda revisión completa, con revisores independientes

> Las decisiones están bien, ¿podemos revisar de nuevo las user stories, PRD y tickets?

La IA lanzó dos subagentes sin el contexto de la conversación, uno de coherencia entre documentos y otro de calidad de producto (INVEST, cobertura, prioridades, estimaciones), y revisó ella misma el PRD. Después comprobó contra el texto los hallazgos más graves antes de presentarlos, agrupados en errores, decisiones con su recomendación y planificación. Tras mi *"Aplica todas las recomendaciones con cuidado y rigor"*:

- **Errores de diseño corregidos**:
  - La clave única de los gastos generados impedía el segundo mes de un gasto recurrente.
  - Faltaban eventos para cancelar avisos al editar o borrar.
  - Las citas pasadas se habrían recordado a diario como "atrasadas".
  - Faltaba el estado `cancelled` de las ocurrencias.
  - El balance no se podía calcular con el modelo; ahora hay una proyección `balance_entries`.
  - Al redactar los escenarios de silencio, la IA vio que los recordatorios debían **programarse por adelantado** (no en el tick) para poder adelantarlos antes del silencio, y rediseñó TCK-08.
- **Decisiones aplicadas**:
  - Acción desde el correo y despliegue mínimo adelantados a la entrega 2, para que el flujo completo funcione en ella.
  - Tareas atrasadas al terminar su día.
  - Fecha y hora obligatorias en las tareas; vencimientos de día completo.
  - Aviso inmediato si una antelación ya pasó.
  - Alerta del motor temporal (US-47) y métricas medibles (US-48, épica E9).
  - Email de avisos confirmado (US-46).
  - US-13 y US-23 pasan a Must.
  - Reglas del digest, del silencio [inicio, fin) y del redondeo.
  - Balance de quién planifica.
  - Citas y vencimientos en "Hoy".
- **Tickets**: se dividieron los grandes, se añadieron plantillas de correo, datos de demo, métricas, despliegue mínimo y restauración de backups, con dependencias explícitas. Pasan de 20 tickets y 53 h a 31 tickets y 95 h (~114 h con un colchón del 20 %).
- **Verificación automática**: numeración, épicas, prioridades, escenarios, cobertura de historias y requisitos, dependencias, diagramas, OpenAPI y enlaces.

**Prompt 3:** tercera revisión, desde tres ángulos

> ¿Aplicamos una revisión final a user stories, tickets, PRD, data model, doc OpenAPI y README?

La IA lanzó tres revisores independientes: uno técnico, que probó el SQL en un Postgres 16 efímero y validó los ejemplos de la OpenAPI con `jsonschema`; uno del entregable frente a la plantilla del máster; y uno de coherencia global. Luego separó los errores claros de las decisiones. Tras mi *"Aplica todo con tus recomendaciones, con cuidado y rigor"*, con dos decisiones mías: aceptar el mensaje de MVP que recomendó la IA y seguir NIST en lugar de mantener las reglas de composición:

- **Errores técnicos corregidos**:
  - La clave única de los avisos hacía perder recordatorios al cancelarlos y reprogramarlos; ahora el índice único excluye los cancelados.
  - `digest()` requería `pgcrypto`; ahora el hash se calcula en la aplicación.
  - La regla de asignación se crea antes que la tarea.
  - Borrar una tarea limpia sus asignaciones y avisos.
  - Un gasto recurrente por plantilla y mes.
  - Una sola ocurrencia abierta por tarea, garantizada en la BD.
  - `DROP TYPE` en el `downgrade`.
  - Clave diaria para los atrasados.
  - OpenAPI con esquemas que rechazan las combinaciones que la BD no admite y ejemplos validados.
  - CHECK e índices que faltaban.
  - Tablas completas para todas las entidades.
  - `due_on` para los vencimientos de día completo.
  - Posponer como aviso nuevo.
  - Límite de intentos en BD.
- **Tickets**: TCK-02 y TCK-08 suben 1 h cada uno (97 h, ~116 h con colchón).
- **Coherencia**: principio 2 aplicado igual en todas las historias, fechas de US-48, ejemplo de US-28, fuente de las historias en el PRD y trazabilidad de los avisos.
- **Entregable**: OpenAPI plegable con resumen previo, subíndice del modelo de datos, enlaces "↑ Índice", terminología unificada ("motor temporal", "posponer", "digest" definido) y este `prompts.md` separando mis decisiones de las propuestas aceptadas.

---

### 7. Pull Requests

**Prompt 1:** *(se completará en las entregas 2 y 3)*
