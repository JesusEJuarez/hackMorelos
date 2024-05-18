import openai

# Reemplaza 'your-api-key' con la clave de API que generaste
openai.api_key = 'skaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

def obtener_respuesta(prompt):
    try:
        respuesta = openai.Completion.create(
            engine="ada",  # Puedes cambiar el motor si es necesario
            prompt=prompt,
            max_tokens=150,  # Ajusta la cantidad de tokens según tus necesidades
            n=1,
            stop=None,
            temperature=0.7  # Ajusta la temperatura para controlar la creatividad de la respuesta
        )
        return respuesta.choices[0].text.strip()
    except Exception as e:
        return f"Error al obtener respuesta: {e}"

# Ejemplo de uso
mi_prompt = "¿Qué riesgos podría representar consumir ibuprofeno seguido.?"
respuesta = obtener_respuesta(mi_prompt)
print(respuesta)
