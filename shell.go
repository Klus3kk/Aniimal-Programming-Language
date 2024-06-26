// shell.go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print(">> ")
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		inputLower := strings.ToLower(input)

		switch inputLower {
		case "exit":
			fmt.Println("Exiting...")
			return
		default:
			fmt.Println("Text: ", input)
		}
	}
}
