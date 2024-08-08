// api_client.rs
use crate::models::{InputData, OutputData}; // Adjusted import
use reqwest::Client;
use std::error::Error;

/// Sends text to the API and retrieves the response.
pub async fn send_text_to_api(url: &str, input_data: InputData) -> Result<OutputData, Box<dyn Error>> {
    let client = Client::new();
    
    // Send the POST request
    let response = client
        .post(url)
        .json(&input_data)
        .send()
        .await?;

    if response.status().is_success() {
        // Parse and return the JSON response
        let output_data: OutputData = response.json().await?;
        Ok(output_data)
    } else {
        Err(Box::new(response.error_for_status().unwrap_err()))
    }
}
