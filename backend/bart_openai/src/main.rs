use warp::Filter;
use std::error::Error;
use tokio;

mod pdf_utils;
mod api_client;
mod summarizer;
mod models;

use models::{InputData, OutputData};
use pdf_utils::read_pdf;
use api_client::send_text_to_api;
use summarizer::summarize_text;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct SummarizeRequest {
    pdf_path: String,
}

#[derive(Serialize)]
struct SummarizeResponse {
    summary: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    println!("Sserver starting");
    // Define the /summarize endpoint
    let summarize = warp::post()
        .and(warp::path("summarize"))
        .and(warp::body::json())
        .and_then(handle_summarize);

    // Run the warp server on port 3030
    warp::serve(summarize).run(([0, 0, 0, 0], 3030)).await;

    Ok(())
}

// Asynchronous function to handle summarize requests
async fn handle_summarize(input: SummarizeRequest) -> Result<impl warp::Reply, warp::Rejection> {
    println!("Got a summarizaito req");
    let pdf_path = input.pdf_path;

    match process_pdf(&pdf_path).await {
        Ok(summary) => Ok(warp::reply::json(&SummarizeResponse { summary })),
        Err(e) => Ok(warp::reply::json(&SummarizeResponse { summary: e.to_string() })),
    }
}

async fn process_pdf(pdf_path: &str) -> Result<String, Box<dyn Error>> {
    // Read and process the PDF
    let filtered_text = read_pdf(pdf_path)?;
    
    // Print the first 100 characters of the filtered text
    let preview_length = 100;
    let preview_text = if filtered_text.len() > preview_length {
        &filtered_text[..preview_length]
    } else {
        &filtered_text
    };
    println!("Preview of filtered text: {}", preview_text);

    let url = "http://bart_summarizer:9999/process/";
    
    // Create the request payload
    let input_data = InputData {
        text: filtered_text,
    };

    // Send the POST request
    let output_data: OutputData = send_text_to_api(url, input_data).await?;
    
    // Summarize the output text
    let summary = summarize_text(&output_data.output).await?;
    Ok(summary)
}
