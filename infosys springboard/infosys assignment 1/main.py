import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyCnDzrcroRYPxj35_J1y3FlwYG9cNYTLuk")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message(
    "I love movies."

)

print(response.text)