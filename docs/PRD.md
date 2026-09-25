# PRD — Tandem

> **Versión**: 1.5 · 2026-09-25
> **Autor**: Manuel Gómez Fernández (MGF)
> **Estado**: Borrador para Entrega 1 (documentación técnica)
> **Convención**: todos los supuestos iniciales (`[ASUMIDO]`) se revisaron y validaron el 24-sep-2026; hoy son decisiones. Los valores por defecto (horarios, caducidades, antelaciones) son configurables y cambiarlos no afecta a la arquitectura.
> **Alcance del documento**: producto y requisitos (qué y por qué). El [README](../readme.md) es la única fuente de la descripción del producto, la arquitectura (ADR, componentes y tecnologías, seguridad RNF-SEC, tests), el modelo de datos, la API y los tickets principales. Las historias están en [USER_STORIES.md](./USER_STORIES.md) (el README §5 copia las tres principales). Este documento enlaza en lugar de repetir.

---

## 1. Resumen, problema y propuesta de valor

Ver [README §0.3 y §1.1](../readme.md#1-descripción-general-del-producto).

---

## 2. Lean canvas

Producto personal, sin ánimo comercial: este canvas sirve para fijar el foco, no un modelo de negocio.

| Bloque | Contenido |
|---|---|
| Segmento, problema y propuesta única | [README §1.1](../readme.md#11-objetivo) |
| Solución | [README §1.2](../readme.md#12-características-y-funcionalidades-principales) |
| Métricas clave | §4 |
| Canales | Web (MVP) → app Android (futuro) |
| Ventaja | Diseñado para exactamente dos personas: sin fricción de onboarding ni configuración de grupos |
| Costes | VPS (~5 €/mes), dominio, SMTP (el que ofrezca el VPS) |

---

## 3. Usuarios

| Persona | Descripción |
|---|---|
| **Miembro A / Miembro B** | Los dos únicos usuarios. Tienen exactamente los mismos permisos. Ambos crean, modifican y completan cualquier elemento. |
| **Sistema (motor temporal)** | Actor técnico que detecta atrasos y citas pasadas, genera los gastos recurrentes y el digest, y entrega los avisos programados. |
| **Operador** | Quien instala y mantiene el sistema (en la práctica, uno de los miembros): alta de miembros, restablecimiento de contraseñas, alertas y métricas. |

Supuestos de partida:
- Los usuarios se dan de alta **por CLI** en la instalación (`tandem create-user`). No hay registro, onboarding ni recuperación de contraseña: el cambio de contraseña se hace por CLI o desde el perfil con la sesión iniciada.
- No hay importación de histórico.
- Una única zona horaria para el hogar: `Europe/Madrid`. Las fechas se guardan en UTC.
- Una única moneda: EUR.

**Escenario tipo**: Lucía y Álex viven juntos. Cada mañana a las 08:00 Tandem manda a cada uno su digest. El del lunes dice que hoy a Álex le toca sacar la basura (se alternan en cada ocurrencia), que el seguro del coche vence dentro de 5 días y que el alquiler se ha registrado automáticamente como gasto a medias. El jueves a las 19:00 Lucía recibe "Hoy te toca: poner lavadora" (y Álex, "Hoy le toca a Lucía") y la marca como hecha desde el propio correo. Álex ve el cambio en la web y el balance de la semana se actualiza.

---

## 4. Objetivos y métricas de éxito

### 4.1. De producto (medibles tras 4 semanas de uso real)

| Objetivo | Métrica | Umbral |
|---|---|---|
| Nada se olvida | Vencimientos que llegan a su fecha sin resolverse · citas que empiezan sin haber recibido ningún recordatorio | 0 · 0 |
| Reparto visible y equilibrado | Ocurrencias completadas por cada miembro (balance) | Entre 40 % y 60 % |
| Los avisos son útiles, no ruido | Avisos cuyo objeto se resolvió, pospuso o asumió (por cualquier canal) después del aviso y antes de su vencimiento; en tareas, antes de que termine su día | ≥ 70 % |
| Uso compartido | Semanas en que ambos miembros realizan al menos una acción | 100 % |
| Puntualidad | Retraso entre el momento previsto del aviso (`planned_for`, ajustado al silencio y recalculado solo si cambian las preferencias del miembro) y su aceptación por el servidor SMTP, sin contar los avisos pospuestos | ≤ 2 min (p95) |

Se calculan con `tandem metrics` (RF-10.1, US-48) a partir de `domain_events`, `notifications` y `deliveries`.

### 4.2. Del proyecto (máster)

- Flujo principal operativo de punta a punta: crear tarea → motor temporal → email → acción desde el email → reflejo en la web.
- Tests unitarios (dominios aislados), de integración (API + BD) y E2E (Playwright).
- Desplegado en VPS con HTTPS y CI/CD.
- Documentación (README, PRD, `prompts.md`) completa.

---

## 5. Alcance

### 5.1. Dentro del MVP

El MVP comprometido y la prioridad MoSCoW de cada dominio y funcionalidad están en el [README §1.2](../readme.md#12-características-y-funcionalidades-principales).

### 5.2. Fuera de alcance (explícito)

- Multiusuario, multihogar, registro, onboarding, recuperación de contraseña por email.
- App nativa Android y push FCM (el diseño lo prevé como un adaptador más).
- Integración con calendarios externos (Google Calendar, iCal).
- Importación de datos de otras apps.
- Multimoneda. Adjuntos en gastos, tareas u otros dominios (solo en citas y vencimientos). OCR o previsualización de adjuntos.
- Pesos o puntos de esfuerzo en tareas (balance ponderado).
- Colas o brokers externos (RabbitMQ, Redis): el bus es en memoria.
- Aviso de "desequilibrio" del balance de tareas: el balance solo se consulta.

---

## 6. Principios de diseño

1. **Dos usuarios, un hogar**: el sistema asume que existen exactamente dos miembros. Esto elimina el registro, el onboarding, las invitaciones, los roles y el aislamiento de datos entre hogares.
2. **Avisar a ambos**: todo recordatorio temporal se notifica a los dos miembros, destacando quién es el responsable. Los eventos causados por una persona (p. ej. "Álex ha añadido un gasto") se notifican **al otro miembro**, porque quien actúa ya lo sabe.
3. **La notificación también es una entrada**: un aviso puede incluir acciones (hecho, posponer, me lo quedo) que modifican el sistema.
4. **Dominios independientes**: principio de arquitectura, ver [README §2.1](../readme.md#21-diagrama-de-arquitectura).
5. **El cliente es sustituible**: principio de arquitectura, ver [README §2.1](../readme.md#21-diagrama-de-arquitectura).
6. **El canal es un adaptador**: principio de arquitectura, ver [README §2.1](../readme.md#21-diagrama-de-arquitectura).
7. **Trazabilidad**: toda acción registra el actor (miembro A, miembro B o sistema) y el momento.

---

## 7. Requisitos funcionales

Los identificadores (RF-x.y) se usarán para trazar historias de usuario y tickets.

### 7.1. Autenticación e identidad (`auth`)

- **RF-1.1** Login con email y contraseña; sesión persistente con cookie. Logout invalida la sesión en servidor. Cada miembro ve sus sesiones activas (navegador, IP, última actividad) y puede cerrar una concreta o todas.
- **RF-1.2** Toda petición autenticada identifica al miembro actor; las acciones quedan registradas con `actor_id`.
- **RF-1.3** Perfil del miembro: nombre visible, email de avisos (un cambio no se aplica hasta confirmarlo desde un correo enviado a la nueva dirección; mientras tanto, los avisos siguen yendo a la anterior), ventana de silencio, digest activado o desactivado y hora del digest (que no puede caer dentro de la ventana de silencio).
- **RF-1.4** Alta de miembros por CLI. Cambio de contraseña desde el perfil (exige la contraseña actual y cierra las demás sesiones) o, si se ha olvidado, restablecimiento por CLI (cierra todas sus sesiones).

### 7.2. Tareas (`tasks`)

- **RF-2.1** Crear, editar, archivar y borrar tareas con título, descripción, fecha y hora (obligatorias). Las tareas no tienen categoría: se consultan por fecha y responsable. Solo se puede borrar una tarea sin ninguna ocurrencia resuelta (hecha u omitida); si tiene alguna, se archiva.
- **RF-2.2** Tareas **puntuales** (una fecha) o **recurrentes**, con dos modos:
  - *Calendario*: cada N días, días concretos de la semana, día N del mes.
  - *Tras completar*: N días después de la última vez que se hizo (p. ej. "cambiar sábanas cada 14 días").

  Las siguientes ocurrencias conservan la hora del día de la tarea.
- **RF-2.3** Cada vencimiento de una tarea recurrente es una **ocurrencia** con estado: `pending`, `done`, `skipped`, `overdue`. Una ocurrencia pendiente queda `overdue` cuando termina su día sin resolverse: se destaca en la web y aparece en el digest, sin avisos inmediatos adicionales. Al archivar una tarea, su ocurrencia pendiente queda `cancelled`.
- **RF-2.4** Completar u omitir una ocurrencia desde la web o desde el email. Queda registrado quién y cuándo.
- **RF-2.5** Historial por tarea: ocurrencias pasadas con estado, responsable y quién la completó.
- **RF-2.6** Vistas "Hoy" y "Esta semana" con las ocurrencias pendientes de ambos y las citas y vencimientos del periodo.

### 7.3. Asignación (`assignment`)

- **RF-3.1** Modo de asignación por tarea: `fixed` (siempre la misma persona), `alternate` (rotación A/B por ocurrencia) o `anyone` (sin responsable; la asume quien la haga). El modo de una tarea existente se puede cambiar: afecta a su ocurrencia pendiente y a las siguientes, no al historial.
- **RF-3.2** **Ausencias**: un miembro registra, modifica o cancela un periodo de ausencia; las ocurrencias que le tocasen en ese periodo se reasignan al otro. Al acortarla o cancelarla, las ocurrencias pendientes reasignadas por ella vuelven a quien les tocaba según su regla (las reasignadas a mano no cambian). Una ausencia ya terminada no se modifica.
- **RF-3.3** "Me lo quedo" / "Ceder": reasignar manualmente una ocurrencia concreta (también una de "cualquiera") sin romper la rotación futura. Si los dos actúan a la vez, prevalece la primera acción.
- **RF-3.4** **Balance**: por cada miembro, ocurrencias completadas (quién hace) y tareas, vencimientos y citas creados (quién planifica; las renovaciones anuales automáticas no cuentan), en la semana, el mes y en total.

### 7.4. Citas y vencimientos (`deadlines`)

- **RF-4.1** Crear, editar y borrar vencimientos (ITV, seguro, renovación DNI) y citas (médico, cena) con fecha/hora, responsable opcional y notas. Los vencimientos pueden ser de día completo (solo fecha); las citas siempre tienen fecha y hora. Al asignar o cambiar el responsable, se avisa al nuevo responsable si no es quien hace el cambio. Al cambiar la fecha, los recordatorios se recalculan para la nueva; al borrar, se eliminan sus adjuntos y sus avisos pendientes.
- **RF-4.2** Antelaciones configurables por elemento (p. ej. 30 días + 7 días + 1 día). Por defecto: 7 días y 1 día para vencimientos; 1 día y 2 horas para citas. Los recordatorios se programan por adelantado, al crear o cambiar el elemento. Si al crearlo o moverlo alguna antelación ya ha pasado, se envía un único aviso inmediato. En los vencimientos de día completo, las antelaciones son en días y el aviso sale a la hora del digest de cada miembro.
- **RF-4.3** Marcar como resuelto. Una cita cuya hora pasa queda `past` automáticamente, sin recordatorios de atraso. Un vencimiento no resuelto al pasar su fecha (los de día completo, al empezar el día siguiente) queda `overdue` y se recuerda a ambos una vez al día, a la hora del digest de cada miembro, hasta resolverlo. Si el miembro tiene el digest activo, el recordatorio va dentro del digest; si no, se envía como aviso independiente.
- **RF-4.4** Vencimientos que se repiten anualmente (seguro del coche) con renovación automática al resolverse. Los adjuntos no se copian a la renovación.
- **RF-4.5** **Adjuntos**: subir, listar, descargar y borrar archivos asociados a una cita o vencimiento (reservas, billetes, entradas, pólizas). Formatos PDF, JPEG, PNG y WebP; máximo 10 MB por archivo y 10 archivos por elemento. Los avisos indican cuántos adjuntos hay e incluyen un enlace al elemento en la web (requiere login); los archivos **no** se adjuntan al correo.

### 7.5. Gastos (`expenses`)

- **RF-5.1** Registrar, corregir y borrar un gasto: importe, concepto, categoría, fecha, quién pagó y reparto. Cualquiera de los dos puede hacerlo; los cambios se notifican al otro y no alteran las liquidaciones ya registradas.
- **RF-5.2** Reparto por defecto del hogar (50/50, configurable desde la web), sobrescribible por gasto: % personalizado, "todo del que paga" o "todo del otro". Cambiarlo solo afecta a los gastos nuevos sin reparto explícito, no a los ya registrados ni a los recurrentes existentes.
- **RF-5.3** **Saldo neto** actualizado: "Álex debe 42,30 € a Lucía". Redondeo: la parte del otro de cada gasto se redondea a la baja al céntimo; el céntimo sobrante lo asume quien paga.
- **RF-5.4** **Liquidar**: registrar un pago de compensación que deja el saldo a 0; queda en el historial. Se confirma con el importe mostrado: si el saldo ha cambiado entretanto, se rechaza y se muestra el nuevo.
- **RF-5.5** Gastos **recurrentes** (alquiler, luz, suscripciones) que el motor temporal crea automáticamente en su fecha. Se pueden editar, pausar, reanudar y eliminar sin afectar a los gastos ya registrados.
- **RF-5.6** Listado filtrable por mes y categoría con totales.
- **RF-5.7** Gestionar las categorías de gasto (crear, renombrar, archivar). Vienen precargadas (hogar, supermercado, suministros, ocio, transporte, salud, otros); una categoría en uso no se borra, se archiva.

### 7.6. Compra (`shopping`)

- **RF-6.1** Una lista de la compra activa en la que se añaden, editan y quitan artículos con cantidad opcional y categoría (frutería, limpieza…), mostrada en el orden de las categorías.
- **RF-6.2** Marcar o desmarcar artículos como cogidos.
- **RF-6.3** **Cerrar compra**: los artículos cogidos se archivan, los no cogidos siguen en la lista y opcionalmente se indica el importe total. Emite `ShoppingCompleted`.
- **RF-6.4** Si al cerrar se indica un importe, `expenses` reacciona y registra el gasto en la categoría "Supermercado" con el reparto por defecto (ejemplo de colaboración entre dominios por eventos).
- **RF-6.5** Gestionar las categorías de la compra (crear, renombrar, archivar y **ordenar** para que sigan el recorrido del supermercado). Vienen precargadas.

### 7.7. Listas de interés (`lists`)

- **RF-7.1** Crear, renombrar, archivar y borrar listas temáticas con nombre y emoji (pelis, series, bares, viajes…). Cada lista actúa como categoría de sus elementos, así que los elementos no necesitan otra categoría.
- **RF-7.2** Añadir, editar y borrar elementos con título, nota y enlace opcional; marcarlos como hechos/vistos con valoración opcional (1-5).
- **RF-7.3** Los elementos añadidos por un miembro aparecen en el digest del otro.

### 7.8. Notificaciones (`notifications`)

- **RF-8.1** Reacciona a eventos de dominio y crea **notificaciones persistidas** (qué, a quién, cuándo, urgencia). Los avisos con fecha (recordatorios, tarea que toca) se programan por adelantado y se cancelan o reprograman cuando su objeto se resuelve, cambia o se borra.
- **RF-8.2** **Política híbrida**:
  - *Inmediatas*: recordatorios de vencimiento o cita dentro de su antelación, tarea que toca hoy (a su hora; si al crearla su hora ya ha pasado, no se envía), y acciones del otro miembro que requieren atención: asignarme, cederme o quedarse algo que era mío o de "cualquiera", cambiar una ausencia que me afecta, añadir, corregir o borrar gastos, liquidar y cambiar el reparto por defecto.
  - *Digest diario* (**opcional por miembro**, activado por defecto): resumen a la hora configurada (por defecto 08:00) con lo del día, lo atrasado, los vencimientos y citas de los próximos 7 días, el saldo (cuando exista el dominio de gastos) y las novedades desde el último digest: lo que ha creado el otro miembro (tareas, vencimientos, citas, gastos, liquidaciones, elementos de listas) y los gastos generados automáticamente. No se envía si no hay nada del día, atrasado ni novedades: el saldo por sí solo no basta. Todo aviso cuyo momento coincide con la hora del digest de un miembro que lo tiene activo (retenidos por el silencio, recordatorios de día completo, avisos pospuestos a "mañana") va dentro del digest, en un único correo.
- **RF-8.3** **Ventana de silencio** por miembro, intervalo [inicio, fin) (por defecto 22:00–08:00): las inmediatas se retienen hasta el final de la ventana. Si eso dejara un aviso en o después de su límite (la hora de la cita o del vencimiento; en tareas, el final de su día), se adelanta al minuto anterior al inicio del silencio.
- **RF-8.4** **Agrupación**: las inmediatas pendientes para un mismo destinatario en un mismo tick se envían en un único correo.
- **RF-8.5** **Posponer** (snooze) un aviso: 1 h, mañana o 3 días. Crea un aviso nuevo enlazado al original, que no se reabre.
- **RF-8.6** **Idempotencia**: cada notificación tiene una clave única (`tipo + entidad + fecha objetivo + umbral + destinatario`), de modo que reprocesar un tick nunca duplica avisos. En los avisos diarios (vencimientos atrasados, digest), el umbral incluye el día. Un aviso cancelado no impide reprogramarlo con la misma clave.
- **RF-8.7** **Acciones en el aviso** (hecho, omitir, posponer, me lo quedo, resolver; y confirmar el email de avisos): enlaces con token de un solo uso (ver RNF-SEC-6 en el [README §2.5](../readme.md#25-seguridad)).
- **RF-8.8** Reintentos con backoff ante fallos SMTP; tras 5 fallos queda `failed` y es visible en la web.

### 7.9. Motor temporal (`scheduler`)

- **RF-9.1** Un comando `tandem tick` que se ejecuta cada minuto (cron). Publica `ClockTicked(now, since)` en el bus, donde `since` es el último tick correcto.
- **RF-9.2** Cada dominio reacciona a `ClockTicked` generando sus eventos temporales (ocurrencias y vencimientos atrasados, citas pasadas, gastos recurrentes, digest).
- **RF-9.3** Tras procesar los dominios, el tick entrega las notificaciones pendientes cuyo momento de envío ya ha llegado.
- **RF-9.4** El tick es **idempotente** y **reanudable**: si un tick falla o no se ejecuta, el siguiente recupera lo pendiente.
- **RF-9.5** Exclusión mutua mediante un advisory lock de Postgres (dos ticks nunca corren a la vez).
- **RF-9.6** `GET /api/health/scheduler` responde 503 si el último tick correcto tiene más de 10 minutos; un monitor externo lo consulta y avisa al operador. Es público y no devuelve datos.

### 7.10. Operación

- **RF-10.1** `tandem metrics [--since fecha]` calcula las métricas de éxito de §4.1.
- **RF-10.2** `tandem seed-demo` carga datos de demostración de forma idempotente (evidencias, vídeo y pruebas de rendimiento).

---

## 8. Catálogo de eventos (contrato entre dominios)

| Dominio | Emite | Reacciona a |
|---|---|---|
| `scheduler` | `ClockTicked(now, since)` | — |
| `auth` (núcleo) | `MemberProfileUpdated`, `NotifyEmailChangeRequested`, `NotifyEmailChanged`, `PasswordChanged` | — |
| `tasks` | `TaskCreated`, `TaskUpdated`, `TaskArchived`, `TaskDeleted` (incluye los ids de sus ocurrencias), `OccurrenceCreated`, `OccurrenceRescheduled`, `OccurrenceCompleted`, `OccurrenceSkipped`, `OccurrenceOverdue`, `OccurrenceCancelled` | `ClockTicked` (atrasadas) |
| `assignment` | `AssignmentRuleChanged`, `OccurrenceAssigned`, `OccurrenceReassigned`, `AbsenceRegistered`, `AbsenceUpdated`, `AbsenceCancelled` | `OccurrenceCreated` (asignar), `OccurrenceCompleted`, `TaskCreated`, `DeadlineCreated`, `DeadlineDeleted` (balance), `TaskDeleted` (balance y borrado de la regla y las asignaciones) |
| `deadlines` | `DeadlineCreated`, `DeadlineUpdated`, `DeadlineDeleted`, `DeadlineResolved`, `DeadlineOverdue`, `AppointmentPassed`, `AttachmentAdded`, `AttachmentRemoved` | `ClockTicked` (atrasos y citas pasadas) |
| `expenses` | `ExpenseRecorded`, `ExpenseUpdated`, `ExpenseDeleted`, `SettlementRecorded`, `DefaultSplitChanged`, `RecurringExpenseDefined`, `RecurringExpenseUpdated`, `RecurringExpenseDeleted`, `ExpenseCategoryChanged` | `ClockTicked` (recurrentes), `ShoppingCompleted` |
| `shopping` | `ShoppingItemAdded`, `ShoppingItemUpdated`, `ShoppingItemRemoved`, `ShoppingCompleted`, `ShoppingCategoryChanged` | — |
| `lists` | `ListCreated`, `ListUpdated`, `ListArchived`, `ListDeleted`, `ListItemAdded`, `ListItemUpdated`, `ListItemDeleted`, `ListItemDone` | — |
| `notifications` | `NotificationScheduled`, `NotificationSent`, `NotificationFailed`, `NotificationCancelled`, `NotificationSnoozed` | Los eventos relevantes para el usuario de todos los dominios: programa avisos (p. ej. `DeadlineCreated`, `OccurrenceCreated`), los cancela o reprograma (p. ej. `DeadlineUpdated`, `DeadlineDeleted`, `OccurrenceCompleted`, `TaskDeleted`, `AppointmentPassed`), avisa al otro miembro de sus acciones, envía la confirmación de `NotifyEmailChangeRequested` y reprograma los pendientes de un miembro en `MemberProfileUpdated` (silencio u hora del digest); `ClockTicked` (digest y recordatorio diario de vencimientos atrasados) |

Cada evento es inmutable e incluye: `event_id`, `occurred_at`, `actor_id` (miembro o `system`) y su payload tipado. Todos se guardan en `domain_events` (auditoría, RNF-SEC-8).

---

## 9. Requisitos no funcionales

### 9.1. Seguridad (prioritaria)

Los requisitos **RNF-SEC-1 … RNF-SEC-10** se documentan en el [README §2.5](../readme.md#25-seguridad).

### 9.2. Fiabilidad

- **RNF-REL-1** Ningún aviso se pierde por un fallo de SMTP (outbox persistente + reintentos).
- **RNF-REL-2** Consistencia transaccional: el cambio de estado y los efectos de los handlers síncronos se confirman en la misma transacción (unit of work).
- **RNF-REL-3** Mantenimiento: purga de datos técnicos (`rate_limit_events` con más de 30 días, `scheduler_runs` con más de 7) y alerta al operador si el disco de adjuntos supera el 80 %.

### 9.3. Rendimiento

- **RNF-PERF-1** p95 < 300 ms en endpoints de la API con el volumen esperado (miles de filas, no millones).
- **RNF-PERF-2** Un tick completo < 5 s.

### 9.4. Mantenibilidad y testabilidad

- **RNF-MNT-1** Los dominios no importan infraestructura (FastAPI, SQLAlchemy, SMTP); dependen de puertos.
- **RNF-MNT-2** Reloj inyectable (`Clock`): toda la lógica temporal es testeable sin esperas.
- **RNF-MNT-3** Cobertura ≥ 80 % en la capa de dominio.
- **RNF-MNT-4** Contrato OpenAPI generado automáticamente; tipos del frontend generados desde él.

### 9.5. Usabilidad

- **RNF-UX-1** Web responsive usable en móvil (será el uso principal hasta que exista la app Android).
- **RNF-UX-2** UI en español.

---

## 10. Arquitectura y stack técnico

Ver [README §2](../readme.md#2-arquitectura-del-sistema): diagrama, patrón, ADR, componentes y tecnologías, estructura, infraestructura, seguridad y tests.

---

## 11. Plan por entregas

| Entrega | Fecha | Contenido |
|---|---|---|
| 1. Documentación | 25-sep-2026 | PRD, README (ficha, arquitectura, modelo de datos, API, historias, tickets), `prompts.md` |
| 2. Código funcional | 23-oct-2026 | Esqueleto hexagonal, auth, `tasks` + `assignment` + `deadlines`, `scheduler` + `notifications` + SMTP, acciones desde el correo y despliegue mínimo en el VPS con monitor del motor temporal. Flujo principal de punta a punta (crear tarea → aviso por correo → acción desde el correo → reflejo en la web), cubierto por un test E2E |
| 3. Final | 11-nov-2026 | `expenses`, `shopping`, `lists`, adjuntos, métricas, resto de tests E2E, CD, backups con restauración probada, purgas, evidencias |

---

## 12. Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Alcance amplio (~97 h estimadas) | Alto | MVP comprometido = Must + Should; los Could (compra, listas y algunas vistas) solo si el plan lo permite ([README §1.2](../readme.md#12-características-y-funcionalidades-principales)); plantilla común por dominio |
| Complejidad del bus de eventos | Medio | Bus síncrono y mínimo (≈50 líneas); sin sagas ni reintentos a nivel de evento |
| Recurrencias y zonas horarias (DST) | Medio | Guardar en UTC, calcular en `Europe/Madrid`, tests con cambios de hora |
| Correos en spam / fallos SMTP | Medio | Proveedor SMTP con SPF/DKIM; outbox con reintentos; estado visible en la web |
| Escáneres de email ejecutando acciones | Medio | Confirmación por POST (RNF-SEC-6) |
| El motor temporal se detiene sin que nadie lo note | Alto | Monitor externo sobre `GET /api/health/scheduler` (RF-9.6, US-47) |
| Un error en el email de avisos deja a un miembro sin avisos | Medio | El cambio se confirma desde la nueva dirección (RF-1.3) |
| Fatiga de notificaciones | Medio | Digest opcional, agrupación, ventanas de silencio, posponer; métrica de avisos accionados |
| Archivos maliciosos o disco lleno por adjuntos | Medio | Lista blanca de tipos por magic bytes, límites de tamaño y número, descarga como adjunto, alerta de disco |

---

## 13. Preguntas abiertas

Ninguna. Las decisiones de las revisiones del 24 y el 25-sep-2026 están incorporadas en este documento y en el README; el razonamiento que llevó a cada una está en [prompts.md](../prompts.md).

---

## 14. Glosario

| Término | Definición |
|---|---|
| **Miembro** | Cada uno de los dos usuarios del hogar |
| **Ocurrencia** | Instancia concreta de una tarea en una fecha (una tarea recurrente genera muchas) |
| **Rotación** | Alternancia automática del responsable entre ocurrencias |
| **Ausencia** | Periodo en que un miembro no puede asumir tareas; provoca reasignación |
| **Antelación** | Tiempo antes de un vencimiento o cita en que se envía un recordatorio |
| **Digest** | Correo resumen diario |
| **Ventana de silencio** | Franja horaria en que no se envían avisos inmediatos |
| **Posponer (snooze)** | Volver a recibir un aviso más tarde (1 h, mañana o 3 días) |
| **Outbox** | Tabla de notificaciones pendientes de entregar; garantiza que no se pierdan |
| **Tick** | Ejecución periódica (cada minuto) del motor temporal |
| **Liquidación** | Pago que compensa el saldo entre miembros y lo deja a 0 |
| **Token de acción** | Credencial de un solo uso incluida en un email para ejecutar una acción concreta |
| **Adjunto** | Archivo (PDF o imagen) asociado a una cita o vencimiento |
| **Vencimiento de día completo** | Vencimiento sin hora ("el seguro vence el 20/11"): pasa a atrasado al empezar el día siguiente |
| **Cita pasada** | Cita cuya hora ya ha pasado: se cierra sola, sin recordatorios de atraso |
| **Balance** | Recuento, por miembro, de lo que ha completado (hace) y de lo que ha creado (planifica) |
