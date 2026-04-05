from app import create_app
import os

flask_app = create_app()

# Wrap Flask WSGI app as ASGI for uvicorn
from asgiref.wsgi import WsgiToAsgi
app = WsgiToAsgi(flask_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("run:app", host="0.0.0.0", port=port)