# Cambios

Cada versión publicada actualiza los manifiestos de los tres paquetes y las
entradas del marketplace de Claude, y lleva un tag `vX.Y.Z`.

## 0.22.0 — 2026-11-12

- La skill enseña a mantener o recalcular el precio al corregir una reserva.
  Cuando `preparar_edicion_de_reserva` cambia la ocupación o las mascotas sin
  mover las fechas y los precios de esa reserva cambiaron desde que se
  reservó, la preparación no firma y `faltan` trae `campo: precio` con una
  pregunta y sus cifras (total actual y con los precios de hoy, lo que vale
  la corrección sola y, cuando difieren, comisión de la plataforma y pago al
  anfitrión; sin «Importes y pagos», sin cifras). La skill se la lee entera
  al anfitrión y vuelve a preparar con `precio: recalcular` o
  `precio: mantener`; nunca elige por él ni envía `precio` sin que se pida.
  `mantener` no toca el dinero y un cargo aparte se añade a mano en Booked.
  Si la corrección no se puede recalcular hoy, la pregunta ofrece solo
  mantener, con el motivo. Requiere el
  [PR #884](https://github.com/ruizbjaime/booked/pull/884) de Booked.
- Una reserva completada, cancelada o no-show tiene el precio cerrado: la
  skill sabe que corregir su ocupación no pregunta ni toca el dinero, que
  llega un solo aviso y que sus fechas no se mueven (una cancelada se
  reactiva primero). El rechazo de las fechas llega en `errores`.
- `preparar_edicion_de_conjunto` hace la misma pregunta al cambiar solo la
  ocupación: una por guardado, que nombra las cabañas cuyos precios cambiaron
  y da el total del conjunto si se recalcula y si se mantiene; las demás
  cabañas se calculan como siempre.
- Si `editar_reserva` o `editar_conjunto` responden que cambió —también
  porque los precios se movieron entre preparar y confirmar—, la skill
  prepara de nuevo sin `precio` y repite la pregunta.
- La skill recoge además que una reserva con importes declarados los conserva
  al corregir la ocupación, con su aviso
  ([PR #883](https://github.com/ruizbjaime/booked/pull/883)).

## 0.21.0 — 2026-11-11

- La skill enseña el gasto de mano de obra ocasional: cada gasto de `gastos`
  trae `tipo` (`general` o `mano_de_obra_ocasional`) y, en el segundo,
  `persona` con su `tipo` (`trabajador_ocasional` o `trabajador` de la
  nómina), `id` y `nombre`. Un gasto general lleva `persona: null`. Con `id`
  y `nombre` en `null` falta un permiso: del anfitrión en Booked para ver a
  esa persona o, si es de nómina, «Nómina por trabajador» (`payroll:read`) en
  la credencial; la skill dice el tipo de persona sin adivinar quién. `gastos`
  no filtra por tipo ni por persona, así que lo pagado a alguien se suma
  sobre sus gastos listados (`pagado_centavos`, o `monto_centavos` para lo
  causado) y, con `truncado`, se acotan las fechas o se sube `limite`. Un
  trabajador ocasional no sale en `trabajadores` ni en `gastos_de_nomina`, y
  el trabajo puntual pagado a uno de la nómina sale solo en `gastos`; la
  ficha de un ocasional y los gastos se registran en el panel de Booked.
  Requiere los [PR #879](https://github.com/ruizbjaime/booked/pull/879) y
  [#880](https://github.com/ruizbjaime/booked/pull/880) de Booked.
- `preparar_edicion_de_conjunto` ya no prepara un cambio de fechas cuando una
  cabaña que sigue en la estancia tiene el check-in hecho o la estancia
  terminada: lo devuelve en `impedimentos`, nombrando las cabañas, sin firma.
  La skill deja de prometer «nuevas fechas para todas las cabañas» sin esa
  condición: lee el impedimento, recuerda que la ocupación sí se cambia
  preparando sin fechas y que una cabaña sola va por
  `preparar_edicion_de_reserva`, y vuelve a preparar si `editar_conjunto`
  rechaza porque una cabaña entró en estancia entretanto.
  Requiere el [PR #878](https://github.com/ruizbjaime/booked/pull/878).
- Sin herramientas ni permisos nuevos: siguen siendo ciento seis, treinta y
  tres de escritura.

## 0.20.0 — 2026-11-11

- La skill enseña a retener lo cobrado de un conjunto cancelado con la pareja
  de siempre, `preparar_retencion_o_devolucion` →
  `registrar_retencion_o_devolucion`: el `reserva_id` de cualquier cabaña
  responde por el conjunto entero, con `situacion_conjunto` sin `decision` y
  `resumen_conjunto` con `decision: retener`. Solo se retiene todo lo
  retenible de las cabañas canceladas, sin monto parcial ni `retener_resto`;
  devolver lo de un conjunto sigue registrándose en Booked. Registrar exige
  además «Reservas de conjunto» (`groups:manage`): sin él, la preparación
  devuelve el resumen con un aviso y sin firma, y la skill no intenta
  registrar. En la respuesta, `retenido` es lo de esta operación y el detalle
  por cabaña y el total retenido van en `conjunto`. Tras cancelar un conjunto
  con pagos, la skill ofrece registrar la retención en vez de mandar todo a
  Booked. Requiere el
  [PR #875](https://github.com/ruizbjaime/booked/pull/875) de Booked.
- `ver_cotizaciones` trae en la cabecera de una cotización de conjunto
  `cabanas_con_cupo_excepcional`: cuántas de sus cabañas, dentro del token,
  llevan cupo excepcional, para saberlo desde el listado. Requiere el
  [PR #872](https://github.com/ruizbjaime/booked/pull/872).
- La descripción de la skill baja de 1.144 a menos de 1.024 caracteres, el
  límite de algunos clientes, y su lista inicial de escrituras ya nombra
  convertir una solicitud del sitio directo en reserva.
- Sin herramientas nuevas: siguen siendo ciento seis, treinta y tres de
  escritura. Retener un conjunto usa permisos que ya existían
  (`bookings:settle_cancellation` y `groups:manage`); una credencial que no
  los tenga juntos debe volver a autorizarse para hacerlo.

## 0.19.0 — 2026-11-11

- La skill enseña el cupo excepcional: alojar en una cotización de una
  propiedad administrada o de un conjunto más huéspedes que la capacidad
  publicada. `cupo_excepcional: true` en `preparar_cotizacion` y
  `preparar_edicion_de_cotizacion` solo se envía si el anfitrión lo pide
  expresamente, tras leerle `cupo_excepcional_disponible` (o
  `cupo_excepcional_disponible_por_cabana`) con huéspedes, capacidad publicada
  y tope; si el aviso dice que no es posible, no se ofrece. El tope es la
  capacidad más 2 o más el 25 %, lo que sea mayor; niños e infantes siguen
  estrictos, y en un conjunto un solo acuse vale para todas las cabañas
  excedidas, todo o nada. `ver_cotizaciones`, `ver_reserva`,
  `ver_reserva_de_conjunto` y las preparaciones de conversión y de edición de
  reserva traen `cupo_excepcional` mientras siga sobre la capacidad
  publicada. Una reserva solo lo hereda al convertir la cotización: `cotizar`,
  `cotizar_conjunto`, las reservas directas y las solicitudes del sitio siguen
  estrictos. Requiere los
  [PR #864](https://github.com/ruizbjaime/booked/pull/864),
  [#865](https://github.com/ruizbjaime/booked/pull/865) y
  [#866](https://github.com/ruizbjaime/booked/pull/866) de Booked.
- Una cotización de conjunto en borrador ya cambia de fechas y de reparto con
  `preparar_edicion_de_cotizacion` → `editar_cotizacion`: `entrada`,
  `salida`, `cabanas` —el reparto completo que dicta el anfitrión; sin él se
  conserva el guardado— y `notas`. Re-precia todas las cabañas con las
  tarifas vigentes y la vigencia la pone Booked, renovada si ya venció. La
  skill deja de decir que de un conjunto solo se editan las notas. Requiere
  los [PR #867](https://github.com/ruizbjaime/booked/pull/867),
  [#868](https://github.com/ruizbjaime/booked/pull/868) y
  [#869](https://github.com/ruizbjaime/booked/pull/869).
- El marketplace y el README vuelven a contar ciento seis herramientas. Sin
  herramientas ni permisos nuevos: ninguna credencial necesita volver a
  autorizar.

## 0.18.0 — 2026-11-09

- Convertir una solicitud del sitio directo en reserva ya vale también para un
  conjunto de varias cabañas: crea una reserva pendiente por cabaña, todas o
  ninguna, con `reserva.cabanas` en la vista previa y `reserva_conjunto_id` y
  `reservas` en la respuesta. La skill deja de decir que un conjunto se
  convierte en cotización. Requiere el
  [PR #820](https://github.com/ruizbjaime/booked/pull/820) de Booked.
- Al convertir un bloqueo en reserva, la skill enseña `recibido_centavos`: lo
  que paga la plataforma («Ganas» en Airbnb) en vez de lo que pagó el
  huésped, uno de los dos y nunca ambos. Requiere el
  [PR #855](https://github.com/ruizbjaime/booked/pull/855).
- Las cotizaciones administradas de Directo traen `oferta_publica`: el enlace a
  la ficha del sitio público y, si el sitio cotiza más caro, el precio del
  sitio y el descuento. Llega en el detalle de `ver_cotizaciones` y en las
  respuestas de `crear_cotizacion` y `editar_cotizacion`; en las
  preparaciones es una previsión. Requiere los
  [PR #858](https://github.com/ruizbjaime/booked/pull/858) y
  [#859](https://github.com/ruizbjaime/booked/pull/859).
- `ver_reserva_de_conjunto` trae `por_resolver` y `retenido` de las cabañas
  canceladas con dinero cobrado; la skill enseña que no son pagado ni saldo a
  favor. Requiere los [PR #838](https://github.com/ruizbjaime/booked/pull/838)
  y [#839](https://github.com/ruizbjaime/booked/pull/839).
- Los manifiestos vuelven a contar bien el catálogo: 106 herramientas, 73 de
  lectura y 33 de escritura. Sin herramientas ni permisos nuevos: ninguna
  credencial necesita volver a autorizar.

## 0.17.0 — 2026-11-04

- Añade la conversión directa de una solicitud del sitio en reserva en los
  tres paquetes (`preparar_conversion_de_solicitud_en_reserva` →
  `convertir_solicitud_en_reserva`): para el huésped que ya acordó por
  teléfono o WhatsApp, sin cotización que enviar. Solo una propiedad o un
  conjunto resuelto en una cabaña, con llegada futura; pregunta precio,
  estadía mínima, método y compromiso de pago y un teléfono si falta, y crea
  la cotización, la acepta y la convierte, todo o nada. Exige además «Cambiar
  el estado de cotizaciones» (`quotations:transition`) y «Convertir
  cotizaciones en reservas» (`quotations:convert`).
- Las dos conversiones de solicitudes muestran el precio que vio el huésped y
  el de hoy, y preguntan `precio` cuando difieren; la skill enseña que esa
  elección es de Jaime. Sus firmas ya no cruzan la medianoche.
- El catálogo pasa a 106 herramientas: 73 de lectura y 33 de escritura.
  Requiere desplegar el [PR #818](https://github.com/ruizbjaime/booked/pull/818)
  de Booked.

## 0.16.0 — 2026-11-02

- Añade `conceder_compensatorio` en los tres paquetes: concede el día libre
  que paga un descanso obligatorio trabajado, en dos llamadas con firma, con
  el permiso «Registrar descansos» (`payroll:rest_days`). La skill enseña que
  el `descanso_trabajado` es el `descanso.fecha` de `descansos_de_contrato`,
  que el día libre lo dice Jaime y nunca es el descanso obligatorio de su
  semana ni un festivo, que un día antes o después del `plazo` es `tardio` y
  solo se concede con `acepta_tardio` tras su sí, y que `ya_estaba_concedido`
  reconoce un compensatorio ya concedido tras una respuesta perdida. Deja de
  decir que conceder el compensatorio se hace en Booked; revocarlo sí.
- El catálogo pasa a 104 herramientas: 72 de lectura y 32 de escritura. Las
  credenciales con «Registrar descansos» ya pueden conceder compensatorios sin
  volver a autorizar. Requiere desplegar el
  [PR #804](https://github.com/ruizbjaime/booked/pull/804) de Booked.

## 0.15.0 — 2026-11-02

- Añade nueve herramientas en los tres paquetes. Agregar acompañantes a una
  reserva de cualquier canal (`preparar_acompanantes_de_reserva` →
  `agregar_acompanantes_a_reserva`, permiso nuevo «Agregar acompañantes»,
  `guests:write`), todos o ninguno, sin devolver sus datos. Mover las fechas
  límite de pago de una reserva o de un conjunto entero
  (`preparar_cambio_de_plazos_de_pago` → `cambiar_plazos_de_pago`, con
  «Registrar pagos»). Consultar y marcar el descanso semanal de un trabajador
  (`descansos_de_contrato` y `marcar_dia_de_descanso`, permiso nuevo
  «Registrar descansos», `payroll:rest_days`): la skill enseña que el descanso
  obligatorio es el domingo salvo pacto escrito, que el día libre entre semana
  es el compensatorio y que si lo trabajó sale de sus horas. Leer
  `liquidacion_del_propietario` (el extracto mensual en PDF, cada estancia
  entera en el mes en que empieza), `proyeccion` (semana a semana desde hoy,
  con puentes libres) y `posibles_duplicados`.
- `editar_bloqueo`, `eliminar_bloqueo` y `descartar_solicitud` se preparan con
  una primera llamada sin firma y se confirman con la firma y
  `confirmado: true`; la skill y el README ya no dicen que no llevan firma.
- Registrar un pago vale en cualquier canal con compromiso de pago en Booked,
  también en una reserva convertida desde iCal, y las notas de una reserva se
  editan en cualquier canal.
- `ver_contactos` y `posibles_duplicados` traen documento y notas solo con
  «Nombre del huésped» (`guests:read`); `flujo_de_caja` cuenta solo la parte
  del anfitrión, con los payouts de plataforma el día del check-in;
  `trabajadores` trae el `descanso` vigente.
- Las guías de autenticación nombran los permisos de escritura de reservas,
  pagos, acompañantes y descansos que faltaban.
- El catálogo pasa a 103 herramientas: 72 de lectura y 31 de escritura. Las
  credenciales existentes no ganan permisos al actualizar. Todo lo que
  documenta ya está desplegado en Booked (PR #673, #674, #676, #707, #766 y
  #792, entre otros).

## 0.14.0 — 2026-10-02

- Registrar un pago, de reserva o de conjunto, es recuperable: la preparación
  devuelve un `operacion_id` y, si la respuesta se pierde, se prepara de nuevo
  con ese mismo id para recuperar el pago ya registrado (`repetido: true`) en
  vez de duplicarlo. Un pago distinto se prepara sin `operacion_id`, aunque
  tenga el mismo importe; si ya hay un pago vivo igual, la preparación lo
  avisa. La skill deja de decir que repetir la preparación no duplica el pago.
- `listar_propiedades_comisionadas` busca por parte del nombre (`busqueda`) y
  pagina con `despues_id` / `siguiente_id`.
- `estado_de_sincronizacion` informa `propiedades_sin_sincronizar`, y
  `vencida` cubre también una sincronización incompleta o sin respuesta.

## 0.13.0 — 2026-09-24

- Añade las reservas de conjunto en los tres paquetes: `ver_conjuntos`,
  `ver_reserva_de_conjunto` y `cotizar_conjunto`, y reservar un conjunto
  directo con `preparar_reserva_de_conjunto` → `crear_reserva_de_conjunto`
  (una reserva pendiente por cabaña, todas o ninguna). Moverlo, cambiar su
  estado —cancelar incluido— o cobrarlo se prepara y confirma para todas sus
  cabañas a la vez (`editar_conjunto`, `cambiar_estado_de_conjunto`,
  `registrar_pago_de_conjunto`). Permiso «Reservas de conjunto»
  (`groups:manage`) con «Propiedades», «Reservas» y «Cotizar estancias». La
  skill enseña que un conjunto solo existe para el token si alcanza todas sus
  cabañas.
- Una cabaña de conjunto se edita o cambia de estado sola solo si el token
  alcanza el conjunto entero, y las cabañas canceladas o no-show quedan fuera
  de mover el conjunto y de cambiar su estado en vez de bloquearlo.
- Las cotizaciones de conjunto funcionan con las herramientas de siempre:
  `preparar_cotizacion` con `tipo_inventario: conjunto` y el
  `reparto_para_cotizar` de `cotizar_conjunto`, `crear_cotizacion`,
  `ver_cotizaciones`, `editar_cotizacion` (solo notas) y
  `convertir_cotizacion_en_reserva`. La skill ya no dice que se gestionan en
  Booked.
- Añade cuatro flujos sobre una reserva existente, cada uno con preparación,
  firma y confirmación explícita: editarla (`editar_reserva`,
  `bookings:update`), cambiar su estado (`cambiar_estado_de_reserva`,
  `bookings:transition`), registrar un pago ya recibido
  (`registrar_pago_de_reserva`, `bookings:register_payment`) y anular un pago
  o una devolución registrados por error (`anular_pago`,
  `bookings:void_payment`). Ninguno mueve dinero; los de pagos exigen
  «Importes y pagos».
- Añade `cambios_por_revisar` y `marcar_cambio_revisado` para los avisos que
  deja la sincronización de calendarios; cerrar un aviso no aplica ni deshace
  nada.
- Añade `solicitudes`, `preparar_conversion_de_solicitud` →
  `convertir_solicitud_en_cotizacion` y `descartar_solicitud`, con los
  permisos «Solicitudes del sitio» (`inquiries:read`) y «Gestionar
  solicitudes» (`inquiries:manage`).
- Añade `cumplimiento_tra_sire` («Cumplimiento TRA/SIRE», `compliance:read`):
  qué falta reportar, en estados y conteos, nunca identidades. La skill ya no
  dice que TRA/SIRE no llega por ninguna herramienta.
- Añade `trabajadores` (con `payroll:read`), `gastos_recurrentes` y
  `eventos_locales`. `ver_reserva` trae `detalle` y `ver_propiedad`,
  `descripcion`.
- El catálogo pasa a 94 herramientas: 66 de lectura y 28 de escritura. Las
  credenciales existentes no ganan permisos al actualizar.
- Requiere desplegar primero el PR [#590](https://github.com/ruizbjaime/booked/pull/590)
  de Booked. Las tres skills se regeneran desde la fuente compartida.

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
