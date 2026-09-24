# Distribución pública de aplicaciones

Esta carpeta contiene únicamente metadatos ligeros de distribución. Los binarios no se guardan en el historial Git.

Plataformas previstas:
- Windows: Release fija `windows-public`, asset estable `BrotesDeOlivo-Setup.exe`.
- macOS: Release fija `macos-public`, asset estable `BrotesDeOlivo-macOS.dmg`.
- Android: Release fija `android-public`, asset estable `BrotesDeOlivo-Android.apk`.
- iOS/iPadOS: enlace de App Store o TestFlight cuando exista.

`manifest.json` es el contrato consumido por la web. Una plataforma solo se habilita cuando `available` es `true`.
