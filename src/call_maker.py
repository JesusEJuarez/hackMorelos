from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from twilio.rest import Client
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
import pytz
import os


## Carga de los datos necesarios para la llamada  
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = "your_twilio_phone_number"
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



def listar_todos_los_pacientes():
    # Conexión con MongoDB
    client = MongoClient('mongodb+srv://leo:123@cluster0.hnpunss.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client['Data_HackMorelos']
    collection = db['Pacientes']

    # Recupera todos los documentos de la colección
    resultados = collection.find()
    pacientes = []
    # Itera sobre los resultados de la consulta
    for resultado in resultados:
        pacientes.append(resultado)
    return pacientes

def comprobar_citas_y_medicamentos(pacientes):
    ahora = datetime.now(pytz.timezone('America/Mexico_City'))#datetime(2024, 6, 11, 8, 00).replace(tzinfo=timezone.utc) #
    mensajes = []
    fecha = 0
    for paciente in pacientes:
        
        fecha = 0 # Se inicializa en 0 para poder evitar generar llamadas con fechas y tiempo anterior al actual
        nombre = paciente['nombre']
        telefono = paciente['numero']
        medicamentos = paciente['medicamentos']
        citas = paciente['fecha_cita_sig']
        #Inicializa el mensaje
        mensaje = f"Hola {nombre},"

        # Comprobar medicamentos para hoy
        medicamentos_hoy = [med for med in medicamentos if datetime.strptime(med['hora'], "%H:%M").time() >= ahora.time()]
        horas = []
        for med in medicamentos_hoy:
            horas.append(datetime.strptime(med['hora'], "%H:%M").replace(year=ahora.year, day=ahora.day, month=ahora.month))

        if medicamentos_hoy:
            mensaje += " recuerda tomar tus medicamentos: " + ", ".join([f"{med['nombre']} a las {med['hora']}" for med in medicamentos_hoy]) + "."
            #Elige la fecha más proxima al momento actual para realizar la llamada
            fecha = sorted(horas)[0]
        # Comprobar citas para los próximos días
        if datetime.strptime(citas, "%d/%m/%Y").replace(tzinfo=timezone.utc) <= (ahora + timedelta(days=7)):
            citas_proximas = datetime.strptime(citas, "%d/%m/%Y")
            mensaje += " Su siguiente cita médica es: " + ", ".join([f"{citas}"]) + "."
            if fecha == 0:
                fecha = ahora.replace(hour=15)
        mensajes.append((telefono, mensaje, fecha))

    return mensajes

def programar_llamada(telefono, mensaje, fecha):
    def realizar_llamada():
        llamada = client_twilio.calls.create(
            twiml=f'<Response><Say language="es-MX" voice="woman">{mensaje}</Say></Response>',
            to=telefono,
            from_=TWILIO_PHONE_NUMBER
        )
        print(f"Llamada programada a {telefono} para el {fecha} con SID: {llamada.sid}")

    scheduler.add_job(realizar_llamada, trigger=DateTrigger(run_date=fecha, timezone='America/Mexico_City'))

def enviar_mensajes(mensajes):
    for telefono, mensaje, fecha in mensajes:
        if fecha != 0:
          print(f"Programando llamada a {telefono} para el {fecha} con mensaje: {mensaje}")
          programar_llamada(telefono, mensaje, fecha)




# Configuración del programador de tareas
scheduler = BackgroundScheduler()
scheduler.start() 

# Cargar datos de pacientes desde la base de datos
pacientes = listar_todos_los_pacientes()

# Comprobar citas y medicamentos, generar mensajes
mensajes = comprobar_citas_y_medicamentos(pacientes)

# Programar las llamadas telefónicas
enviar_mensajes(mensajes)
