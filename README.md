# OpenCode Mobile

Aplicación de chat Flutter preparada para conectarse a una API HTTP.

## Requisitos

- [Flutter SDK](https://flutter.dev/docs/get-started/install) (>=3.0.0)
- Android Studio o herramienta类似 con SDK Android 34
- Java 17 (para compilar Android)

## Configuración inicial

1. Asegúrate de tener Flutter instalado y en el PATH:

```bash
flutter --version
```

2. Ve al directorio del proyecto:

```bash
cd opencode_mobile
```

3. Obtén las dependencias:

```bash
flutter pub get
```

4. Genera el archivo `local.properties` con la ruta del SDK de Android:

```bash
flutter config --android-sdk <ruta-a-tu-sdk>
```

O créalo manualmente en `android/local.properties`:

```properties
sdk.dir=C:\\Users\\TuUsuario\\AppData\\Local\\Android\\Sdk
flutter.sdk=C:\\Users\\TuUsuario\\flutter
```

## Compilar APK

### APK de depuración (debug)

```bash
flutter build apk --debug
```

El APK se generará en: `build/app/outputs/flutter-apk/app-debug.apk`

### APK de publicación (release)

```bash
flutter build apk --release
```

El APK se generará en: `build/app/outputs/flutter-apk/app-release.apk`

### APK dividido por arquitectura

```bash
flutter build apk --split-per-abi --release
```

Genera APKs separados para arm64-v8a, armeabi-v7a y x86_64 en:
`build/app/outputs/flutter-apk/`

## Ejecutar en dispositivo

```bash
flutter run
```

## Conexión con API

La aplicación está preparada para conectarse a una API HTTP en `http://10.0.2.2:8000/api/chat`.
Edita `lib/services/api_service.dart` para cambiar la URL base según tu backend.
