# Cambios

Cada versión publicada actualiza los manifiestos de los tres paquetes y las
entradas del marketplace de Claude, y lleva un tag `vX.Y.Z`.

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
