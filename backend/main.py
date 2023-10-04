import os
import logging
from dotenv import load_dotenv
from google.cloud import vision
from google.oauth2.service_account import Credentials
import openai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nikk0o046.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')
openai.organization = os.environ.get('OPENAI_ORG_ID')

GCP_TYPE = os.getenv("GCP_TYPE")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_PRIVATE_KEY_ID = os.getenv("GCP_PRIVATE_KEY_ID")
GCP_PRIVATE_KEY = os.getenv("GCP_PRIVATE_KEY")
GCP_CLIENT_EMAIL = os.getenv("GCP_CLIENT_EMAIL")
GCP_CLIENT_ID = os.getenv("GCP_CLIENT_ID")
GCP_AUTH_URI = os.getenv("GCP_AUTH_URI")
GCP_TOKEN_URI = os.getenv("GCP_TOKEN_URI")
GCP_AUTH_PROVIDER_X509_CERT_URL = os.getenv("GCP_AUTH_PROVIDER_X509_CERT_URL")
GCP_CLIENT_X509_CERT_URL = os.getenv("GCP_CLIENT_X509_CERT_URL")

# Reformat the PRIVATE_KEY for the credential json
GCP_PRIVATE_KEY = GCP_PRIVATE_KEY.replace('\\n', '\n')

logging.debug("Creating key dictionary")

# Create a dictionary to mimic the JSON key file
gcp_config = {
    "type": GCP_TYPE,
    "project_id": GCP_PROJECT_ID,
    "private_key_id": GCP_PRIVATE_KEY_ID,
    "private_key": GCP_PRIVATE_KEY,
    "client_email": GCP_CLIENT_EMAIL,
    "client_id": GCP_CLIENT_ID,
    "auth_uri": GCP_AUTH_URI,
    "token_uri": GCP_TOKEN_URI,
    "auth_provider_x509_cert_url": GCP_AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": GCP_CLIENT_X509_CERT_URL,
}


logging.info("Initializing Google Vision client...")

# Initialize the Google Vision client
try:
    client = vision.ImageAnnotatorClient(credentials=Credentials.from_service_account_info(gcp_config))
    logging.info("Google Vision client initialized.")
except Exception as e:
    logging.error(f"Failed to initialize Google Vision client: {e}")

def detect_text(content):
    logging.debug("Starting detect_text")
    # Detects text in the provided image
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    logging.info("Detected text: %s", texts[0].description)

    # Check if any text was detected
    if texts:
        return texts[0].description  # Return entire text detected in the image
    else:
        return ""


def ask_GPT(input_text):
    logging
    system_template = """You are a tool for people who are sensitive to gluten. You are provided a text, extracted from an image taken from a label of a product. This can be in any language. Your job is to analyse that text.

Begin by checking, if the text explicitly mentions gluten, e.g. "gluten-free" or "could contain traces of gluten". Then, proceed to analysing ingredients, one by one. Identify ingredients that are very likely to contain gluten, e.g. "wheat" and ingredients that are often at risk at containing gluten.

Based on your analysis, place the item in of of three categories: No gluten/Might contain gluten/Contains gluten.

Your response should be formatted as follows (example):

"Contains gluten. Reasoning: wheat contains gluten."

Your answer should only contain the response as defined above. Keep it as brief as possible: if many ingredients contain gluten, mention only the most important ones."""

    #human_template = f"Origin: {selectedCityID}\nInfo: {user_request}"
    human_template = input_text

    # Construct the conversation message list
    message_list = [
        {"role": "system", "content": system_template},
        {"role": "user", "content": human_template}
    ]

    # Request the response from the model
    response = openai.ChatCompletion.create(
      model="gpt-4",
      temperature=0,
      messages=message_list,
    )
    response_content = response.choices[0].message['content']
    logging.info("OpenAI response content: %s", response_content)

    return response_content

@app.post("/analyze/")
def analyze(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        content = file.file.read()

        # Get the detected text from the image
        extracted_text = detect_text(content)

        # Check if any text was detected
        if extracted_text:
            analysis = ask_GPT(extracted_text)
            return {"analysis": analysis}
        else:
            return JSONResponse(content={"error": "No text found"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

