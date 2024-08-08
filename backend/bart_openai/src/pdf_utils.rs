// pdf_utils.rs
use lopdf::Document;
use std::error::Error;

/// Reads a PDF file and extracts text, then filters and returns it.
pub fn read_pdf(pdf_path: &str) -> Result<String, Box<dyn Error>> {
    // Load the PDF document
    let document = Document::load(pdf_path)?;
    
    // Retrieve the pages of the document
    let pages = document.get_pages();
    let mut text = String::new();
    
    // Extract text from each page
    for (i, _) in pages.iter().enumerate() {
        let page_number = (i + 1) as u32;
        if let Ok(page_text) = document.extract_text(&[page_number]) {
            text.push_str(&page_text);
        }
    }

    // Print the length of the extracted text
    println!("Length of extracted text: {}", text.len());

    // Split text into sentences and filter
    let filtered_text = filter_sentences(&text);
    
    // Print the length of the filtered text
    println!("Length of filtered text: {}", filtered_text.len());

    Ok(filtered_text)
}

/// Splits text into sentences and filters them.
fn filter_sentences(text: &str) -> String {
    let mut sentences = Vec::new();
    let mut current_sentence = String::new();
    let sentence_endings = ['.', '!', '?'];

    for char in text.chars() {
        current_sentence.push(char);
        if sentence_endings.contains(&char) {
            sentences.push(current_sentence.trim().to_string());
            current_sentence.clear();
        }
    }

    if !current_sentence.trim().is_empty() {
        sentences.push(current_sentence.trim().to_string());
    }

    let filtered_sentences: Vec<String> = sentences.chunks(4)
        .flat_map(|chunk| chunk.iter().take(3).cloned())
        .collect();

    filtered_sentences.join(" ")
}
