import uvicorn
import gradio as gr
from fastapi import FastAPI, status
from healthcheck import app_healthcheck
from gradio_interface import gradio_interface


# Initialize FastAPI app
app = FastAPI()


# Add healthcheck method
@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def healthcheck():
    return app_healthcheck()


# Mount gradio interface into app
app = gr.mount_gradio_app(app, gradio_interface, path="/")


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
