from dotenv import load_dotenv
load_dotenv('.env')
from app import app


app.run(port=8000)
