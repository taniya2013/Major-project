import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6IqdO5rdk__cPu5EyElZVrV-65TiulmjX1tYIiG5lfcSg")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)