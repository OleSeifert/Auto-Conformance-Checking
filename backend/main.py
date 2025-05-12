# backend/main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io, json

app = FastAPI()

# Allow React frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-and-analyze")
async def upload_and_analyze(file: UploadFile, metadata: str = Form(...)):
    # Step 1: Parse metadata
    meta = json.loads(metadata)

    # Step 2: Read uploaded file
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content), sep=';')  # Assumes semicolon separator

    # Step 3: For now, just print what we got
    print("Received metadata:", meta)
    print("CSV columns:", df.columns.tolist())

    # TODO: Call a Jupyter kernel or analysis function here

    # Step 4: Return dummy response
    return JSONResponse(content={
        "status": "success",
        "columns": df.columns.tolist(),
        "meta": meta,
        "message": "Ready to run notebook or analysis script."
    })