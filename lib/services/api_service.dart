class ApiService {
  Future<String> sendMessage(String message) async {
    await Future.delayed(const Duration(seconds: 1));
    return "Recibí tu mensaje: \"$message\". Soy OpenCode Mobile, una app de chat preparada para conectarse a una API.";
  }
}
