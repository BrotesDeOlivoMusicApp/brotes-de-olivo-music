# Histórico estadístico GitHub — Brotes de Olivo

Esta rama `github-statistics` **solo almacena datos**. No es rama de desarrollo
ni de publicación. Los archivos de la aplicación y las bases de datos incluidos
al crear esta rama son una copia inicial de `main`; no se modifican aquí.

Cada día, el workflow `.github/workflows/github-statistics.yml` de `main`
guarda `snapshots/AAAA-MM/AAAA-MM-DD.json` (días en UTC).

## Qué contiene cada archivo

- Metadatos del repositorio: estrellas, forks, tamaño y actividad general.
- Releases y activos: identificador estable, nombre, fecha, tamaño y contador
  **acumulado** de descargas que publica GitHub.
- Ejecuciones recientes de GitHub Actions y su estado.
- Existencia, tamaño y SHA del blob Git para determinados manifiestos y bases
  de datos; un cambio de SHA no significa necesariamente una descarga.
- Visitas, clones, procedencias y rutas populares de los últimos 14 días
  **solo si** está configurado el secreto opcional `GITHUB_STATS_TRAFFIC_TOKEN`
  con permiso `Administration: read` para este repositorio.
- `errors` y estados explícitos cuando la fuente no está disponible.

## Límites

GitHub no facilita contadores de acceso para archivos `raw`, `contents`,
GitHub Pages ni peticiones a una SQLite descargada mediante esas URLs.
Por tanto, **no se deducen descargas de BD de visitas, SHA o clones**.
Tampoco se equiparan descargas de Releases con instalaciones o personas únicas.
Los contadores de Releases pueden incluir descargas de prueba o automatizadas;
los activos eliminados dejan de consultarse, pero sus snapshots anteriores
permanecen en el histórico.

La actualización diaria no ejecuta compilaciones ni despliegues. Se puede
ejecutar manualmente desde Actions > Registrar estadisticas GitHub > Run workflow.
No se deben borrar los snapshots aunque se limpien runs de Actions.

## Android y Google Play (12/10/2026)

La distribución oficial de Android se realiza mediante **Google Play**.
Las estadísticas de descargas de APK/AAB y de las Releases `android-*`
no se capturan a partir de este cambio: pertenecen a Play Console.
El capturador filtra esas Releases y también los archivos `.apk` y `.aab`
en cualquier otra Release. **No se elimina ningún instalador del repositorio.**

Las capturas de instalación y la línea base anteriores a esta regla
pueden contener contadores históricos de APK/AAB; son datos técnicos y
se excluyen de los informes oficiales. El reinicio oficial de todos
los indicadores a partir del 13/10/2026 se gestionará de forma separada.
