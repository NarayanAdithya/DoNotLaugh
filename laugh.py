from dotenv import load_dotenv
load_dotenv('.env')
from app import app


app.run(debug=True, host=app.config['HOST'], port=8000)
