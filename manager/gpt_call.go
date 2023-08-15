package main

import (
	"context"
	"log"
)

func main() {
	// Set your OpenAI API Key here.
	apiKey := "YOUR_OPENAI_API_KEY"

	// Read input from standard input
	inputText, err := readInputFromStdin()

	if err != nil {
		// Read input from standard input
		inputText, err := readInputFromStdin()
		if err != nil {
			log.Fatal("Error reading input from stdin:", err)
		}
	}

	// Initialize the OpenAI client
	client := gpt.NewClient(apiKey)

	// Set up the prompt for language model inference
	prompt := "Given the following text:\n" + inputText + "\nDetect any hallucinations or inaccuracies in the text."

	// Create a context for the API call
	ctx := context.Background()
	
}

//Test for the call for chatGPT.
//add the endpoints for Django for the ocr pdf.
