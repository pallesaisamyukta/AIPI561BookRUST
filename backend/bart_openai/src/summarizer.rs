// summarizer.rs
use crate::models::{CompletionRequest, CompletionResponse, Message}; // Adjusted import
use reqwest::Client;
use std::error::Error;

/// Splits text into chunks for processing.
fn split_text_into_chunks(text: &str, max_words: usize) -> Vec<String> {
    let words: Vec<&str> = text.split_whitespace().collect();
    let mut chunks = Vec::new();
    for chunk in words.chunks(max_words) {
        chunks.push(chunk.join(" "));
    }
    chunks
}

/// Summarizes text using the API.
pub async fn summarize_text(user_text: &str) -> Result<String, Box<dyn Error>> {
    let client = Client::new();
    let api_key = "sk-no-key-required"; // Replace with your actual API key
    let base_url = "http://localhost:8080/v1";
    let max_words_per_chunk = 2000;
    let chunks = split_text_into_chunks(user_text, max_words_per_chunk);

    let mut summaries = Vec::new();
    for chunk in chunks {
        let formatted_content = format!(
            "Please summarize the following text:\n\n{}\n\nSummarize the key events only, to the point, and do not include any direct quotes or specific lines from the text.",
            chunk
        );

        let request_body = CompletionRequest {
            model: "LLaMa_CPP",
            messages: vec![
                Message {
                    role: "system",
                    content: "You are a helpful assistant that provides concise summaries of text. Focus on summarizing the key events without listing quotes.",
                },
                Message {
                    role: "user",
                    content: &formatted_content,
                },
            ],
        };

        let response = client
            .post(format!("{}/chat/completions", base_url))
            .bearer_auth(api_key)
            .json(&request_body)
            .send()
            .await?;

        let completion_response: CompletionResponse = response.json().await?;
        let summary = &completion_response.choices[0].message.content;

        summaries.push(summary.replace("Here are the key events summarized:", "").trim().to_string());
    }

    // Combine all summaries into one string
    let combined_summary = summaries.join("\n\n");

    Ok(combined_summary)
}
