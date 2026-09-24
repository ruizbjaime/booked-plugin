# Cambios

Cada versión publicada actualiza los manifiestos de los tres paquetes y las
entradas del marketplace de Claude, y lleva un tag `vX.Y.Z`.

## 0.12.0 — 2026-09-23

- Añade `gastos`, `gastos_de_nomina` e `informe_financiero` en los tres
  paquetes: los gastos causados con quién asume cada parte (anfitrión,
  propietario o tercero), el costo de nómina por concepto, propiedad y mes, y
  el informe del anfitrión o la liquidación de un propietario con el detalle
  de cada línea y, si se pide, en Markdown. La skill dice que el filtro por
  quién asume suma solo su parte mientras lo pagado es del gasto entero, que
  el documento se entrega sin recalcular y qué significan `detalle_oculto` y
  `completo`.
- Documenta el permiso «Nómina por trabajador» (`payroll:read`), que exige
  «Importes y pagos»: sin él la nómina sigue en totales y por concepto. La
  skill ya no dice que la nómina por trabajador no llega por ninguna
  herramienta.
- Añade `preparar_edicion_de_propiedad` → `editar_propiedad`: nombre, ciudad,
  dirección, horarios y capacidad de una propiedad administrada, con resumen
  antes y después, firma y confirmación explícita. Permiso «Editar
  propiedades» (`properties:update`) con «Propiedades y canales».
- Añade `sincronizar_calendarios` y `estado_de_sincronizacion`: importar ya
  los iCal de las plataformas, solo a petición, y ver cómo terminó. Permiso
  «Sincronizar calendarios» (`blocks:sync`) con «Propiedades».
- El catálogo pasa a 65 herramientas: 48 de lectura y 17 de escritura. Las
  credenciales existentes no ganan permisos al actualizar.
- Requiere desplegar primero los PR [#587](https://github.com/ruizbjaime/booked/pull/587),
  [#588](https://github.com/ruizbjaime/booked/pull/588) y
  [#589](https://github.com/ruizbjaime/booked/pull/589) de Booked. Las tres
  skills se regeneran desde la fuente compartida.

## 0.11.0 — 2026-09-23

- Añade `editar_bloqueo` en los tres paquetes: cambia las fechas o las notas
  de un bloqueo manual con la misma identificación y confirmación explícita
  que `eliminar_bloqueo`, enviando solo lo que cambia. Es todo o nada: si las
  fechas nuevas se cruzan con otra ocupación, tampoco se guardan las notas.
  Devuelve el bloqueo antes y después; la skill pide confirmar con esa
  respuesta y avisar si otra persona lo cambió entretanto.
- `ver_bloqueos`, `bloqueos_por_convertir` y `preparar_conversion_de_bloqueo`
  traen las notas del bloqueo; la skill las usa para explicar la razón.
- El catálogo pasa a 58 herramientas: 43 de lectura y 15 de escritura.
  Documenta `blocks:update` («Editar bloqueos») y sus lecturas acompañantes
  `properties:read` y `blocks:read`. Las credenciales existentes no ganan
  permisos al actualizar.
- Requiere desplegar primero los PR [#585](https://github.com/ruizbjaime/booked/pull/585)
  y [#586](https://github.com/ruizbjaime/booked/pull/586) de Booked. Las tres
  skills se regeneran desde la fuente compartida.

## 0.10.1 — 2026-09-23

- En las herramientas de huéspedes, las reservas de la misma persona con
  fechas pegadas o superpuestas cuentan como una sola visita; la skill lo dice
  en la regla de qué es una «estancia». Una noche libre en medio sigue
  separando dos visitas.
- Requiere desplegar el [PR #584 de Booked](https://github.com/ruizbjaime/booked/pull/584).
  Las tres skills se regeneran desde la fuente compartida.

## 0.10.0 — 2026-09-23

- Añade las preguntas de análisis en los tres paquetes: huéspedes
  (`huespedes_recurrentes`, `ver_huesped`, `analisis_de_huespedes`),
  reservas y propiedades (`patrones_de_reserva`, `huecos_de_ocupacion`,
  `comparar_propiedades`, `embudo_de_ventas`) y finanzas
  (`estado_de_resultados`, `flujo_de_caja`, `obligaciones_por_pagar`,
  `ingresos_comprometidos`, `comparativo_interanual`); `deudas` añade la
  antigüedad y las comisiones cobradas.
- La skill lleva cada pregunta típica a su herramienta y fija lo que ninguna
  descripción dice sola: devengo y caja no cuadran por diseño, «estancia» no
  cuenta lo mismo en huéspedes que en reservas, un contacto duplicado es otra
  persona, y qué permiso falta cuando no llegan datos de contacto o importes.
- El catálogo pasa a 57 herramientas: 43 de lectura y 14 de escritura. No hay
  permisos nuevos; las credenciales existentes no ganan permisos al
  actualizar.
- Requiere desplegar primero el [PR #583 de Booked](https://github.com/ruizbjaime/booked/pull/583).
  Las tres skills se regeneran desde la fuente compartida.

## 0.9.0 — 2026-09-23

- Añade la gestión de cotizaciones en los tres paquetes: `ver_cotizaciones`
  para listar o ver el detalle, y tres flujos preparar → confirmar resumen →
  escribir: cambiar el estado (`cambiar_estado_de_cotizacion`), editar un
  borrador (`editar_cotizacion`) y convertir una aceptada en reserva
  (`convertir_cotizacion_en_reserva`).
- La skill explica que «enviar» solo registra el envío, que rechazar es
  definitivo, que editar re-precia a la fecha de hoy salvo las notas, qué
  pregunta la conversión y que ante una respuesta perdida se consulta
  `ver_cotizaciones`, que también sustituye la verificación en el panel al
  guardar una cotización.
- El catálogo pasa a 45 herramientas: 31 de lectura y 14 de escritura.
  Documenta `quotations:transition`, `quotations:update` y
  `quotations:convert` y sus lecturas acompañantes. Las credenciales
  existentes no ganan permisos al actualizar.
- Requiere desplegar primero el [PR #581 de Booked](https://github.com/ruizbjaime/booked/pull/581).
  Las tres skills se regeneran desde la fuente compartida.

## 0.8.0 — 2026-09-22

- Añade el flujo `preparar_retencion_o_devolucion` → confirmar resumen →
  `registrar_retencion_o_devolucion` en los tres paquetes: tras cancelar, el
  anfitrión decide si retiene o devuelve lo cobrado, o registra el neto que
  liquidó el canal. La modalidad la decide el servidor y nada transfiere
  dinero.
- La skill ya no dice que los reembolsos se hacen solo en Booked, lee
  `decision_de_pagos_pendiente` al cancelar y manda a la aplicación los casos
  que el MCP rehúsa (grupos, anfitrión externo, pagos mezclados, revocaciones).
- El catálogo pasa a 38 herramientas: 27 de lectura y 11 de escritura.
  Documenta `bookings:settle_cancellation` y sus lecturas acompañantes
  `properties:read`, `bookings:read` y `finance:read`. Las credenciales
  existentes no ganan permisos al actualizar.
- Requiere desplegar primero el [PR #579 de Booked](https://github.com/ruizbjaime/booked/pull/579).
  Las tres skills se regeneran desde la fuente compartida.

## 0.7.0 — 2026-09-22

- Añade el flujo `preparar_reserva_comisionada` → confirmar resumen →
  `crear_reserva_comisionada` en los tres paquetes, con contacto existente,
  estado elegido, cargos y comisión declarados por el anfitrión.
- El catálogo pasa a 36 herramientas: 26 de lectura y 10 de escritura. La
  disponibilidad comisionada solo refleja lo registrado en Booked; no se
  registran pagos ni cobros de comisión.
- Documenta `brokered:create` y sus lecturas acompañantes `brokered:read`,
  `finance:read` y `contacts:read`, el alcance comisionado y la renovación de
  credenciales. Las conexiones existentes no ganan permisos al actualizar.
- Requiere desplegar primero el [PR #576 de Booked](https://github.com/ruizbjaime/booked/pull/576).
  Las tres skills se regeneran desde la fuente compartida.

## 0.6.0 — 2026-09-22

- Preparación guiada y guardado confirmado de cotizaciones para propiedades
  propias, administradas y comisionadas; teléfono opcional, elecciones del host
  y permisos condicionales, sin ocupar fechas ni registrar pagos o envíos.
- El catálogo pasa a 34 herramientas: 25 de lectura y 9 de escritura.
- Las tres skills se regeneran desde la fuente compartida. Requiere desplegar
  primero el soporte del PR #575 de Booked; actualizar el plugin no despliega
  el backend ni amplía los permisos de las credenciales existentes.
- El diálogo explica los permisos faltantes, las comisiones en porcentaje y
  los límites de confirmación. Conserva el resumen de lectura cuando no puede
  guardar, y pide volver a preparar si no puede emitirse una firma válida.

## 0.5.0 — 2026-09-22

- El catálogo pasa a treinta y dos herramientas: veinticuatro de lectura y
  ocho de escritura. Se incorporan `ver_contactos`, `crear_contacto` y
  `eliminar_contacto` a las reglas compartidas de los tres paquetes.
- La skill permite consultar datos personales autorizados: teléfono por
  contacto y responsable de una estancia por propiedad y fecha, con hoy como
  valor predeterminado. Explica la diferencia entre titular y huésped alojado.
- Toda eliminación exige explicar las consecuencias y recibir un sí explícito
  posterior. Los contactos se preparan y confirman con la misma herramienta y
  una firma de treinta minutos vinculada a la credencial; los bloqueos manuales
  requieren `confirmado: true`, sin firma.
- Se documentan el alcance de toda la libreta de `contacts:read`, las lecturas
  y la lista de propiedades exigidas para buscar por estancia, y los permisos
  independientes de creación y eliminación. Las credenciales existentes no
  ganan permisos: hay que emitir un token o volver a autorizar OAuth.
- Requiere desplegar primero el soporte MCP del PR #574 de Booked. Se conservan
  las URLs de los conectores y las variantes de autenticación; actualizar el
  plugin no despliega el backend ni publica las aplicaciones.

## 0.4.1 — 2026-09-22

- La validación exige el catálogo completo, versiones coordinadas,
  autenticación manual obligatoria y sensible, y rutas válidas en los paquetes
  fuente y generado. Las pruebas cubren las configuraciones rotas que antes
  pasaban CI.
- El empaquetador rechaza salidas dentro de su fuente, incluidos enlaces
  simbólicos, y evita dejar un paquete incompleto si falla la construcción.
- La skill distingue escritura deshabilitada de permiso faltante y aclara
  cómo presentar cálculos en centavos sin convertir dos veces un importe.
- Los manifiestos y la documentación distinguen la petición de un bloqueo de
  la preparación y confirmación de una reserva, y explican el almacenamiento
  real de credenciales según el cliente.
- CI ejecuta primero las comprobaciones Python y las pruebas de regresión,
  fija Claude Code en `2.1.278` y limita los permisos a lectura del repositorio.

## 0.4.0 — 2026-09-21

- El servidor pasa a veintinueve herramientas y seis escriben: además de
  convertir bloqueos, ahora crear y eliminar bloqueos manuales, y crear,
  cancelar y archivar reservas directas o del sitio público.
- La skill enseña el contrato de las escrituras de reservas —preparar, leer el
  resumen, esperar el sí explícito, ejecutar con la firma— y que cancelar y
  archivar son dos confirmaciones separadas.
- Los avisos de permiso faltante nombran la acción y el permiso exacto de
  Booked, en la variante manual y en las OAuth.
- Requiere desplegar primero Booked con las reservas manuales y la gestión de
  reservas por MCP, y `INTEGRATION_WRITES_ENABLED=true`; sin eso, los paquetes
  siguen leyendo igual.

## 0.3.0 — 2026-09-21

- El servidor pasa a veintidós herramientas y una escribe:
  `convertir_bloqueo_en_reserva`. La skill deja de decir «solo lectura» y
  enseña el flujo listar → preparar → preguntar lo que falta → confirmar →
  convertir, sin inventar ningún dato.
- La regla de datos personales se acota: al convertir un bloqueo, los datos del
  huésped se le preguntan al anfitrión.
- La credencial decide si se puede escribir: un token aparte en `booked`, o
  volver a autorizar marcando el permiso en los paquetes OAuth.
- Requiere desplegar primero Booked con la conversión de bloqueos y
  `INTEGRATION_WRITES_ENABLED=true`; sin eso, los paquetes siguen leyendo igual.

## 0.2.0 — 2026-09-21

- Paquete `booked-oauth` para Claude y `booked-chatgpt` para OpenAI, con
  conexión al mismo `/mcp/oauth` y autorización revocable sin caducidad fija.
- Se conserva `booked` con token manual y su límite de 30 días.
- Reglas de negocio compartidas y generación comprobada en CI.
- Script para empaquetar ChatGPT con el ID real de su conexión registrada.
- Requiere desplegar primero el soporte OAuth de Booked; no basta actualizar
  el marketplace.

## 0.1.1 — 2026-09-21

- El token pasa a ser obligatorio al instalar: antes se podía dejar vacío y cada
  llamada contestaba «credenciales» sin decir por qué.
- La skill dice qué hacer ante un token caducado o revocado, ante un límite de
  peticiones, y avisa cuando al token le queda menos de una semana.
- README: el token caduca a los 30 días y cómo renovarlo; regla de versionado.
- Licencia MIT, `homepage`, CHANGELOG y validación del plugin en CI.

## 0.1.0 — 2026-09-21

- Primera versión: el conector HTTP al MCP de Booked y la skill `booked-fincas`.
