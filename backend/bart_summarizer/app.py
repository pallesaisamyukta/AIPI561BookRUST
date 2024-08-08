from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BartForConditionalGeneration, BartTokenizer
import textwrap
import torch
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Global variables for the model and tokenizer
model_name = "facebook/bart-large-cnn"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
tokenizer = None

@app.on_event("startup")
async def startup_event():
    global model, tokenizer
    logger.info("Starting up...")
    try:
        model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
        tokenizer = BartTokenizer.from_pretrained(model_name)
        logger.info("Model and tokenizer loaded successfully.")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

def text_summarizer_batch(text, batch_size=4, max_chunk_size=1000):
    formatted_summary = ""
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    for batch_start in range(0, len(chunks), batch_size):
        batch_texts = chunks[batch_start:batch_start+batch_size]
        inputs = tokenizer.batch_encode_plus(
            ["summarize: " + chunk for chunk in batch_texts], 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True, 
            padding=True
        ).to(device)
        summary_ids = model.generate(
            inputs['input_ids'], 
            max_length=250, 
            min_length=50, 
            length_penalty=2.0, 
            num_beams=4, 
            early_stopping=True
        )
        summaries = [tokenizer.decode(summary_id, skip_special_tokens=True) for summary_id in summary_ids]
        formatted_summary += "\n".join(textwrap.wrap("\n".join(summaries), width=80))

    return formatted_summary

class InputText(BaseModel):
    text: str

@app.post("/process/")
async def process_text(input_text: InputText):
    logger.info("Processing text.")
    try:
        total_length = len(input_text.text)
        present_summary = text_summarizer_batch(input_text.text)
        logger.info("First BART Summarization complete.")
        while len(present_summary) > total_length / 5:
            present_summary = text_summarizer_batch(present_summary, max_chunk_size=800)
            logger.info("Second BART Summarization complete.")
        return {"output": present_summary}
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


