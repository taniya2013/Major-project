import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6KiUAont9b0O7AiP5jXAFy1B93uZuE4P3hPNni6W-XyXg")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)