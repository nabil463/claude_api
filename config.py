import os

class Api_Keys:
    CLAUDE_KEY = os.environ.get('ANTHROPIC_API_KEY')
    CHATGPT_KEY = os.environ.get('OPENAPI_API_KEY')