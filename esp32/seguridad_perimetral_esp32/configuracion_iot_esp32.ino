#include <WiFi.h>
#include <PubSubClient.h>

// 1. CONFIGURACIÓN DE RED Y BROKER (Ajustar en el Laboratorio)
const char* WIFI_SSID = "JPOLPC 3633";
const char* WIFI_PASSWORD = "819Wd!07";

// IP de tu laptop asignada por el Hotspot del teléfono
const char* MQTT_BROKER = "192.168.137.1";
const int MQTT_PORT = 1883;
const char* CLIENT_ID = "ESP32_Perimetro_Seguro_Jpol22"; 

// Tópicos del proyecto
const char* TOPIC_ALERTA = "seguridad/alertamovimiento";
const char* TOPIC_CONFIRMACION = "seguridad/confirmacionvision";

// 2. CONFIGURACIÓN DE HARDWARE (Mapeo de Pines GPIO)
const int PIN_LED_VERDE = 12;
const int PIN_LED_ROJO = 14;
const int PIN_LED_AMARILLO = 27;
const int PIN_SIMULADOR_PIR = 13;

// Variables globales estructurales
unsigned long ultimoDisparo = 0;
WiFiClient espClient; 
PubSubClient client(espClient);

// 3. SUBRUTINA DE CONEXIÓN WIFI
void conectar_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Buscando red WiFi e iniciando enlace de hardware...");

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    int intentos = 0;
    while (WiFi.status() != WL_CONNECTED && intentos < 20) {
        delay(500); 
        Serial.print(".");
        intentos++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[ÉXITO] Capa física conectada al router.");
        Serial.print("Dirección IP asignada por DHCP al ESP32: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\n[ERROR] Tiempo de espera agotado. Verifica el SSID/Contraseña.");
    }
}

// 4. FUNCIÓN CALLBACK (Recepción de Mensajes JSON desde la Laptop)
void al_recibir_mensaje(char* topic, byte* payload, unsigned int length) {
    Serial.print("\n[Broker] Mensaje entrante en tópico: ");
    Serial.println(topic);

    // Convertimos el payload de bytes a un String de C++ manejable
    String mensaje = "";
    for (int i = 0; i < length; i++) {
        mensaje += (char)payload[i];
    }
    Serial.print("[Payload] Contenido string recibido: ");
    Serial.println(mensaje);
    
    // Lógica de control perimetral mediante los LEDs
    if (mensaje.indexOf("intruso_confirmado") != -1) {
        Serial.println("[ALERTA CRÍTICA] ¡La Laptop confirmó un humano! Activando alarma física.");
        digitalWrite(PIN_LED_ROJO, HIGH);
        delay(3000);                          // Espera 3 segundos
        digitalWrite(PIN_LED_ROJO, LOW);  // Apaga amarillo al terminar
    }
    else if (mensaje.indexOf("falsa_alarma") != -1) {
        Serial.println("[INFO] Falsa alarma procesada por OpenCV. Restableciendo perímetro.");
        digitalWrite(PIN_LED_VERDE, HIGH);
        delay(3000);                          // Espera 3 segundos
        digitalWrite(PIN_LED_VERDE, LOW);     // Apaga verde al terminar
    }
}

// Subrutina para gestionar la reconexión automática al Broker MQTT
void reconectar_broker() {
    while (!client.connected()) {
        Serial.print("Enlazando pila de protocolos TCP/IP con el Broker Mosquitto...");
        if (client.connect(CLIENT_ID)) {
            Serial.println("\n[MQTT] Broker enlazado con éxito. Sistema listo.");
            // Volvemos a suscribirnos al canal de confirmación
            client.subscribe(TOPIC_CONFIRMACION);
        } else {
            Serial.print("[FALLO] Código de error MQTT = ");
            Serial.print(client.state());
            Serial.println(" -> Reintentando en 2 segundos...");
            delay(2000);
        }
    }
}

// 5. CONFIGURACIÓN INICIAL (Setup)
void setup() {
    Serial.begin(115200); // Configuración de registros de dirección de los pines (I/O)
    pinMode(PIN_LED_VERDE, OUTPUT);
    pinMode(PIN_LED_ROJO, OUTPUT);
    pinMode(PIN_LED_AMARILLO, OUTPUT);
    pinMode(PIN_SIMULADOR_PIR, INPUT);
    
    // Estado inicial del hardware
    digitalWrite(PIN_LED_VERDE, LOW); // Verde apagado
    digitalWrite(PIN_LED_ROJO, LOW); // Rojo Apagado
    digitalWrite(PIN_LED_AMARILLO, LOW); // Amarillo Apagado
    
    // Enlace WiFi
    conectar_wifi();
    
    // Configuración del servidor y callback MQTT
    client.setServer(MQTT_BROKER, MQTT_PORT);
    client.setCallback(al_recibir_mensaje);
}

// 6. BUCLE PRINCIPAL (Loop)
void loop() {
    // Si se pierde la conexión con el Broker, forzamos reconexión no bloqueante
    if (!client.connected()) {
        reconectar_broker();
    }

    // Hilo de polling asíncrono para mantener vivo el canal MQTT y escuchar callbacks
    client.loop();
    
    // Leemos la señal digital del pin simulador (Pulsador / Puente)
    int estadoPir = digitalRead(PIN_SIMULADOR_PIR);
    unsigned long tiempoActual = millis(); 
    
    // Filtro debounce de tiempo mínimo: 5 segundos (5000 ms) entre ráfagas de alertas
    if (estadoPir == HIGH && (tiempoActual - ultimoDisparo) > 5000) {
        Serial.println("\n[EVENTO] ¡Simulador PIR Activado (1 logical)!");
        Serial.print("Publicando señal en '");
        Serial.print(TOPIC_ALERTA);
        Serial.println("'...");
        
        // ==========================================
        // NUEVA LÓGICA: Encendido por 1 segundo fijo
        // ==========================================
        digitalWrite(PIN_LED_AMARILLO, HIGH);
        delay(1000);
        digitalWrite(PIN_LED_AMARILLO, LOW);
        // ==========================================

        // Publicamos el string en el Broker de forma directa
        if (client.publish(TOPIC_ALERTA, "MOVIMIENTO")) {
            Serial.println("[MQTT] Mensaje inyectado en el bus de datos.");
        } else {
            Serial.println("[ERROR] Error al publicar en el bus de datos.");
        }

        ultimoDisparo = tiempoActual;
    }
    delay(10); // Pequeño respiro para mitigar consumos del watchdog de la CPU
}