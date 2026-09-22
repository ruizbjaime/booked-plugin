- **«No se proporcionaron credenciales válidas»** (o cualquier respuesta de
  autenticación): el token del plugin está vacío, caducado o revocado. No
  reintentes ni busques otra herramienta; di que hay que emitir uno nuevo en
  *Booked → Ajustes → Integraciones API* y pegarlo en la configuración del
  plugin.
- **Al token le falta un permiso de escritura, o las escrituras no están
  disponibles:** dilo así, nombrando la acción que faltó, y no insistas. Hace
  falta un token aparte, emitido en *Booked → Ajustes → Integraciones API*,
  que lleve el permiso de esa acción: «Crear bloqueos», «Eliminar bloqueos»,
  «Crear reservas manuales», «Cancelar reservas», «Eliminar reservas» o
  «Convertir bloqueos en reservas».
- **`caduca` a menos de siete días** (lo devuelve `alcance_del_token`): avísalo
  al final de la respuesta, una sola vez por conversación, con la fecha.
