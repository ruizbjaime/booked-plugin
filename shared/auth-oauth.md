- **Error de autenticación:** solicita volver a conectar Booked mediante OAuth
  desde el cliente. No pidas contraseñas ni tokens en el chat. El inicio de
  sesión y el consentimiento ocurren en Booked.
- **La autorización OAuth no caduca por tiempo.** El cliente renueva sus
  accesos automáticamente. Se revoca desde *Booked → Ajustes → Integraciones
  API*. Si `caduca` es `null`, no anuncies una caducidad de 30 días ni pidas
  emitir un token manual.
