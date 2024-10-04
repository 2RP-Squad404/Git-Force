import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting

# Configuração da IA
def generate(prompt: str, instruction: str):
    textsi_1 = instruction

    vertexai.init(project="tarefa-squad", location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-001",
        system_instruction=[textsi_1]
    )
    responses = model.generate_content(
        ["""{}(não retorne ```sql)""".format(prompt)],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    content = [] # array para transformar em string
    for response in responses:
        content.append(response.text)
    text = "".join(content) # Transforma em string
    return text

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.4,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]