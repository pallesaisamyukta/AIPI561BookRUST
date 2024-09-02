from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BartForConditionalGeneration, BartTokenizer
import textwrap
import torch
import logging
from concurrent.futures import ThreadPoolExecutor

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) # Create a logger object to log messages for debugging and monitoring

app = FastAPI()

# Global variables for the model and tokenizer
model_name = "facebook/bart-large-cnn"  # Specify the pre-trained BART model to use
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # Check if CUDA (GPU) is available; use CPU otherwise
model = None  # Placeholder for the BART model, to be initialized during startup
tokenizer = None  # Placeholder for the tokenizer, to be initialized during startup

@app.on_event("startup")
async def startup_event():
    """
    Event handler for the startup event.
    This function is triggered when the FastAPI application starts. It loads the BART model and tokenizer into memory.
    """
    global model, tokenizer
    logger.info("Starting up...")  # Log the startup event
    try:
        model = BartForConditionalGeneration.from_pretrained(model_name).to(device)  # Load the BART model onto the specified device (CPU/GPU)
        tokenizer = BartTokenizer.from_pretrained(model_name)  # Load the corresponding tokenizer
        logger.info("Model and tokenizer loaded successfully.")  # Log successful loading
    except Exception as e:
        logger.error(f"Error during startup: {e}")  # Log any errors encountered during model/tokenizer loading

@app.get("/")
async def read_root():
    """
    Root endpoint for the FastAPI application.
    Returns a simple JSON message indicating that the application is up and running.
    """
    return {
        "message": "Application is up and running!"
    }

def process_chunk(chunk):
    """
    Function to process and summarize a single chunk of text.

    Args:
        chunk (str): A chunk of text to be summarized.

    Returns:
        str: The summarized text.
    """
    inputs = tokenizer.batch_encode_plus(
        ["summarize: " + chunk], 
        return_tensors="pt", 
        max_length=1024, 
        truncation=True, 
        padding=True
    ).to(device)  # Tokenize the input text and prepare it for the model
    summary_ids = model.generate(
        inputs['input_ids'], 
        max_length=250, 
        min_length=50, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True
    )  # Generate a summary using the BART model
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)  # Decode the generated IDs back into text

def text_summarizer_batch(text, batch_size=4, max_chunk_size=1000):
    """
    Function to summarize a long text by splitting it into chunks and processing them in parallel.

    Args:
        text (str): The full text to be summarized.
        batch_size (int, optional): The number of chunks to process in parallel. Defaults to 4.
        max_chunk_size (int, optional): The maximum size of each text chunk. Defaults to 1000 characters.

    Returns:
        str: The summarized version of the input text.
    """
    formatted_summary = ""  # Initialize an empty string to store the final summarized text
    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]  # Split the text into chunks

    with ThreadPoolExecutor() as executor:
        summaries = list(executor.map(process_chunk, chunks))  # Process each chunk in parallel using ThreadPoolExecutor

    formatted_summary = " ".join(textwrap.wrap("\n".join(summaries), width=80))  # Join the summarized chunks and format them neatly
    print("Formatted Summary: ")
    print(formatted_summary)  # Print the final summarized text (for debugging)
    return formatted_summary

class InputText(BaseModel):
    """
    Pydantic model to validate the input data for the summarization API.
    
    Attributes:
        text (str): The text to be summarized.
    """
    text: str

@app.post("/process/")
async def process_text(input_text: InputText):
    """
    API endpoint to process and summarize the input text.

    Args:
        input_text (InputText): A Pydantic model containing the text to be summarized.

    Returns:
        dict: A dictionary containing the summarized text under the "output" key.
    """
    logger.info("Processing text.")  # Log the start of the text processing
    try:
        total_length = len(input_text.text)  # Get the total length of the input text
        present_summary = text_summarizer_batch(input_text.text)  # Summarize the input text
        logger.info("First BART Summarization complete.")  # Log the completion of the first summarization
        while (len(present_summary) > total_length / 5) and (len(present_summary) > 4000):
            present_summary = text_summarizer_batch(present_summary, max_chunk_size=800)  # Further summarize if the text is still too long
            logger.info("Second BART Summarization complete.")  # Log the completion of the second summarization
        return {"output": present_summary}  # Return the summarized text
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))  # Raise an HTTP 500 error with the error message