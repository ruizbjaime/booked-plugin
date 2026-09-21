# Plugin de Booked para Claude Cowork y Claude Code

Un solo plugin, `booked`: el conector al servidor MCP de
[Booked](https://booked.fincasdelavilla.com) —diecinueve herramientas de solo
lectura sobre propiedades, reservas, calendario y dinero— y una skill con las
reglas de negocio que no caben en la descripción de una herramienta.

Este repositorio es a la vez el *marketplace* y el plugin, así que se instala
por URL y se actualiza con un `git push`.

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
