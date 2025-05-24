from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from summarizer import summarize_text
from database import save_summary, get_summaries
import os
import PyPDF2
import docx

app = FastAPI(title="Document Summarizer API")

class TextInput(BaseModel):
    text: str
    max_length: int = 150

@app.post("/summarize")
async def summarize(input: TextInput):
    try:
        summary = summarize_text(input.text, max_length=input.max_length)
        summary_id = save_summary(input.text, summary)
        return {"summary": summary, "summary_id": summary_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize_file")
async def summarize_file(file: UploadFile = File(...)):
    try:
        content = ""
        if file.filename.endswith(".pdf"):
            pdf = PyPDF2.PdfReader(file.file)
            content = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif file.filename.endswith(".docx"):
            doc = docx.Document(file.file)
            content = " ".join(paragraph.text for paragraph in doc.paragraphs)
        elif file.filename.endswith(".txt"):
            content = await file.read()
            content = content.decode("utf-8")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        summary = summarize_text(content, max_length=150)
        summary_id = save_summary(content, summary)
        return {"summary": summary, "summary_id": summary_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summaries")
async def list_summaries():
    summaries = get_summaries()
    return {"summaries": summaries}