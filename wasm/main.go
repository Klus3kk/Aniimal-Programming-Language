package main

import (
	"animal/core"
	"syscall/js"
)

func runAnimal(this js.Value, args []js.Value) interface{} {
	code := args[0].String()

	globalSymbolTable := core.NewSymbolTable()
	context := &core.Context{
		DisplayName:  "<browser>",
		Symbol_Table: globalSymbolTable,
	}

	core.ClearCapturedOutput() // Reset buffer first
	core.CaptureOutput = true  // Start capturing!

	_, err := core.CustomRun(code, "<stdin>", context)

	output := core.GetCapturedOutput()
	core.CaptureOutput = false // Stop capturing after run

	if err != nil {
		return js.ValueOf("Error: " + err.Error())
	}
	//
	//// If result exists, append it too
	//if result != nil {
	//	output += fmt.Sprintf("%v", result)
	//}

	return js.ValueOf(output)
}

func main() {
	c := make(chan struct{}, 0)
	js.Global().Set("runAnimalCode", js.FuncOf(runAnimal))
	<-c // block forever
}
