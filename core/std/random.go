package std

import (
	"fmt"
	"math/rand"
)

import "time"

func AnimalPounce(args []interface{}) interface{} {
	if len(args) != 2 {
		return fmt.Errorf("pounce expects 2 arguments: (min, max)")
	}
	min, ok1 := args[0].(float64)
	max, ok2 := args[1].(float64)
	if !ok1 || !ok2 {
		return fmt.Errorf("pounce expects numbers")
	}
	if min > max {
		return fmt.Errorf("min must be <= max")
	}
	rand.Seed(time.Now().UnixNano())
	return float64(rand.Intn(int(max-min+1)) + int(min))
}

func AnimalStalk(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("stalk expects 1 argument: (target)")
	}
	target, ok := args[0].(float64)
	if !ok {
		return fmt.Errorf("stalk expects a number")
	}
	rand.Seed(time.Now().UnixNano())
	return float64(rand.Intn(int(target)))
}
func AnimalProwl(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("prowl expects 1 list argument")
	}
	list, ok := args[0].([]interface{})
	if !ok {
		return fmt.Errorf("prowl expects a list")
	}	
	if len(list) == 0 {
		return fmt.Errorf("cannot prowl in empty list")
	}
	rand.Seed(time.Now().UnixNano())
	index := rand.Intn(len(list))
	return list[index]
}

func AnimalTumble(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("scramble expects 1 list argument")
	}
	list, ok := args[0].([]interface{})
	if !ok {
		return fmt.Errorf("scramble expects a list")
	}
	rand.Seed(time.Now().UnixNano())

	// Copy the list
	shuffled := make([]interface{}, len(list))
	copy(shuffled, list)

	// Shuffle
	rand.Shuffle(len(shuffled), func(i, j int) {
		shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
	})
	return shuffled
}
