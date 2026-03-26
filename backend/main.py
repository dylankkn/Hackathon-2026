import serial
import time
from quiz_ia import iniciar_quiz



# --- CONFIGURAÇÃO DA SERIAL ---
porta_arduino = 'COM22' 
baud_rate = 9600


# --- LOOP PRINCIPAL ---
try:
    arduino = serial.Serial(porta_arduino, baud_rate, timeout=1)
    print(f"✅ Conectado ao Arduino na {porta_arduino}!")

    while True:
        if arduino.in_waiting > 0:
            msg = arduino.readline().decode('utf-8', errors='ignore').strip()
            if msg == "LED VERDE ON - Quiz ativado":
                iniciar_quiz(arduino)

except serial.SerialException:
    print("❌ Erro: Porta COM ocupada! Verifique o Monitor Serial do Arduino.")
except KeyboardInterrupt:
    print("\nEncerrando...")
finally:
    if 'arduino' in locals():
        arduino.close()

