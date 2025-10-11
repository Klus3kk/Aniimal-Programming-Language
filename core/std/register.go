package std

import "animal/core"

// RegisterStandardLibrary injects standard library functions into the symbol table.
func RegisterStandardLibrary(symbolTable *core.SymbolTable) {
	// Math
	symbolTable.Set("max", AnimalMax)
	symbolTable.Set("min", AnimalMin)
	symbolTable.Set("abs", AnimalAbs)

	// Numbers
	symbolTable.Set("purr", AnimalPurr)
	symbolTable.Set("scent", AnimalScent)

	// Random
	symbolTable.Set("pounce", AnimalPounce)
	symbolTable.Set("stalk", AnimalStalk)
	symbolTable.Set("tumble", AnimalTumble)

	// List
	symbolTable.Set("paw", AnimalPaw)
	symbolTable.Set("burrow", AnimalBurrow)
	symbolTable.Set("perch", AnimalPerch)
	symbolTable.Set("lick", AnimalLick)
	symbolTable.Set("howl", AnimalHowl)
	symbolTable.Set("chase", AnimalChase)
	symbolTable.Set("trace", AnimalTrace)
	symbolTable.Set("trail", AnimalTrail)
	symbolTable.Set("howlpack", AnimalHowlpack)
	symbolTable.Set("nest", AnimalNest)

	// String
	symbolTable.Set("pelt", AnimalPelt)
	symbolTable.Set("nuzzle", AnimalNuzzle)
	symbolTable.Set("squirrel", AnimalSquirrel)
	symbolTable.Set("parrot", AnimalParrot)
	symbolTable.Set("rat", AnimalRat)
	symbolTable.Set("mole", AnimalMole)
	symbolTable.Set("snipe", AnimalSnipe)
	symbolTable.Set("ferret", AnimalFerret)
	symbolTable.Set("badger", AnimalBadger)

	// Sounds
	symbolTable.Set("load_sound", AnimalLoadSound)
	symbolTable.Set("play_sound", AnimalPlaySound)
	symbolTable.Set("stop_sound", AnimalStopSound)
	symbolTable.Set("set_volume", AnimalSetVolume)
	symbolTable.Set("is_playing", AnimalIsPlaying)
	symbolTable.Set("get_duration", AnimalGetDuration)
	symbolTable.Set("get_current_time", AnimalGetCurrentTime)
	symbolTable.Set("set_current_time", AnimalSetCurrentTime)
	symbolTable.Set("set_loop", AnimalSetLoop)
	symbolTable.Set("get_loop", AnimalGetLoop)

	// Tests

}
