- **Error de autenticación:** solicita volver a conectar Booked mediante OAuth
  desde el cliente. No pidas contraseñas ni tokens en el chat. El inicio de
  sesión y el consentimiento ocurren en Booked.
- **«La escritura por integraciones está apagada en esta instalación»:**
  pide que el administrador revise la habilitación de escrituras en Booked.
  Reconectar OAuth no activa esa función; conserva la conexión de lectura.
- **A la autorización le falta `contacts:read`:** no significa que el contacto
  no exista. Vuelve a autorizar Booked seleccionando «Consultar contactos» en
  los permisos de lectura; permite consultar toda la libreta del anfitrión.
  Para buscar al responsable por propiedad y fecha selecciona además
  «Propiedades» y «Reservas». Actualizar el plugin no amplía permisos existentes.
- **A la autorización le falta un permiso de escritura:** dilo así, nombrando
  la acción que faltó, y no insistas.
  Los permisos se fijan al autorizar: hay que desconectar Booked, volver a
  conectarlo y marcar en la pantalla de consentimiento el permiso de esa
  acción: «Guardar cotizaciones», «Crear bloqueos», «Eliminar bloqueos»,
  «Crear reservas manuales», «Crear reservas comisionadas», «Cancelar reservas»,
  «Eliminar reservas», «Retener o devolver pagos de cancelaciones»,
  «Convertir bloqueos en reservas», «Crear contactos» o «Eliminar contactos».
  Este último requiere también «Consultar contactos» en los permisos de
  lectura. Para «Retener o devolver pagos de cancelaciones»
  (`bookings:settle_cancellation`), selecciona además «Propiedades»,
  «Reservas» e «Importes y pagos». Para «Crear reservas
  comisionadas» (`brokered:create`), selecciona además «Reservas comisionadas»,
  «Importes y pagos» y «Consultar contactos» al volver a autorizar.
- **La autorización OAuth no caduca por tiempo.** El cliente renueva sus
  accesos automáticamente. Se revoca desde *Booked → Ajustes → Integraciones
  API*. Si `caduca` es `null`, no anuncies una caducidad de 30 días ni pidas
  emitir un token manual.
