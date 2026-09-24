# Booked para Claude y ChatGPT

Los paquetes conectan al servidor MCP de
[Booked](https://booked.fincasdelavilla.com) —noventa y cuatro herramientas sobre
propiedades, reservas, contactos, calendario y dinero, veintiocho de ellas de escritura— e
incluyen una skill con las reglas de negocio que no caben en la descripción de
una herramienta.

Este repositorio incluye el *marketplace* de Claude y los paquetes para ambas
plataformas. Claude se instala por URL; ChatGPT requiere registrar su conexión
y generar el paquete con ese identificador. Las publicaciones siguen el
[versionado](#versionado) de los manifiestos.


## Paquetes

| Paquete | Plataforma | Autenticación |
| --- | --- | --- |
| `booked` | Claude Code / Cowork, instalaciones existentes | Token manual, máximo 30 días |
| `booked-oauth` | Claude Code / Cowork | Inicio de sesión en Booked, OAuth |
| `booked-chatgpt` | ChatGPT; manifiesto compatible con Codex | Inicio de sesión en Booked, OAuth |

Instala una sola variante de Booked en cada cliente para evitar herramientas
repetidas. Las reglas de negocio se mantienen en `shared/booked-fincas.md` y
se generan con `python3 scripts/sync-skills.py`. No edites las copias generadas.

**Versión 0.13.0:** despliega primero el
[PR #590](https://github.com/ruizbjaime/booked/pull/590) de Booked, que trae
las reservas de conjunto, editar, cambiar de estado y cobrar reservas, las
solicitudes del sitio, el cumplimiento TRA/SIRE y las nuevas lecturas. El
backend debe incluir también los PR que traen sincronizar calendarios ([PR #587](https://github.com/ruizbjaime/booked/pull/587)),
editar propiedades ([PR #588](https://github.com/ruizbjaime/booked/pull/588)) y
gastos, nómina e informes financieros ([PR #589](https://github.com/ruizbjaime/booked/pull/589)).
Editar bloqueos requiere el [PR #586](https://github.com/ruizbjaime/booked/pull/586),
con las notas de los bloqueos ([PR #585](https://github.com/ruizbjaime/booked/pull/585)).
Las preguntas de análisis requieren los PR [#583](https://github.com/ruizbjaime/booked/pull/583)
y [#584](https://github.com/ruizbjaime/booked/pull/584).
El backend también debe incluir la gestión de cotizaciones
([PR #581](https://github.com/ruizbjaime/booked/pull/581)), la retención o
devolución de cancelaciones ([PR #579](https://github.com/ruizbjaime/booked/pull/579)), reservas comisionadas
([PR #576](https://github.com/ruizbjaime/booked/pull/576)), cotizaciones
([PR #575](https://github.com/ruizbjaime/booked/pull/575)) y contactos
([PR #574](https://github.com/ruizbjaime/booked/pull/574)). Actualizar el
plugin no despliega el servidor ni amplía permisos existentes.
OAuth requiere además el soporte de la rama `feat/mcp-oauth` del backend.
Estos archivos preparan los paquetes; no registran ni publican una app en ChatGPT.

## Instalar con OAuth

El administrador debe completar primero [la configuración del backend](#preparar-el-backend).

En Booked, crea una integración en **Ajustes → Integraciones API** y selecciona
las propiedades administradas y comisionadas que quieres compartir. No necesitas
emitir un token manual. Durante la vinculación, escoge esa integración y marca
los permisos de lectura y, si quieres escribir desde el cliente, los de escritura. La pantalla muestra el alcance antes de autorizar.

### Claude

Añade el marketplace `ruizbjaime/booked-plugin` e instala **Booked — conexión con
OAuth**. En Claude Code:

```bash
claude plugin marketplace add ruizbjaime/booked-plugin
claude plugin install booked-oauth@booked
```

Abre `/mcp` y completa la autenticación de Booked en el navegador. En Claude /
Cowork también puedes añadir un conector remoto con la URL
`https://booked.fincasdelavilla.com/mcp/oauth` y completar la vinculación.
El servidor admite registro dinámico de clientes para los retornos permitidos.

### ChatGPT

1. Activa el modo desarrollador si está disponible en tu cuenta o espacio.
2. Registra una conexión MCP con
   `https://booked.fincasdelavilla.com/mcp/oauth`, autenticación OAuth y registro
   dinámico. Inicia sesión en Booked y autoriza el alcance.
3. Copia el ID técnico de la conexión real (`plugin_asdk_app_…`).
4. Genera el paquete con esa conexión. El directorio de salida debe ser nuevo,
   llamarse `booked-chatgpt` y quedar fuera de `plugins/booked-chatgpt`, incluso
   si se accede a él mediante un enlace simbólico:

```bash
python3 scripts/configure-chatgpt.py --app-id ID_REAL --output /tmp/booked-chatgpt
```

El script crea `.app.json` y enlaza el manifiesto a la conexión registrada.
El paquete fuente mantiene `.mcp.json` para clientes que aceptan MCP directo;
ChatGPT necesita el registro de la conexión. Instala el paquete generado por
la vía de plugins disponible en tu espacio; el marketplace de Claude no se
instala directamente en ChatGPT. La publicación pública es un paso separado.
Consulta la [documentación oficial de empaquetado](https://developers.openai.com/plugins/build/plugins).

### Caducidad y revocación

- **Token manual:** máximo 30 días, como antes.
- **OAuth:** autorización sin vencimiento temporal; accesos de 15 minutos y
  credenciales de renovación rotatorias sin caducidad temporal.
- Revoca el registro **OAuth …** desde la ficha de la integración en Booked
  para bloquear tanto consultas como renovaciones. Desactivar la integración
  o al anfitrión también bloquea el acceso. Quitar un plugin del cliente no
  sustituye la revocación en Booked.
- La contraseña se introduce únicamente en Booked. Ningún paquete guarda
  contraseñas, secretos de cliente ni tokens de usuario en el repositorio.

## Preparar el backend

En el repositorio de la aplicación, con el soporte OAuth y los cambios del
[PR #574](https://github.com/ruizbjaime/booked/pull/574) y del
[PR #575](https://github.com/ruizbjaime/booked/pull/575) revisados:

1. Instala las dependencias bloqueadas con `composer install` y aplica las
   migraciones mediante el procedimiento de despliegue habitual.
2. Genera las claves con `php artisan passport:keys` **solo si aún no existen**.
   Conserva las claves entre despliegues y protege también `APP_KEY`: cambiar
   esas claves invalida credenciales existentes. Nunca las subas a Git.
3. Configura `APP_URL` con el origen HTTPS del panel y habilita
   `INTEGRATION_OAUTH_ENABLED=true`. Reconstruye la caché de configuración.
4. Verifica que el proxy admite `/mcp/oauth`, `/oauth/authorize`, `/oauth/token`,
   `/oauth/register` y `/.well-known/oauth-*` en el dominio del panel.
5. Verifica descubrimiento, consentimiento y consulta con una cuenta de prueba
   en Claude y otra en ChatGPT antes de distribuir la versión. Confirma que el
   servidor ofrece `ver_contactos`, `crear_contacto` y `eliminar_contacto`, y que
   `editar_bloqueo` y `eliminar_bloqueo` exigen `confirmado: true`. Comprueba también que ofrece
   `preparar_cotizacion`, `crear_cotizacion` y `ver_cotizaciones`, con sus
   tres flujos de gestión, las doce de análisis (de `huespedes_recurrentes`
   a `comparativo_interanual`), `gastos`, `gastos_de_nomina` e
   `informe_financiero`, `preparar_edicion_de_propiedad` con
   `editar_propiedad`, `sincronizar_calendarios` con
   `estado_de_sincronizacion`, y las veintinueve del
   [PR #590](https://github.com/ruizbjaime/booked/pull/590), entre ellas
   `ver_conjuntos`, `cotizar_conjunto`, `preparar_reserva_de_conjunto`,
   `solicitudes`, `cumplimiento_tra_sire` y `preparar_pago_de_reserva`;
   `tools/list` debe devolver las noventa y cuatro en una sola página. Actualizar solo el plugin no
   incorpora estas herramientas ni sus permisos al backend.

El registro dinámico permite HTTPS en `chatgpt.com`, `chat.openai.com`,
`claude.ai` y `claude.com`, y retornos locales de Claude Code. Las URI exactas
quedan fijadas en cada cliente registrado; no se admiten fragmentos ni credenciales
embebidas. Los límites de solicitudes también cubren el registro y los canjes.

Para revertir la habilitación, establece `INTEGRATION_OAUTH_ENABLED=false`:
la entrada histórica `/mcp` con Sanctum sigue funcionando. Antes de revertir
migraciones, revoca las autorizaciones OAuth; la migración también las invalida
al recuperar la columna de caducidad obligatoria.

## Desarrollo y validación

```bash
python3 scripts/sync-skills.py
python3 scripts/validate.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Las versiones de los tres paquetes y las entradas del marketplace de Claude
se publican coordinadas. CI exige el catálogo completo, versiones coincidentes,
la configuración de autenticación y rutas válidas a las skills y conexiones,
tanto en la fuente como en el paquete generado. También comprueba que las
skills coincidan con su fuente y ejecuta las pruebas de regresión en copias
temporales. La versión del servidor MCP sigue siendo independiente.

Las comprobaciones Python no requieren red y se ejecutan antes de instalar
Claude Code. CI fija Claude Code en `2.1.278`, la versión usada para validar
estos paquetes; actualiza esa versión de forma explícita al comprobar
compatibilidad con una nueva versión del cliente.

## Instalar la variante con token en Cowork

1. **Customize → Plugins → Add marketplace** y pega `ruizbjaime/booked-plugin`.
2. Instala **Booked** desde ese marketplace.
3. Cuando pida el **token de la integración**, pega el tuyo. Se emite en
   *Booked → Ajustes → Integraciones API* y se muestra una sola vez. El token
   decide lo que el plugin puede hacer: mira [Lectura y escritura](#lectura-y-escritura).

Para actualizar: **Update** en el marketplace.

## Instalar la variante con token en Claude Code

```bash
claude plugin marketplace add ruizbjaime/booked-plugin
claude plugin install booked@booked
```

## El token manual caduca a los 30 días

Es el techo que impone Booked a todo token de integración, y no se puede alargar
desde el plugin. Cuando el plugin conteste que no hay credenciales válidas, el
token está vacío, caducado o revocado — las tres se arreglan igual:

1. En *Booked → Ajustes → Integraciones API*, revoca el token viejo si sigue
   listado (su nombre queda reservado mientras no se revoque, aunque haya
   caducado) y emite uno nuevo con las mismas capacidades.
2. Pega el nuevo en la configuración del plugin: en Cowork, desde la ficha del
   plugin en **Customize → Plugins**; en Claude Code, desde el gestor `/plugin`.
   El almacenamiento depende del cliente y del sistema. Claude Code usa el
   llavero de macOS cuando está disponible; si falla o no hay un llavero
   compatible, usa `~/.claude/.credentials.json`. `sensitive: true` oculta el
   valor y evita guardarlo en `settings.json`, pero no garantiza un llavero en
   todas las plataformas. Consulta la
   [referencia de configuración de Claude](https://code.claude.com/docs/en/plugins-reference#user-configuration).

La herramienta `alcance_del_token` devuelve `caduca`; la skill le pide al
modelo que avise cuando falte menos de una semana.

## Versionado

Cada publicación sube `version` en los manifiestos de los tres paquetes y en
las entradas del marketplace de Claude, y lleva un tag `vX.Y.Z`. CI comprueba
que las versiones coincidan. La versión de los paquetes es independiente de
la del servidor MCP (`#[Version]` en `BookedServer`). El detalle de cada versión
está en [CHANGELOG.md](CHANGELOG.md).

## Qué hay dentro

```
shared/                          # la fuente de las skills: edita aquí, no las copias
├── booked-fincas.md             # las reglas de la respuesta: dinero, ids, alcance
├── auth-manual.md               # qué decir cuando falla el token manual
└── auth-oauth.md                # qué decir cuando falla la autorización OAuth
scripts/
├── sync-skills.py               # genera cada SKILL.md desde shared/ (--check en CI)
├── validate.py                  # versiones, conexiones y skills al día
└── configure-chatgpt.py         # empaqueta ChatGPT con el ID de su conexión
plugins/booked/                  # Claude, token manual
├── .claude-plugin/plugin.json   # identidad y el token que se pide al instalar
├── .mcp.json                    # el conector HTTP a /mcp, con el bearer en la cabecera
└── skills/booked-fincas/        # generada
plugins/booked-oauth/            # Claude, OAuth
├── .claude-plugin/plugin.json   # identidad; no pide token
├── .mcp.json                    # el conector HTTP a /mcp/oauth, sin cabeceras
└── skills/booked-fincas/        # generada
plugins/booked-chatgpt/          # ChatGPT, OAuth
├── .codex-plugin/plugin.json    # manifiesto OpenAI
├── .mcp.json                    # /mcp/oauth; el paquete generado lo cambia por .app.json
└── skills/booked-fincas/        # generada
```

En `booked`, el token viaja como `Authorization: Bearer` hacia
`https://booked.fincasdelavilla.com/mcp`. El cliente gestiona su almacenamiento
con `sensitive: true`, según lo explicado arriba; el paquete no lo guarda en
este repositorio. Los paquetes OAuth no llevan credenciales: el cliente las
obtiene al vincularse con
`https://booked.fincasdelavilla.com/mcp/oauth`. El servidor vive en el repo de
la aplicación, en `app/Mcp/`, y la puerta remota se monta en `routes/ai.php`.

## Cotizaciones persistidas

La skill ya guía `preparar_cotizacion` → confirmación explícita →
`crear_cotizacion` para propiedades propias, administradas y comisionadas.
El servidor pregunta datos y selecciones pendientes y guarda un borrador
con número y enlace; no reserva fechas, registra pagos ni envía mensajes.

Para usar esta función, despliega el soporte correspondiente de
Booked y comprueba ambas herramientas en `tools/list`. Habilita escrituras
con `INTEGRATION_WRITES_ENABLED=true` y concede «Guardar cotizaciones» más
las lecturas de la rama y los permisos de contactos necesarios. Los tokens y
consentimientos existentes no ganan permisos automáticamente. Ante una
respuesta perdida, consulta `ver_cotizaciones` antes de repetir.

## Gestionar cotizaciones

`ver_cotizaciones` lista las cotizaciones de una propiedad (administrada o
comisionada) con filtros por propiedad, estado y número, o da el detalle de una:
desglose, destinatario, notas, `acciones_posibles` y si ya es una reserva. Las
de un conjunto llevan `tipo_inventario: conjunto` y sus cabañas; de ellas
solo se editan las notas, y convertirlas crea una reserva por cabaña, todas o
ninguna. Tres flujos escriben, cada uno con
preparación, resumen, firma de un solo uso (treinta minutos, sin cruzar la
medianoche) y el sí explícito del anfitrión:

- **Cambiar el estado** (`preparar_cambio_de_estado_de_cotizacion` →
  `cambiar_estado_de_cotizacion`): enviar, aceptar, rechazar o volver a
  borrador. «Enviar» solo registra que el anfitrión la envió; Booked no manda
  nada al huésped. Rechazar es definitivo.
- **Editar un borrador** (`preparar_edicion_de_cotizacion` →
  `editar_cotizacion`): fechas, vigencia, ocupación, descuentos y notas, y en
  comisionadas alojamiento, cargos y comisión. Solo se envían los campos que
  cambian; el precio se recalcula a la fecha de hoy como en la ficha.
- **Convertir en reserva** (`preparar_conversion_de_cotizacion` →
  `convertir_cotizacion_en_reserva`): una cotización aceptada pasa a reserva
  pendiente con su precio y retiene las noches. La preparación pregunta método
  y compromiso de pago, el huésped real si el destinatario es un comisionista,
  un teléfono si falta y, en cotizaciones antiguas sin precio guardado, si se
  acepta el precio vigente.

La escritura se niega si la cotización, su precio o las condiciones de pago
cambiaron desde la preparación. Primero debe desplegarse el
[PR #581 del servidor](https://github.com/ruizbjaime/booked/pull/581) y estar
habilitado `INTEGRATION_WRITES_ENABLED=true`. Emite un token aparte o vuelve a
autorizar OAuth con «Cambiar el estado de cotizaciones» (`quotations:transition`),
«Editar cotizaciones» (`quotations:update`) o «Convertir cotizaciones en
reservas» (`quotations:convert`), además de «Cotizaciones» (`quotations:read`).
Actualizar el plugin no concede estos permisos.

## Crear reservas comisionadas

`preparar_reserva_comisionada` recibe la propiedad de
`listar_propiedades_comisionadas`, un huésped de `ver_contactos` y los datos
proporcionados por el anfitrión. Un contacto nuevo se crea por separado con
`crear_contacto` y su permiso `contacts:create`. La entrada debe ser hoy o
posterior; la salida es exclusiva. Se solicitan estado pendiente o confirmado,
ocupación, alojamiento, cargos y una sola forma de comisión (configurada,
porcentaje o monto fijo). Los importes viajan en centavos enteros. Las edades
son opcionales, pero una lista proporcionada debe incluir a todos los niños.

La preparación no ocupa noches. Con solo permisos de lectura puede mostrar el
resumen, pero no entrega una firma de creación. La disponibilidad únicamente
cubre las reservas registradas en Booked; hay que comprobarla con el propietario.
Tras leer el resumen completo y recibir el sí explícito del anfitrión,
`crear_reserva_comisionada` recibe solo `firma` y `confirmado: true`. La firma
está vinculada a la credencial y es válida hasta treinta minutos, sin pasar de
medianoche en Bogotá. El servidor vuelve a comprobar los datos y la disponibilidad.
No se registran pagos ni cobros de comisión. Si se pierde la respuesta, consulta
`reservas_comisionadas` antes de preparar otra creación.

Primero debe desplegarse el [PR #576 del servidor](https://github.com/ruizbjaime/booked/pull/576)
y estar habilitado `INTEGRATION_WRITES_ENABLED=true`. Emite un token aparte o
vuelve a autorizar OAuth con «Crear reservas comisionadas» (`brokered:create`)
y `brokered:read`, `finance:read` y `contacts:read`. La integración debe incluir
la propiedad en su alcance comisionado; autorizar propiedades administradas no
concede acceso a las comisionadas. Actualizar el plugin no concede estos permisos.

## Retener o devolver tras cancelar

Después de cancelar, `cancelar_reserva` indica con `decision_de_pagos_pendiente`
si queda dinero cobrado por decidir (solo cuando el token lee importes).
`preparar_retencion_o_devolucion` sin `decision` describe la situación, y la
modalidad la decide el servidor:

- **`anfitrion`**: el anfitrión cobró los pagos. Puede retener todo lo cobrado
  o devolver una parte o todo, con fecha, medio de pago y, en una devolución
  parcial, la opción de retener el resto.
- **`canal`**: la plataforma manejó el pago. Solo se registra el neto que le
  liquidó al anfitrión (`monto_centavos` obligatorio).

Admite reservas canceladas o no presentadas de cualquier canal, importadas
incluidas. Las de grupo, las de un anfitrión externo, las de propiedades sin
finanzas y las que mezclan pagos del canal y del anfitrión se deciden en
Booked, igual que revocar o corregir una decisión ya registrada. Con la
decisión, la herramienta devuelve un resumen y una firma de un solo uso, válida
treinta minutos; `registrar_retencion_o_devolucion` recibe solo `firma` y
`confirmado: true` tras el sí explícito del anfitrión. No transfiere dinero:
anota lo que el anfitrión hizo. Si se pierde la respuesta, consulta
`ver_reserva` antes de preparar otra vez.

Primero debe desplegarse el [PR #579 del servidor](https://github.com/ruizbjaime/booked/pull/579)
y estar habilitado `INTEGRATION_WRITES_ENABLED=true`. Emite un token aparte o
vuelve a autorizar OAuth con «Retener o devolver pagos de cancelaciones»
(`bookings:settle_cancellation`) y `properties:read`, `bookings:read` y
`finance:read`. Actualizar el plugin no concede estos permisos.

## Editar, cambiar de estado y cobrar reservas

Cuatro flujos escriben sobre una reserva existente, cada uno con preparación,
resumen, firma de un solo uso (treinta minutos) y el sí explícito del
anfitrión; si la reserva cambió desde la preparación, no guardan nada:

- **Editar** (`preparar_edicion_de_reserva` → `editar_reserva`): fechas,
  ocupación, mascotas, notas, método de pago o responsable de una reserva no
  importada de Directo o del sitio público. Si cambia la estancia, el precio
  se recalcula con la configuración de hoy y se guarda el total mostrado.
- **Cambiar el estado** (`preparar_cambio_de_estado_de_reserva` →
  `cambiar_estado_de_reserva`): confirmar, volver a pendiente, no-show,
  reconfirmar, reactivar o reabrir, en cualquier canal. Cancelar sigue siendo
  `cancelar_reserva`; check-in y salida son automáticos.
- **Registrar un pago** (`preparar_pago_de_reserva` →
  `registrar_pago_de_reserva`): un pago que el anfitrión ya recibió, por
  segmento (depósito, saldo o total), con su recibo cuando el segmento queda
  pagado. Repetir la misma preparación no lo duplica.
- **Anular un pago o una devolución** (`preparar_anulacion_de_pago` →
  `anular_pago`): deshace, con motivo, un registro hecho por error y anula o
  reemite su recibo.

`cambios_por_revisar` lista los avisos que dejó la sincronización de
calendarios —fechas aplicadas o diferidas, cancelaciones, pagos por
conciliar— y `marcar_cambio_revisado` cierra uno tras confirmación explícita,
sin aplicar ni deshacer nada. Ninguno de estos flujos mueve dinero.

Emite un token aparte o vuelve a autorizar OAuth con «Editar reservas»
(`bookings:update`), «Cambiar el estado de reservas» (`bookings:transition`),
«Registrar pagos» (`bookings:register_payment`) o «Anular pagos»
(`bookings:void_payment`), con «Propiedades» y «Reservas»; los de pagos
exigen además «Importes y pagos».

## Conjuntos

Un conjunto son varias cabañas cercanas que se venden juntas. Solo existe
para una credencial que alcanza **todas** sus cabañas: con una fuera del
alcance de la integración, `ver_conjuntos` no lo muestra y ninguna herramienta
lo lee ni lo escribe.

- **Consultar:** `ver_conjuntos` y `ver_reserva_de_conjunto`.
- **Reservar sin cotización:** `cotizar_conjunto` propone el reparto más
  barato entre las cabañas libres, o cotiza el que dicte el anfitrión;
  `preparar_reserva_de_conjunto` recibe ese `reparto_para_cotizar` y pregunta
  huésped, método y compromiso de pago una sola vez; `crear_reserva_de_conjunto`,
  tras el sí, crea una reserva pendiente por cabaña, todas o ninguna.
- **Cotizar y convertir:** el mismo reparto va a `preparar_cotizacion` con
  `tipo_inventario: conjunto`; la cotización se gestiona con las herramientas
  de siempre.
- **Mover, cambiar de estado o cobrar:** `preparar_edicion_de_conjunto` →
  `editar_conjunto`, `preparar_cambio_de_estado_de_conjunto` →
  `cambiar_estado_de_conjunto` (cancelar incluido) y
  `preparar_pago_de_conjunto` → `registrar_pago_de_conjunto`, siempre para
  todas las cabañas a la vez, todo o nada.

Escribir requiere «Reservas de conjunto» (`groups:manage`) con «Propiedades»,
«Reservas» y «Cotizar estancias»; cobrar, además «Importes y pagos».
Retener o devolver lo cobrado de un conjunto cancelado, archivarlo y anular
sus pagos se hacen en Booked.

## Solicitudes del sitio y TRA/SIRE

`solicitudes` lista las solicitudes de reserva del sitio público con los datos
de quien las envió. `preparar_conversion_de_solicitud` →
`convertir_solicitud_en_cotizacion` crea, tras el sí, una cotización borrador
con los precios vigentes; `descartar_solicitud` la cierra para siempre tras
confirmación explícita. Leer requiere «Solicitudes del sitio»
(`inquiries:read`); escribir, «Gestionar solicitudes» (`inquiries:manage`) con
«Cotizaciones» (`quotations:read`).

`cumplimiento_tra_sire` dice qué falta reportar a la TRA o al SIRE por
propiedad y reserva, como estados y conteos: nunca nombres, documentos ni
nacionalidades. Requiere «Cumplimiento TRA/SIRE» (`compliance:read`).

Primero debe desplegarse el [PR #590 del servidor](https://github.com/ruizbjaime/booked/pull/590)
y, para escribir, estar habilitado `INTEGRATION_WRITES_ENABLED=true`.
Actualizar el plugin no concede estos permisos.

## Preguntas de análisis

Estas herramientas de solo lectura contestan preguntas sobre personas, patrones
y resultados sin paginar reservas ni sumar a mano:

| Herramienta | Contesta | Permisos |
| --- | --- | --- |
| `huespedes_recurrentes` | Quiénes repiten y, con `sin_volver_desde`, a quién reactivar | «Nombre del huésped» (`guests:read`) y «Reservas» (`bookings:read`) |
| `ver_huesped` | El historial de una persona | Igual |
| `analisis_de_huespedes` | Cuántos repiten, cuánto facturan y de dónde vienen | Igual |
| `patrones_de_reserva` | Anticipación, duración, grupo y cancelaciones por mes, canal o propiedad | «Reservas» |
| `huecos_de_ocupacion` | Noches sueltas entre ocupaciones, con festivos y puentes | «Disponibilidad» (`availability:read`) |
| `comparar_propiedades` | Ocupación, ADR y RevPAR por propiedad | «Propiedades y canales» (`properties:read`) y «Reservas» |
| `embudo_de_ventas` | Solicitudes → cotizaciones → reservas | «Cotizaciones» (`quotations:read`) |
| `estado_de_resultados` | Lo que dejó una propiedad o el conjunto, en devengo | «Importes y pagos» (`finance:read`) |
| `flujo_de_caja` | Lo que entró y salió, por fecha de pago | Igual |
| `obligaciones_por_pagar` | Lo que debe el anfitrión: gastos, nómina y comisiones | Igual |
| `ingresos_comprometidos` | Lo ya vendido por mes y el ritmo frente al año pasado | Igual |
| `comparativo_interanual` | Ingresos, ocupación y ADR por año | Igual |
| `gastos` | Los gastos causados, uno por uno, y quién asume cada parte: anfitrión, propietario o tercero | Igual |
| `gastos_de_nomina` | El costo de nómina por concepto, quién lo asume, propiedad y mes | Igual; por trabajador, además «Nómina por trabajador» (`payroll:read`) |
| `informe_financiero` | El informe del anfitrión o la liquidación de un propietario, con el detalle de cada línea y, si se pide, en Markdown | Igual; la nómina por trabajador, además `payroll:read` |
| `gastos_recurrentes` | Las plantillas de gasto fijo de cada propiedad y quién asumiría cada parte | «Importes y pagos» |
| `trabajadores` | Quién trabaja en cada propiedad, su contrato, salario vigente y vacaciones pendientes; sin documento, EPS, dirección ni teléfono | «Importes y pagos» y «Nómina por trabajador» (`payroll:read`) |
| `eventos_locales` | Ferias, festivales y fiestas del destino, con la estancia que el sitio propone | «Calendario» (`calendar:read`) |
| `cumplimiento_tra_sire` | Qué falta reportar a la TRA o al SIRE, en estados y conteos, nunca identidades | «Cumplimiento TRA/SIRE» (`compliance:read`) |

`deudas` añade la antigüedad de lo que le deben y las comisiones ya cobradas.
Teléfono, cumpleaños y origen de los huéspedes llegan solo con «Consultar
contactos» (`contacts:read`), y los importes de las herramientas de reservas y
huéspedes, con «Importes y pagos». La nómina viaja en totales y por concepto;
por trabajador, con su nombre, solo con «Nómina por trabajador»
(`payroll:read`), que exige «Importes y pagos» y se concede aparte. Los datos
de TRA/SIRE llegan solo como estados y conteos. `gastos` y `gastos_de_nomina` dicen quién asume cada
costo; `informe_financiero` entrega la cascada con su detalle y, con
`documento`, el informe en Markdown para entregar sin recalcular. Primero debe
desplegarse el [PR #583 del servidor](https://github.com/ruizbjaime/booked/pull/583),
y para las tres de costos e informes el [PR #589](https://github.com/ruizbjaime/booked/pull/589);
actualizar el plugin no concede permisos.

## Lectura y escritura

Sesenta y seis herramientas solo leen. `cotizar` y `cotizar_conjunto` calculan un
precio; no apartan fechas. `ver_reserva` trae además `detalle` (fechas,
cancelación, edades, pagos, devoluciones, recibos y su conjunto) y
`ver_propiedad`, `descripcion` (tipo, zona, amenidades, habitaciones y baños).

`ver_contactos` consulta la libreta del anfitrión con `contacts:read`: devuelve
nombre, teléfono, email, documento y notas disponibles. Ese permiso permite
leer toda su libreta, aunque algunas propiedades queden fuera de la lista
autorizada. Para buscar al responsable de una estancia por propiedad también
requiere `properties:read` y `bookings:read`, y sí respeta esa lista.

- «¿Cuál es el teléfono de María Pérez?» busca con `busqueda`; si hay varias
  coincidencias, pregunta cuál antes de atribuir datos.
- «Dame nombre y teléfono del huésped actual de Casita Artemisa» identifica la
  propiedad con `listar_propiedades` y consulta `ver_contactos` con
  `propiedad_id`; la fecha predeterminada es hoy.
- «¿Quién es el huésped principal de la reserva de Casita Artemisa para el
  25 de septiembre de 2026?» usa el mismo filtro y `fecha: "2026-09-25"`.
  La llegada está incluida y la salida excluida; no incluye canceladas ni
  no-show. Devuelve el responsable de la reserva, su estado y si se hospeda,
  no la lista de acompañantes. Una reserva pendiente o confirmada no prueba
  presencia física.

Veintiocho herramientas escriben, y cada una lleva su permiso en Booked:

| Herramienta | Permiso | Qué hace |
| --- | --- | --- |
| `crear_cotizacion` | Guardar cotizaciones (`quotations:create`) | Guarda un borrador tras preparar, presentar el resumen y recibir confirmación explícita; no reserva noches ni envía mensajes. |
| `cambiar_estado_de_cotizacion` | Cambiar el estado de cotizaciones (`quotations:transition`) | Marca una cotización como enviada, aceptada o rechazada, o la devuelve a borrador, tras preparar y confirmar; no envía nada al huésped. |
| `editar_cotizacion` | Editar cotizaciones (`quotations:update`) | Corrige un borrador tras preparar y confirmar, recalculando el precio como la ficha; no reserva noches. |
| `convertir_cotizacion_en_reserva` | Convertir cotizaciones en reservas (`quotations:convert`) | Convierte una cotización aceptada en una reserva pendiente con su precio tras preparar y confirmar; retiene las noches y no registra pagos. |
| `editar_propiedad` | Editar propiedades (`properties:update`) | Cambia nombre, ciudad, dirección, horarios o capacidad de una propiedad administrada tras preparar, mostrar antes y después y recibir confirmación explícita; no toca precios ni canales. |
| `sincronizar_calendarios` | Sincronizar calendarios (`blocks:sync`) | Importa ya los calendarios iCal de las plataformas, solo a petición; puede crear o quitar bloqueos importados y cambiar o cancelar reservas sincronizadas. El resultado se consulta con `estado_de_sincronizacion`. |
| `crear_bloqueo` | Crear bloqueos | Bloquea noches de una propiedad administrada. |
| `editar_bloqueo` | Editar bloqueos (`blocks:update`) | Cambia las fechas o las notas de un bloqueo manual tras mostrar cómo quedará y recibir confirmación explícita; si las fechas se cruzan con otra ocupación no cambia nada; nunca uno importado. |
| `eliminar_bloqueo` | Eliminar bloqueos | Borra un bloqueo manual tras explicar las consecuencias y recibir confirmación explícita; nunca uno importado. |
| `crear_reserva_manual` | Crear reservas manuales | Crea una reserva pendiente por Directo o el canal del sitio público, sin registrar pagos. |
| `crear_reserva_comisionada` | Crear reservas comisionadas (`brokered:create`) | Crea una reserva pendiente o confirmada en una propiedad comisionada tras preparar y confirmar huésped, estancia, importes y comisión; no registra pagos ni cobros de comisión. |
| `cancelar_reserva` | Cancelar reservas | Cancela una reserva directa o del sitio público, conservando su historial. |
| `eliminar_reserva` | Eliminar reservas | Archiva una reserva ya cancelada y sin retención. |
| `registrar_retencion_o_devolucion` | Retener o devolver pagos de cancelaciones (`bookings:settle_cancellation`) | Registra, tras preparar y confirmar, si el anfitrión retiene o devuelve lo cobrado de una reserva cancelada o no presentada, o el neto que liquidó el canal; no transfiere dinero. |
| `convertir_bloqueo_en_reserva` | Convertir bloqueos en reservas | Convierte en reserva un bloqueo importado de Airbnb, Booking.com o VRBO. |
| `editar_reserva` | Editar reservas (`bookings:update`) | Cambia fechas, ocupación, mascotas, notas, método de pago o responsable de una reserva no importada de Directo o del sitio público tras preparar y confirmar; re-precia con la configuración de hoy. |
| `marcar_cambio_revisado` | Editar reservas (`bookings:update`) | Cierra un aviso de `cambios_por_revisar` tras confirmación explícita; no aplica ni deshace el cambio. |
| `cambiar_estado_de_reserva` | Cambiar el estado de reservas (`bookings:transition`) | Confirma, devuelve a pendiente, marca no-show, reconfirma, reactiva o reabre una reserva de cualquier canal tras preparar y confirmar; no cancela ni hace check-in o salida. |
| `registrar_pago_de_reserva` | Registrar pagos (`bookings:register_payment`) | Registra un pago ya recibido en una reserva no importada de Directo o del sitio público tras preparar y confirmar; no mueve dinero. |
| `anular_pago` | Anular pagos (`bookings:void_payment`) | Anula, con motivo y tras preparar y confirmar, un pago o una devolución registrados por error y su recibo; no mueve dinero. |
| `crear_reserva_de_conjunto` | Reservas de conjunto (`groups:manage`) | Crea una reserva pendiente por cabaña de un conjunto, todas o ninguna, tras preparar y confirmar; no registra pagos. |
| `editar_conjunto` | Reservas de conjunto (`groups:manage`) | Mueve las fechas o cambia la ocupación de todas las cabañas de una estancia de conjunto a la vez, re-preciando cada una, tras preparar y confirmar. |
| `cambiar_estado_de_conjunto` | Reservas de conjunto (`groups:manage`) | Cambia el estado de todas las cabañas de un conjunto a la vez, cancelar incluido, todo o nada, tras preparar y confirmar. |
| `registrar_pago_de_conjunto` | Reservas de conjunto (`groups:manage`) | Registra un pago ya recibido por todo el conjunto, repartido entre sus cabañas, tras preparar y confirmar; no mueve dinero. |
| `convertir_solicitud_en_cotizacion` | Gestionar solicitudes (`inquiries:manage`) | Convierte una solicitud pendiente del sitio en una cotización borrador con los precios vigentes tras preparar y confirmar; no retiene noches ni envía nada. |
| `descartar_solicitud` | Gestionar solicitudes (`inquiries:manage`) | Descarta una solicitud pendiente tras confirmación explícita; es definitivo y borra después los datos de quien la envió. |
| `crear_contacto` | Crear contactos (`contacts:create`) | Crea un contacto con nombre y teléfono internacional proporcionados por el anfitrión; no crea una reserva. |
| `eliminar_contacto` | Eliminar contactos (`contacts:delete`) y Consultar contactos (`contacts:read`) | Prepara y, tras confirmación explícita, elimina un contacto que puede borrarse. |

Los bloqueos manuales y los contactos se crean con una petición explícita del
anfitrión y todos los datos necesarios. Ante datos incompletos o ambigüedad,
el agente pregunta antes de actuar. Crear contactos requiere `contacts:create`,
sin permisos de lectura acompañantes. Si se pierde la respuesta, no repitas la
creación a ciegas: puede duplicarla; consulta `ver_contactos` si dispones de
`contacts:read`.

**Toda eliminación exige una confirmación explícita posterior al resumen de
lo que se eliminará y sus consecuencias. La petición inicial no cuenta como
confirmación.** Para `eliminar_bloqueo`, el agente identifica el bloqueo manual,
muestra la propiedad, las fechas y las consecuencias, espera el sí y llama con
`confirmado: true`. Borrar el bloqueo no garantiza disponibilidad: pueden
existir otras reservas o bloqueos. Esta herramienta no tiene preparación con
firma, y `editar_bloqueo` sigue el mismo patrón: muestra el bloqueo como está y
como quedará, espera el sí y envía solo lo que cambia con `confirmado: true`.

`eliminar_contacto` usa la misma herramienta en dos etapas: primero solo
`contacto_id`, obtenido de `ver_contactos`, para recibir el resumen y la firma
sin borrar nada; después de mostrarlo y recibir el sí explícito, repite con el
mismo `contacto_id`, `firma` y `confirmado: true`. La firma está vinculada a la
credencial, caduca a los treinta minutos y no puede volver a usarse tras un
borrado exitoso. El servidor comprueba que los datos sigan iguales y rehúsa si
hay reservas sin archivar, cotizaciones, una cuenta de usuario o un comisionista
vinculados. Las reservas archivadas conservan su historial y pierden únicamente
la referencia al contacto eliminado. No se deben eliminar vínculos para forzar
el borrado. Si el resumen cambia o la firma caduca, vuelve a preparar y a pedir
confirmación.

Las reservas se preparan antes con una herramienta que no escribe
(`preparar_reserva_manual`, `preparar_reserva_comisionada`, `preparar_gestion_de_reserva`,
`preparar_retencion_o_devolucion`, `preparar_conversion_de_bloqueo`,
`preparar_conversion_de_cotizacion`, `preparar_edicion_de_reserva`,
`preparar_cambio_de_estado_de_reserva`, `preparar_pago_de_reserva`,
`preparar_anulacion_de_pago`, `preparar_reserva_de_conjunto`,
`preparar_edicion_de_conjunto`, `preparar_cambio_de_estado_de_conjunto`,
`preparar_pago_de_conjunto`, `preparar_conversion_de_solicitud`): devuelve un resumen y una firma de un solo
uso, válida hasta treinta minutos, y el agente solo ejecuta tras leer el resumen
y recibir el sí explícito del anfitrión. Cancelar y archivar una reserva son
acciones separadas, cada una con su propia preparación y confirmación.
Ninguna escritura mueve dinero: crear no registra pagos, cancelar o archivar
no reembolsa, y registrar o anular un pago, o una retención o devolución, solo
anota lo que hizo el anfitrión. `marcar_cambio_revisado` y
`descartar_solicitud` no llevan firma, pero sí la confirmación explícita con
`confirmado: true`.

La credencial es el interruptor, y los permisos de escritura solo se ofrecen
cuando la instalación tiene `INTEGRATION_WRITES_ENABLED=true`. Además del
permiso de escritura de cada herramienta, se exigen estas lecturas acompañantes:

| Herramienta | Lecturas acompañantes |
| --- | --- |
| `crear_cotizacion` | «Cotizaciones» (`quotations:read`); propias/administradas requieren `properties:read` y `pricing:read`; comisionadas requieren `brokered:read` y `finance:read`. Elegir un contacto o comisionista requiere `contacts:read`; crear un contacto nuevo requiere además la escritura `contacts:create`. |
| `cambiar_estado_de_cotizacion` | «Cotizaciones» (`quotations:read`); comisionadas requieren `brokered:read` y `finance:read`. |
| `editar_cotizacion` | «Cotizaciones» (`quotations:read`); administradas requieren `pricing:read`; comisionadas, `brokered:read` y `finance:read`. |
| `convertir_cotizacion_en_reserva` | «Cotizaciones» (`quotations:read`); una cotización antigua sin precio guardado requiere `pricing:read`; comisionadas, `brokered:read` y `finance:read`. |
| `editar_propiedad` | «Propiedades y canales» (`properties:read`). |
| `sincronizar_calendarios` | «Propiedades» (`properties:read`). |
| `crear_bloqueo` | «Propiedades» (`properties:read`). |
| `editar_bloqueo`, `eliminar_bloqueo` | «Propiedades» (`properties:read`) y «Bloqueos» (`blocks:read`). |
| `crear_reserva_manual` | «Propiedades» (`properties:read`) y «Cotizar estancias» (`pricing:read`). |
| `crear_reserva_comisionada` | «Reservas comisionadas» (`brokered:read`), «Importes y pagos» (`finance:read`) y «Consultar contactos» (`contacts:read`). |
| `cancelar_reserva`, `eliminar_reserva` | «Propiedades» (`properties:read`) y «Reservas» (`bookings:read`). |
| `registrar_retencion_o_devolucion` | «Propiedades» (`properties:read`), «Reservas» (`bookings:read`) e «Importes y pagos» (`finance:read`). |
| `convertir_bloqueo_en_reserva` | «Bloqueos» (`blocks:read`) y «Cotizar estancias» (`pricing:read`). |
| `editar_reserva`, `marcar_cambio_revisado`, `cambiar_estado_de_reserva` | «Propiedades» (`properties:read`) y «Reservas» (`bookings:read`). |
| `registrar_pago_de_reserva`, `anular_pago` | «Propiedades» (`properties:read`), «Reservas» (`bookings:read`) e «Importes y pagos» (`finance:read`). |
| `crear_reserva_de_conjunto`, `editar_conjunto`, `cambiar_estado_de_conjunto` | «Propiedades» (`properties:read`), «Reservas» (`bookings:read`) y «Cotizar estancias» (`pricing:read`). |
| `registrar_pago_de_conjunto` | Las tres anteriores e «Importes y pagos» (`finance:read`). |
| `convertir_solicitud_en_cotizacion`, `descartar_solicitud` | «Solicitudes del sitio» (`inquiries:read`) y «Cotizaciones» (`quotations:read`). |
| `crear_contacto` | Ninguna. |
| `eliminar_contacto` | «Consultar contactos» (`contacts:read`). |

Si Booked responde que la escritura por integraciones está apagada en la
instalación, el administrador debe revisar esa habilitación. Emitir otro token
o reconectar OAuth no resuelve ese caso; conserva el acceso de lectura.

- **Token manual (`booked`).** Con uno de solo lectura, el plugin no puede
  escribir. Para escribir desde aquí, emite **un token aparte** —no amplíes
  uno que ya use otro agente— con las lecturas y los permisos de escritura
  que quieras dar. Para usar los nuevos permisos de contactos, emite un token
  con los permisos necesarios y sus lecturas acompañantes; los tokens existentes
  no se amplían al actualizar el plugin.
- **OAuth (`booked-oauth`, `booked-chatgpt`).** Los permisos quedan fijados al
  autorizar. Una conexión anterior sigue con los permisos que tenía:
  desconecta y vuelve a conectar, y selecciona «Consultar contactos» en lectura y
  las acciones que necesites en el bloque de escritura de la pantalla de
  consentimiento, que nunca viene premarcado. Actualizar el plugin no añade
  permisos a la autorización. La autorización anterior de ese cliente se
  revoca sola.

## Licencia

[MIT](LICENSE).
