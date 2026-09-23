- **«No se proporcionaron credenciales válidas»** (o cualquier respuesta de
  autenticación): el token del plugin está vacío, caducado o revocado. No
  reintentes ni busques otra herramienta; di que hay que emitir uno nuevo en
  *Booked → Ajustes → Integraciones API* y pegarlo en la configuración del
  plugin.
- **«La escritura por integraciones está apagada en esta instalación»:**
  pide que el administrador revise la habilitación de escrituras en Booked.
  Emitir otro token no activa esa función; conserva el acceso de lectura.
- **Al token le falta `contacts:read`:** no significa que el contacto no exista.
  Para consultar teléfonos y otros datos, hace falta un token con «Consultar
  contactos», que abarca la libreta completa del anfitrión. Para buscar al
  responsable por propiedad y fecha necesita también «Propiedades» y «Reservas».
- **Al token le falta otro permiso de lectura** —«Importes y pagos», «Nombre
  del huésped», «Disponibilidad»—: hace falta un token que lo lleve, emitido en
  *Booked → Ajustes → Integraciones API*.
- **Al token le falta un permiso de escritura:** dilo así, nombrando la acción
  que faltó, y no insistas. Hace falta un token aparte, emitido en
  *Booked → Ajustes → Integraciones API*, que lleve el permiso de esa acción:
  «Guardar cotizaciones», «Cambiar el estado de cotizaciones», «Editar
  cotizaciones», «Convertir cotizaciones en reservas», «Crear bloqueos»,
  «Editar bloqueos», «Eliminar bloqueos», «Crear reservas manuales», «Crear reservas
  comisionadas», «Cancelar reservas»,
  «Eliminar reservas», «Retener o devolver pagos de cancelaciones»,
  «Convertir bloqueos en reservas», «Crear contactos» o «Eliminar contactos».
  «Eliminar contactos» requiere además «Consultar contactos».
  «Retener o devolver pagos de cancelaciones» (`bookings:settle_cancellation`)
  requiere «Propiedades», «Reservas» e «Importes y pagos».
  «Crear reservas comisionadas» (`brokered:create`) requiere «Reservas
  comisionadas», «Importes y pagos» y «Consultar contactos». Los permisos de
  cotizaciones requieren «Cotizaciones»; editar una administrada o convertir
  una antigua sin precio guardado, también «Cotizar estancias». Actualizar el
  plugin no amplía los permisos del token existente.
- **`caduca` a menos de siete días** (lo devuelve `alcance_del_token`): avísalo
  al final de la respuesta, una sola vez por conversación, con la fecha.
