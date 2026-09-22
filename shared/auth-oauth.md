- **Error de autenticación:** solicita volver a conectar Booked mediante OAuth
  desde el cliente. No pidas contraseñas ni tokens en el chat. El inicio de
  sesión y el consentimiento ocurren en Booked.
- **«La escritura por integraciones está apagada en esta instalación»:**
  pide que el administrador revise la habilitación de escrituras en Booked.
  Reconectar OAuth no activa esa función; conserva la conexión de lectura.
- **A la autorización le falta un permiso de escritura:** dilo así, nombrando
  la acción que faltó, y no insistas.
  Los permisos se fijan al autorizar: hay que desconectar Booked, volver a
  conectarlo y marcar en la pantalla de consentimiento el permiso de esa
  acción: «Crear bloqueos», «Eliminar bloqueos», «Crear reservas manuales»,
  «Cancelar reservas», «Eliminar reservas» o «Convertir bloqueos en reservas».
- **La autorización OAuth no caduca por tiempo.** El cliente renueva sus
  accesos automáticamente. Se revoca desde *Booked → Ajustes → Integraciones
  API*. Si `caduca` es `null`, no anuncies una caducidad de 30 días ni pidas
  emitir un token manual.
