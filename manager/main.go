package main

import (
	"fmt"
	"log"
	"net/http"
)

type Article struct {
	Title   string "json:Title"
	Desc    string "json:"
	Content string "json:content"
}
type Articles []Article

func handlePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Homepage Endpoint hit") // Use fmt.Fprint instead of fmt.Fprintf
}

func handleRequests() {
	http.HandleFunc("/", handlePage) // Use the correct function name
	//log.Fatal(http.ListenAndServeTLS(":8081", "cert.pem", "key.pem", nil)) // Provide the certificate and key files
	log.Fatal(http.ListenAndServe(":8081", nil)) // Provide the certificate and key files
}

func main() {
	handleRequests()
}
