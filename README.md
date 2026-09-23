# Brotes de Olivo Music - Repositorio musical

Repositorio oficial para el catálogo y la distribución de contenidos musicales utilizados por las aplicaciones de Brotes de Olivo Music.

## Distribución de los archivos musicales

Los archivos musicales se distribuirán mediante **GitHub Releases**. No deben subirse directamente al historial Git del repositorio.

Los formatos multimedia están excluidos mediante `.gitignore` para evitar que archivos pesados como MP3, MP4, M4A, WAV, FLAC, AAC u OGG formen parte del historial normal de Git.

## Catálogo

El archivo [`catalogo.json`](catalogo.json) es el catálogo utilizado por las aplicaciones. Su estructura se valida con [`schema/catalogo.schema.json`](schema/catalogo.schema.json).

Cada cambio enviado a la rama `main`, o propuesto mediante una pull request dirigida a `main`, ejecuta una validación automática del catálogo con GitHub Actions.

## Derechos sobre las obras

El acceso público a este repositorio y a sus archivos no concede ninguna licencia de uso, copia, modificación, distribución ni reutilización de las obras musicales. Todos los derechos sobre las obras y grabaciones pertenecen a sus respectivos titulares.
