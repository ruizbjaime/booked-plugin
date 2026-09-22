# Cambios

Cada versión publicada actualiza los manifiestos de los tres paquetes y las
entradas del marketplace de Claude, y lleva un tag `vX.Y.Z`.

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
