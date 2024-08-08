// models.rs
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub struct CompletionRequest<'a> {
    pub model: &'a str,
    pub messages: Vec<Message<'a>>,
}

#[derive(Serialize)]
pub struct Message<'a> {
    pub role: &'a str,
    pub content: &'a str,
}

#[derive(Deserialize)]
pub struct Choice {
    pub message: MessageContent,
}

#[derive(Deserialize)]
pub struct MessageContent {
    pub content: String,
}

#[derive(Deserialize)]
pub struct CompletionResponse {
    pub choices: Vec<Choice>,
}

#[derive(Serialize)]
pub struct InputData {
    pub text: String,
}

#[derive(Deserialize)]
pub struct OutputData {
    pub output: String,
}
