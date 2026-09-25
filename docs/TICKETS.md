# Tickets de trabajo — Tandem MVP

> **Fuente**: [historias de usuario](./USER_STORIES.md) · [modelo de datos](../readme.md#3-modelo-de-datos) y [API](../readme.md#4-especificación-de-la-api) en el README
> **Tipos**: `[BD]` base de datos · `[BE]` backend · `[FE]` frontend · `[INFRA]` infraestructura · `[QA]` testing
> **Estimación**: horas ideales con implementación asistida por IA, más un **colchón del 20 %** por entrega para imprevistos (tabla de totales al final). La priorización MoSCoW ([README §1.2](../readme.md#12-características-y-funcionalidades-principales)) marca el orden dentro de cada entrega; la columna "Depende de" fija el orden técnico. **MVP comprometido**: Must y Should. Los tickets que solo sirven a funcionalidades Could (TCK-15, TCK-16, TCK-18b, TCK-18c y la parte correspondiente de TCK-24) se hacen si el plan lo permite.

## Backlog

### Entrega 2 · 23-oct-2026

| ID | Tipo | Épica | Título | Historias | Depende de | Est. |
|---|---|---|---|---|---|---|
| TCK-01 | INFRA | — | Esqueleto del repositorio, Docker Compose de desarrollo (api, db, mailpit) y CI: lint, tests con umbral de cobertura (RNF-MNT-3), `import-linter` (RNF-MNT-1) y `build_readme.py --check` | — | — | 2 h |
| **TCK-02** | **BD** | **E1, E2, E3** | **Migración inicial: núcleo, `tasks` y `assignment`** | US-01, US-06, US-11, US-12, US-14 | TCK-01 | 4 h |
| TCK-03 | BE | — | Núcleo compartido: `EventBus` síncrono, `UnitOfWork`, `Clock`, registro en `domain_events` | — | TCK-02 | 2 h |
| TCK-04 | BE | E1 | Autenticación: CLI `create-user` y `set-password`, política de contraseñas NIST con lista de contraseñas comunes, login/logout, sesiones activas, cambio de contraseña, CSRF, límite de intentos en BD, cabeceras de seguridad (RNF-SEC-5) y test de rutas sin sesión (salvo login, enlaces de acción y salud) | US-01 … US-03, US-39 | TCK-03 | 4 h |
| TCK-07 | BD+BE | E4 | Dominio `deadlines`: vencimientos (también de día completo) y citas, alta, edición, borrado y resolución, antelaciones, renovación anual | US-15, US-17, US-41 | TCK-03 | 4 h |
| TCK-09a | BD+BE | E5 | Entrega de avisos: tablas `notifications` (con `planned_for`, `target_type/target_id`) y `deliveries` (con `sent_at`), puerto `Notifier` y adaptador SMTP, silencio [inicio, fin) con adelanto, agrupación, posponer (aviso nuevo con `snoozed_from_id`), reintentos, `failed` y cancelación por eventos | US-22, US-23, US-25 | TCK-03 | 5 h |
| **TCK-08** | **BE** | **E4, E5** | **Motor temporal `tandem tick` y recordatorios de vencimientos** | US-16 … US-19 | TCK-03, TCK-07, TCK-09a, TCK-23 | 5 h |
| TCK-05 | BE | E2 | Dominio `tasks` + endpoints (`POST /tasks`, completar/omitir, editar/archivar/borrar, vistas "Hoy" y "Esta semana" con citas y vencimientos, atrasadas) | US-05 … US-10, US-40 | TCK-03, TCK-07, TCK-09a | 5 h |
| TCK-06 | BE | E3 | Dominio `assignment`: reglas y cambio de modo, rotación, ausencias (alta, cambios y cancelación), "me lo quedo" concurrente, proyección del balance | US-11 … US-14, US-42 | TCK-05 | 4 h |
| TCK-12 | BE | E1, E5 | Tokens de acción: emisión, `inspect` y `redeem` (incluido `confirm_email`, que invalida los anteriores) | US-24, US-46 | TCK-05, TCK-06, TCK-07, TCK-09a | 3 h |
| TCK-09b | BE | E1 … E5 | Digest, recordatorio diario de vencimientos atrasados, avisos de tareas, de asignaciones y reasignaciones y al responsable, perfil (nombre y cambio de email con confirmación) y reprogramación al cambiar las preferencias | US-04, US-05, US-11 … US-13, US-15, US-18, US-20, US-21, US-41, US-42, US-46 | TCK-05, TCK-06, TCK-08, TCK-12 | 4 h |
| TCK-22 | BE | E1, E4, E5 | Plantillas de correo (HTML y texto por tipo de aviso, correo agrupado, digest, botones de acción, confirmación de email) y entregabilidad (SPF/DKIM) | US-16, US-20 … US-24, US-46 | TCK-09a, TCK-12 | 3 h |
| TCK-10 | FE | E1 | Esqueleto Vue 3 + Vite + TS, cliente tipado desde OpenAPI, login y logout | US-02, US-03 | TCK-04 | 2 h |
| TCK-11a | FE | E2, E5 | Vistas "Hoy" y "Esta semana", tareas y banner de avisos fallidos | US-05 … US-10, US-25, US-40 | TCK-10, TCK-05 | 4 h |
| TCK-11b | FE | E3 | Vistas de asignación, ausencias y balance | US-11 … US-14, US-42 | TCK-10, TCK-06 | 3 h |
| TCK-11c | FE | E1, E4 | Vistas de vencimientos y citas y perfil (preferencias, sesiones, contraseña, nombre y email) | US-03, US-04, US-15 … US-18, US-39, US-41, US-46 | TCK-10, TCK-07 | 4 h |
| **TCK-13** | **FE** | **E5** | **Página de acción desde el correo (`/a#token`)** | US-24 | TCK-10, TCK-12 | 2 h |
| TCK-23 | BE | — | `tandem seed-demo`: datos de demostración idempotentes (evidencias, vídeo, rendimiento) | — | TCK-05, TCK-07 | 1 h |
| TCK-19 | QA | E2, E5 | E2E con Playwright del flujo principal: crear tarea → aviso en Mailpit → acción desde el correo → reflejo en la web | US-06, US-20, US-24 | TCK-08, TCK-09b, TCK-11a, TCK-13, TCK-22 | 3 h |
| TCK-20a | INFRA | E9 | Despliegue mínimo en el VPS: Compose de producción, Caddy (HTTPS), cron, SMTP real, `GET /api/health/scheduler` y monitor externo | US-47 | TCK-08 | 3 h |

### Entrega 3 · 11-nov-2026

| ID | Tipo | Épica | Título | Historias | Depende de | Est. |
|---|---|---|---|---|---|---|
| TCK-14 | BD+BE | E6 | Dominio `expenses`: gastos (alta, corrección y borrado), redondeo, reparto por defecto, recurrentes (con FK de los gastos a su plantilla y borrado lógico), saldo, liquidación con control de concurrencia, categorías editables y avisos al otro miembro | US-26 … US-30, US-38, US-43, US-44 | TCK-03 | 5 h |
| TCK-15 | BD+BE | E7 | Dominio `shopping` + categorías ordenables + `ShoppingCompleted` → gasto (FK diferida `expenses.shopping_trip_id`, ADR-11) | US-31 … US-33, US-38 | TCK-14 | 3 h |
| TCK-16 | BD+BE | E8 | Dominio `lists`: listas y elementos (alta, edición, archivado y borrado) | US-34, US-35, US-45 | TCK-03 | 2 h |
| TCK-17 | BD+BE | E4 | Adjuntos en citas y vencimientos (`FileStorage`) | US-36, US-37 | TCK-07 | 3 h |
| TCK-18a | FE | E6 | Vistas de gastos, saldo, liquidación, recurrentes y categorías de gasto | US-26 … US-30, US-38, US-43, US-44 | TCK-14 | 4 h |
| TCK-18b | FE | E7 | Vista de la compra y categorías de la compra | US-31 … US-33, US-38 | TCK-15 | 2 h |
| TCK-18c | FE | E8 | Vistas de listas de interés | US-34, US-35, US-45 | TCK-16 | 2 h |
| TCK-18d | FE | E4 | Adjuntos en la vista de citas y vencimientos | US-36, US-37 | TCK-17 | 2 h |
| TCK-21 | BE | E9 | Comando `tandem metrics` (los campos que usa los crea TCK-09a) | US-48 | TCK-06, TCK-08, TCK-09a | 2 h |
| TCK-20b | INFRA | — | CD, backups con prueba de restauración, purgas (`rate_limit_events`, `scheduler_runs`) y alerta de disco (RNF-REL-3) | — | TCK-20a | 3 h |
| TCK-24 | QA | E6, E7, E8 | Amplía `seed-demo` con gastos, compra y listas; E2E de esos dominios; comprobación de RNF-PERF-1 con los datos de demo | US-26, US-33, US-34 | TCK-18a, TCK-18b, TCK-18c, TCK-23 | 2 h |

### Totales

| Entrega | Tickets | Estimación | Con colchón del 20 % |
|---|---|---|---|
| 2 | 20 | 67 h | ~80 h |
| 3 | 11 | 30 h | ~36 h |
| **Total** | **31** | **97 h** | **~116 h** |

Épica "—": tickets transversales (infraestructura, núcleo compartido y datos de demo) que no pertenecen a ninguna épica funcional. Las épicas se describen en [USER_STORIES.md](./USER_STORIES.md#épicas).

Los tres tickets en negrita (uno de base de datos, uno de backend y uno de frontend) se detallan en el [README §6](../readme.md#6-tickets-de-trabajo).
