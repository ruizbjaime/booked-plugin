# Plugin de Booked para Claude Cowork y Claude Code

Un solo plugin, `booked`: el conector al servidor MCP de
[Booked](https://booked.fincasdelavilla.com) —diecinueve herramientas de solo
lectura sobre propiedades, reservas, calendario y dinero— y una skill con las
reglas de negocio que no caben en la descripción de una herramienta.

Este repositorio es a la vez el *marketplace* y el plugin, así que se instala
por URL. Se actualiza subiendo la versión: un `git push` sin subir `version`
no llega a nadie (ver [Versionado](#versionado)).

## Instalar en Cowork

1. **Customize → Plugins → Add marketplace** y pega `ruizbjaime/booked-plugin`.
2. Instala **Booked** desde ese marketplace.
3. Cuando pida el **token de la integración**, pega el de solo lectura. Se emite
   en *Booked → Ajustes → Integraciones API* y se muestra una sola vez.

Para actualizar: **Update** en el marketplace.

## Instalar en Claude Code

```bash
claude plugin marketplace add ruizbjaime/booked-plugin
claude plugin install booked@booked
```

## El token caduca a los 30 días

Es el techo que impone Booked a todo token de integración, y no se puede alargar
desde el plugin. Cuando el plugin conteste que no hay credenciales válidas, el
token está vacío, caducado o revocado — las tres se arreglan igual:

1. En *Booked → Ajustes → Integraciones API*, revoca el token viejo si sigue
   listado (su nombre queda reservado mientras no se revoque, aunque haya
   caducado) y emite uno nuevo con las mismas capacidades.
2. Pega el nuevo en la configuración del plugin: en Cowork, desde la ficha del
   plugin en **Customize → Plugins**; en Claude Code, desde el gestor `/plugin`.
   El valor se guarda en el almacén seguro del sistema, nunca en un archivo del
   proyecto.

La herramienta `alcance_del_token` devuelve `caduca`; la skill le pide al
modelo que avise cuando falte menos de una semana.

## Versionado

Cada cambio publicado sube `version` en los dos manifiestos —
`plugins/booked/.claude-plugin/plugin.json` y `.claude-plugin/marketplace.json`,
tienen que coincidir y CI lo comprueba — y lleva un tag `vX.Y.Z`. La versión del
plugin es independiente de la del servidor MCP (`#[Version]` en `BookedServer`):
coinciden hoy por casualidad, no por contrato. El detalle de cada versión está
en [CHANGELOG.md](CHANGELOG.md).

## Qué hay dentro

```
plugins/booked/
├── .claude-plugin/plugin.json   # identidad y el token que se pide al instalar
├── .mcp.json                    # el conector HTTP, con el bearer en la cabecera
└── skills/booked-fincas/        # las reglas de la respuesta: dinero, ids, alcance
```

El token viaja como `Authorization: Bearer` hacia `https://booked.fincasdelavilla.com/mcp`
y se guarda en el almacén seguro del sistema (`sensitive: true`), nunca en este
repositorio. El servidor vive en el repo de la aplicación, en `app/Mcp/`, y la
puerta remota se monta en `routes/ai.php`.

## Solo lectura

Ninguna herramienta escribe. `cotizar` calcula un precio; no aparta fechas.

## Licencia

[MIT](LICENSE).
