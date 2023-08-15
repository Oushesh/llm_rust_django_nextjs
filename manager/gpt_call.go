package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {
	// Set your OpenAI API key here
	apiKey := "YOUR_OPENAI_API_KEY"

	// Read input from standard input
	inputText, err := readInputFromStdin()
	if err != nil {
		log.Fatal("Error reading input from stdin:", err)
	}

	// Initialize the OpenAI client
	client := gpt.NewClient(apiKey)

	// Set up the prompt for language model inference
	prompt := "Given the following text:\n" + inputText + "\nDetect any hallucinations or inaccuracies in the text."

	// Create a context for the API call
	ctx := context.Background()

	// Call the language model for inference
	response, err := client.Completions.Create(
		ctx,
		&gpt.CompletionRequest{
			Model:     "gpt-3.5-turbo",
			Prompt:    prompt,
			MaxTokens: 100,
		},
	)
	if err != nil {
		log.Fatal("Error creating language model completion:", err)
	}

	// Print the generated response
	fmt.Println(response.Choices[0].Text)
}

func readInputFromStdin() (string, error) {
	var builder strings.Builder
	scanner := bufio.NewScanner(os.Stdin)

	for scanner.Scan() {
		builder.WriteString(scanner.Text())
		builder.WriteString("\n")
	}

	if err := scanner.Err(); err != nil {
		return "", err
	}

	return builder.String(), nil
}

// Get the openai api for Go, then pass the modules from: the django app
