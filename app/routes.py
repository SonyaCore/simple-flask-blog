from app import app
from app.main.utils import servername

@app.context_processor
def name():
    info = {
         'servername':   f'{servername()}'
     }
    return dict(info=info)
