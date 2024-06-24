## Claude Flask API 

# Setup the Virtual Environment
- mkdir .venv
- python3 -m venv ./.venv/
- source .venv/bin/activate

# Install dependencies from requirements.txt
- python3 -m pip install -r requirements.txt

# Setup the .env file
- Copy .env from .env.examaple
- Set the Claude and ChatGPT Key

# Start the server
- flask run