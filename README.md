# Booked para Claude y ChatGPT

Los paquetes conectan al servidor MCP de
[Booked](https://booked.fincasdelavilla.com) —veintinueve herramientas sobre
propiedades, reservas, calendario y dinero, seis de ellas de escritura— e
incluyen una skill con las reglas de negocio que no caben en la descripción de
una herramienta.

Este repositorio incluye el *marketplace* de Claude y los paquetes para ambas
plataformas. Claude se instala por URL; ChatGPT requiere registrar su conexión
y generar el paquete con ese identificador. Las publicaciones siguen el
[versionado](#versionado) de los manifiestos.


## Paquetes

| Paquete | Plataforma | Autenticación |
| --- | --- | --- |
| `booked` | Claude Code / Cowork, instalaciones existentes | Token manual, máximo 30 días |
| `booked-oauth` | Claude Code / Cowork | Inicio de sesión en Booked, OAuth |
| `booked-chatgpt` | ChatGPT; manifiesto compatible con Codex | Inicio de sesión en Booked, OAuth |

Instala una sola variante de Booked en cada cliente para evitar herramientas
repetidas. Las reglas de negocio se mantienen en `shared/booked-fincas.md` y
se generan con `python3 scripts/sync-skills.py`. No edites las copias generadas.

**Estado:** OAuth requiere desplegar la rama `feat/mcp-oauth` del backend.
Estos archivos preparan los paquetes; no registran ni publican una app en ChatGPT.

## Instalar con OAuth

El administrador debe completar primero [la configuración del backend](#preparar-el-backend).

En Booked, crea una integración en **Ajustes → Integraciones API** y selecciona
las propiedades administradas y comisionadas que quieres compartir. No necesitas
emitir un token manual. Durante la vinculación, escoge esa integración y marca
los permisos de lectura y, si quieres escribir desde el cliente, los de escritura. La pantalla muestra el alcance antes de autorizar.

### Claude

Añade el marketplace `ruizbjaime/booked-plugin` e instala **Booked — conexión con
OAuth**. En Claude Code:

```bash
claude plugin marketplace add ruizbjaime/booked-plugin
claude plugin install booked-oauth@booked
```

Abre `/mcp` y completa la autenticación de Booked en el navegador. En Claude /
Cowork también puedes añadir un conector remoto con la URL
`https://booked.fincasdelavilla.com/mcp/oauth` y completar la vinculación.
El servidor admite registro dinámico de clientes para los retornos permitidos.

### ChatGPT

1. Activa el modo desarrollador si está disponible en tu cuenta o espacio.
2. Registra una conexión MCP con
   `https://booked.fincasdelavilla.com/mcp/oauth`, autenticación OAuth y registro
   dinámico. Inicia sesión en Booked y autoriza el alcance.
3. Copia el ID técnico de la conexión real (`plugin_asdk_app_…`).
4. Genera el paquete con esa conexión. El directorio de salida debe ser nuevo,
   llamarse `booked-chatgpt` y quedar fuera de `plugins/booked-chatgpt`, incluso
   si se accede a él mediante un enlace simbólico:

```bash
python3 scripts/configure-chatgpt.py --app-id ID_REAL --output /tmp/booked-chatgpt
```

El script crea `.app.json` y enlaza el manifiesto a la conexión registrada.
El paquete fuente mantiene `.mcp.json` para clientes que aceptan MCP directo;
ChatGPT necesita el registro de la conexión. Instala el paquete generado por
la vía de plugins disponible en tu espacio; el marketplace de Claude no se
instala directamente en ChatGPT. La publicación pública es un paso separado.
Consulta la [documentación oficial de empaquetado](https://developers.openai.com/plugins/build/plugins).

### Caducidad y revocación

- **Token manual:** máximo 30 días, como antes.
- **OAuth:** autorización sin vencimiento temporal; accesos de 15 minutos y
  credenciales de renovación rotatorias sin caducidad temporal.
- Revoca el registro **OAuth …** desde la ficha de la integración en Booked
  para bloquear tanto consultas como renovaciones. Desactivar la integración
  o al anfitrión también bloquea el acceso. Quitar un plugin del cliente no
  sustituye la revocación en Booked.
- La contraseña se introduce únicamente en Booked. Ningún paquete guarda
  contraseñas, secretos de cliente ni tokens de usuario en el repositorio.

## Preparar el backend

En el repositorio de la aplicación, con la rama OAuth revisada:

1. Instala las dependencias bloqueadas con `composer install` y aplica las
   migraciones mediante el procedimiento de despliegue habitual.
2. Genera las claves con `php artisan passport:keys` **solo si aún no existen**.
   Conserva las claves entre despliegues y protege también `APP_KEY`: cambiar
   esas claves invalida credenciales existentes. Nunca las subas a Git.
3. Configura `APP_URL` con el origen HTTPS del panel y habilita
   `INTEGRATION_OAUTH_ENABLED=true`. Reconstruye la caché de configuración.
4. Verifica que el proxy admite `/mcp/oauth`, `/oauth/authorize`, `/oauth/token`,
   `/oauth/register` y `/.well-known/oauth-*` en el dominio del panel.
5. Verifica descubrimiento, consentimiento y consulta con una cuenta de prueba
   en Claude y otra en ChatGPT antes de distribuir la versión.

El registro dinámico permite HTTPS en `chatgpt.com`, `chat.openai.com`,
`claude.ai` y `claude.com`, y retornos locales de Claude Code. Las URI exactas
quedan fijadas en cada cliente registrado; no se admiten fragmentos ni credenciales
embebidas. Los límites de solicitudes también cubren el registro y los canjes.

Para revertir la habilitación, establece `INTEGRATION_OAUTH_ENABLED=false`:
la entrada histórica `/mcp` con Sanctum sigue funcionando. Antes de revertir
migraciones, revoca las autorizaciones OAuth; la migración también las invalida
al recuperar la columna de caducidad obligatoria.

## Desarrollo y validación

```bash
python3 scripts/sync-skills.py
python3 scripts/validate.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Las versiones de los tres paquetes y las entradas del marketplace de Claude
se publican coordinadas. CI exige el catálogo completo, versiones coincidentes,
la configuración de autenticación y rutas válidas a las skills y conexiones,
tanto en la fuente como en el paquete generado. También comprueba que las
skills coincidan con su fuente y ejecuta las pruebas de regresión en copias
temporales. La versión del servidor MCP sigue siendo independiente.

Las comprobaciones Python no requieren red y se ejecutan antes de instalar
Claude Code. CI fija Claude Code en `2.1.278`, la versión usada para validar
estos paquetes; actualiza esa versión de forma explícita al comprobar
compatibilidad con una nueva versión del cliente.

## Instalar la variante con token en Cowork

1. **Customize → Plugins → Add marketplace** y pega `ruizbjaime/booked-plugin`.
2. Instala **Booked** desde ese marketplace.
3. Cuando pida el **token de la integración**, pega el tuyo. Se emite en
   *Booked → Ajustes → Integraciones API* y se muestra una sola vez. El token
   decide lo que el plugin puede hacer: mira [Lectura y escritura](#lectura-y-escritura).

Para actualizar: **Update** en el marketplace.

## Instalar la variante con token en Claude Code

```bash
claude plugin marketplace add ruizbjaime/booked-plugin
claude plugin install booked@booked
```

## El token manual caduca a los 30 días

Es el techo que impone Booked a todo token de integración, y no se puede alargar
desde el plugin. Cuando el plugin conteste que no hay credenciales válidas, el
token está vacío, caducado o revocado — las tres se arreglan igual:

1. En *Booked → Ajustes → Integraciones API*, revoca el token viejo si sigue
   listado (su nombre queda reservado mientras no se revoque, aunque haya
   caducado) y emite uno nuevo con las mismas capacidades.
2. Pega el nuevo en la configuración del plugin: en Cowork, desde la ficha del
   plugin en **Customize → Plugins**; en Claude Code, desde el gestor `/plugin`.
   El almacenamiento depende del cliente y del sistema. Claude Code usa el
   llavero de macOS cuando está disponible; si falla o no hay un llavero
   compatible, usa `~/.claude/.credentials.json`. `sensitive: true` oculta el
   valor y evita guardarlo en `settings.json`, pero no garantiza un llavero en
   todas las plataformas. Consulta la
   [referencia de configuración de Claude](https://code.claude.com/docs/en/plugins-reference#user-configuration).

La herramienta `alcance_del_token` devuelve `caduca`; la skill le pide al
modelo que avise cuando falte menos de una semana.

## Versionado

Cada publicación sube `version` en los manifiestos de los tres paquetes y en
las entradas del marketplace de Claude, y lleva un tag `vX.Y.Z`. CI comprueba
que las versiones coincidan. La versión de los paquetes es independiente de
la del servidor MCP (`#[Version]` en `BookedServer`). El detalle de cada versión
está en [CHANGELOG.md](CHANGELOG.md).

## Qué hay dentro

```
shared/                          # la fuente de las skills: edita aquí, no las copias
├── booked-fincas.md             # las reglas de la respuesta: dinero, ids, alcance
├── auth-manual.md               # qué decir cuando falla el token manual
└── auth-oauth.md                # qué decir cuando falla la autorización OAuth
scripts/
├── sync-skills.py               # genera cada SKILL.md desde shared/ (--check en CI)
├── validate.py                  # versiones, conexiones y skills al día
└── configure-chatgpt.py         # empaqueta ChatGPT con el ID de su conexión
plugins/booked/                  # Claude, token manual
├── .claude-plugin/plugin.json   # identidad y el token que se pide al instalar
├── .mcp.json                    # el conector HTTP a /mcp, con el bearer en la cabecera
└── skills/booked-fincas/        # generada
plugins/booked-oauth/            # Claude, OAuth
├── .claude-plugin/plugin.json   # identidad; no pide token
├── .mcp.json                    # el conector HTTP a /mcp/oauth, sin cabeceras
└── skills/booked-fincas/        # generada
plugins/booked-chatgpt/          # ChatGPT, OAuth
├── .codex-plugin/plugin.json    # manifiesto OpenAI
├── .mcp.json                    # /mcp/oauth; el paquete generado lo cambia por .app.json
└── skills/booked-fincas/        # generada
```

En `booked`, el token viaja como `Authorization: Bearer` hacia
`https://booked.fincasdelavilla.com/mcp`. El cliente gestiona su almacenamiento
con `sensitive: true`, según lo explicado arriba; el paquete no lo guarda en
este repositorio. Los paquetes OAuth no llevan credenciales: el cliente las
obtiene al vincularse con
`https://booked.fincasdelavilla.com/mcp/oauth`. El servidor vive en el repo de
la aplicación, en `app/Mcp/`, y la puerta remota se monta en `routes/ai.php`.

## Lectura y escritura

Veintitrés herramientas solo leen. `cotizar` calcula un precio; no aparta fechas.

Seis escriben, y cada una lleva su permiso en Booked:

| Herramienta | Permiso | Qué hace |
| --- | --- | --- |
| `crear_bloqueo` | Crear bloqueos | Bloquea noches de una propiedad administrada. |
| `eliminar_bloqueo` | Eliminar bloqueos | Borra un bloqueo manual; nunca uno importado. |
| `crear_reserva_manual` | Crear reservas manuales | Crea una reserva pendiente por Directo o el canal del sitio público, sin registrar pagos. |
| `cancelar_reserva` | Cancelar reservas | Cancela una reserva directa o del sitio público, conservando su historial. |
| `eliminar_reserva` | Eliminar reservas | Archiva una reserva ya cancelada y sin retención. |
| `convertir_bloqueo_en_reserva` | Convertir bloqueos en reservas | Convierte en reserva un bloqueo importado de Airbnb, Booking.com o VRBO. |

Los bloqueos manuales se crean o eliminan con una petición explícita del
anfitrión y todos los datos completos. Estas dos herramientas no tienen una
preparación con firma ni una segunda confirmación; ante datos incompletos o
ambigüedad, el agente pregunta antes de actuar.

Las reservas se preparan antes con una herramienta que no escribe
(`preparar_reserva_manual`, `preparar_gestion_de_reserva`,
`preparar_conversion_de_bloqueo`): devuelve un resumen y una firma de un solo
intento, válida treinta minutos, y el agente solo ejecuta tras leer el resumen
y recibir el sí explícito del anfitrión. Ninguna escritura mueve dinero:
crear no registra pagos y cancelar o archivar no reembolsa.

La credencial es el interruptor, y los permisos de escritura solo se ofrecen
cuando la instalación tiene `INTEGRATION_WRITES_ENABLED=true`. Cada permiso
exige además sus lecturas acompañantes: «Propiedades» para todos, «Bloqueos»
para eliminar bloqueos y convertirlos, «Reservas» para cancelar y eliminar
reservas, y «Cotizar estancias» para crear reservas y convertir bloqueos.

Si Booked responde que la escritura por integraciones está apagada en la
instalación, el administrador debe revisar esa habilitación. Emitir otro token
o reconectar OAuth no resuelve ese caso; conserva el acceso de lectura.

- **Token manual (`booked`).** Con uno de solo lectura, el plugin no puede
  escribir. Para escribir desde aquí, emite **un token aparte** —no amplíes
  uno que ya use otro agente— con las lecturas y los permisos de escritura
  que quieras dar.
- **OAuth (`booked-oauth`, `booked-chatgpt`).** Los permisos quedan fijados al
  autorizar. Una conexión anterior sigue con los permisos que tenía:
  desconecta y vuelve a conectar, y marca los permisos en el bloque de
  escritura de la pantalla de consentimiento, que nunca viene premarcado. La
  autorización anterior de ese cliente se revoca sola.

## Licencia

[MIT](LICENSE).
