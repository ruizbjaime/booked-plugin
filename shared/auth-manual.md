- **«No se proporcionaron credenciales válidas»** (o cualquier respuesta de
  autenticación): el token del plugin está vacío, caducado o revocado. No
  reintentes ni busques otra herramienta; di que hay que emitir uno nuevo en
  *Booked → Ajustes → Integraciones API* y pegarlo en la configuración del
  plugin.
- **Al token le falta el permiso de convertir, o las escrituras no están
  disponibles:** dilo así y no insistas. Hace falta un token aparte que lleve
  «Convertir bloqueos en reservas», emitido en *Booked → Ajustes →
  Integraciones API*.
- **`caduca` a menos de siete días** (lo devuelve `alcance_del_token`): avísalo
  al final de la respuesta, una sola vez por conversación, con la fecha.
