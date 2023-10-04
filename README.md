# Gluten Analyzer

A tool that allows users to scan product labels to determine if they contain gluten. The app uses Google Vision API for Optical Character Recognition (OCR) and OpenAI's GPT-4 to analyze the extracted text.

You can try it here:
https://nikk0o046.github.io/eat-or-not/

Link to a GIF that shows the app in use:
https://imgur.io/a/AjWzoZ5
Note: Imgur might present a content warning because the GIF was uploaded without an account. Rest assured, the GIF is safe for all audiences and solely demonstrates the app's functionality.

Last time updated: 4th of October 2023

## Features:

- Scan product labels using device camera.
- Analyze labels using a combination of OCR and AI to detect the presence of gluten.
- React-based frontend for intuitive use.

## Backend Setup:

### Pre-requisites:

- I used Python 3.11.4, but likely many other Python 3.x versions will do as well.
- A Google Cloud account with Vision API enabled.
- An OpenAI account for accessing GPT-4.

### Environment Variables:

Make sure to set up the `.env` file in your backend directory with the following:

OPENAI_API_KEY=
OPENAI_ORG_ID=
GCP_TYPE=
GCP_PROJECT_ID=
GCP_PRIVATE_KEY_ID=
GCP_PRIVATE_KEY=
GCP_CLIENT_EMAIL=
GCP_CLIENT_ID=
GCP_AUTH_URI=
GCP_TOKEN_URI=
GCP_AUTH_PROVIDER_X509_CERT_URL=
GCP_CLIENT_X509_CERT_URL=

The first two you get from OpenAI and the rest are related to Google Service Account, which you should create to use Google's Vision API. Remember to keep these private and never push your .env file to public repositories.

### Running the Backend:

1. Install required packages:
   pip install -r requirements.txt

2. Run main.py:
   python main.py

### Frontend Setup:

Overview:
The frontend of this application is built using React, a popular JavaScript library for building user interfaces, and is bootstrapped with Vite, a fast frontend build tool.

### Pre-requisites:

1. Node.js: Ensure you have Node.js installed. You can download and install it from Node.js official website.

2. Vite: After installing Node.js, you can install Vite globally using npm (Node Package Manager, which comes with Node.js).

npm install -g vite

### Steps:

1. Install the dependencies:
   npm install

2. Run the Vite server:
   npm run dev

## Docker Deployment:

The backend includes a Dockerfile and is designed to be deployed as a container on platforms like Google Cloud Run.

### Building the Docker Image:

docker build -t gluten-analyzer-backend .

### Deploying to Cloud Run:

Refer to [Google Cloud Run's documentation](https://cloud.google.com/run/docs) for deployment steps.

## Contributing:

If you find any bugs or have feature suggestions, please open an issue or submit a pull request.

## Contact:

For collaboration or queries, reach out to nikk0o046@gmail.com

## License:

[MIT License](LICENSE)
