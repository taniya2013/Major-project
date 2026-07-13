import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6IOfPnaAzfoITISnBct8sFSGRWrWwEEBnF1ZfxIdIBY3g")

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)