# Cambios

Cada versión publicada sube `version` en `plugins/booked/.claude-plugin/plugin.json`
y en `.claude-plugin/marketplace.json`, y lleva un tag `vX.Y.Z`. Un push sin
subir la versión no llega a nadie: el plugin queda anclado a la versión que
declara y los clientes lo cachean por ella.

## 0.1.1 — 2026-09-21

- El token pasa a ser obligatorio al instalar: antes se podía dejar vacío y cada
  llamada contestaba «credenciales» sin decir por qué.
- La skill dice qué hacer ante un token caducado o revocado, ante un límite de
  peticiones, y avisa cuando al token le queda menos de una semana.
- README: el token caduca a los 30 días y cómo renovarlo; regla de versionado.
- Licencia MIT, `homepage`, CHANGELOG y validación del plugin en CI.

## 0.1.0 — 2026-09-21

- Primera versión: el conector HTTP al MCP de Booked y la skill `booked-fincas`.
