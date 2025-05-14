from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io, json

 # celonis connection imports
 # imports for the temporal/declarative/log-skeleton/resource based profiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile, metadata: str = Form(...)):
    # Parse inputs
    meta = json.loads(metadata)
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content), sep=';')  # change if needed

    # Celonis connection (if used)
    #celonis = connect_to_celonis(meta['api_url'], meta['api_token'])

    # Run all checks
    # temporal_result = run_temporal_profile(df, meta, celonis)
    # declarative_result = run_log_skeleton(df, meta, celonis)
    # resource_result = run_resource_analysis(df, meta, celonis)

    # return JSONResponse(content={
    #     "temporal": temporal_result,
    #     "declarative": declarative_result,
    #     "resource": resource_result
    # })