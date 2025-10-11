package std

import (
	"fmt"
	"sync"
	"time"
)

// For now its just a placeholder implementation that simulates sound handling.
// In a real implementation, you would integrate with an audio library to load
// and play sound files.
// And no. I won't do that. Sorry.
// No way. 


var (
	soundRegistry = map[int]map[string]interface{}{}
	nextSoundID   = 1
	soundMu       sync.Mutex
)

// helper: resolve a sound argument which can be either an instance map or an id (float64)
func resolveSoundArg(arg interface{}) (map[string]interface{}, error) {
	switch v := arg.(type) {
	case map[string]interface{}:
		return v, nil
	case float64:
		id := int(v)
		soundMu.Lock()
		defer soundMu.Unlock()
		if s, ok := soundRegistry[id]; ok {
			return s, nil
		}
		return nil, fmt.Errorf("sound id %d not found", id)
	default:
		return nil, fmt.Errorf("invalid sound reference: %T", arg)
	}
}

// load_sound(path): Load a sound file and return a sound instance
func AnimalLoadSound(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("load_sound expects 1 argument: (path)")
	}
	path, ok := args[0].(string)
	if !ok {
		return fmt.Errorf("load_sound expects a string path")
	}

	soundMu.Lock()
	id := nextSoundID
	nextSoundID++

	inst := map[string]interface{}{
		"id":       float64(id),
		"path":     path,
		"playing":  false,
		"volume":   1.0,
		"duration": 0.0, // unknown in placeholder
		"current":  0.0,
		"loop":     false,
		"started":  time.Time{},
	}
	soundRegistry[id] = inst
	soundMu.Unlock()

	return inst
}

// play_sound(sound): Play the given sound instance
func AnimalPlaySound(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("play_sound expects 1 argument: (sound)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}

	s["playing"] = true
	s["started"] = time.Now()
	// placeholder behaviour: reset current to 0 when started
	s["current"] = 0.0
	fmt.Printf("[sound] play: %v\n", s["path"])
	return nil
}

// stop_sound(sound): Stop the given sound instance
func AnimalStopSound(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("stop_sound expects 1 argument: (sound)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	s["playing"] = false
	// store current position as 0 for placeholder
	s["current"] = 0.0
	fmt.Printf("[sound] stop: %v\n", s["path"])
	return nil
}

// set_volume(sound, volume): Set the volume (0.0 to 1.0) for the sound instance
func AnimalSetVolume(args []interface{}) interface{} {
	if len(args) != 2 {
		return fmt.Errorf("set_volume expects 2 arguments: (sound, volume)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	vol, ok := args[1].(float64)
	if !ok {
		return fmt.Errorf("set_volume expects volume as number")
	}
	if vol < 0 || vol > 1 {
		return fmt.Errorf("volume must be between 0 and 1")
	}
	s["volume"] = vol
	fmt.Printf("[sound] set volume %v -> %f\n", s["path"], vol)
	return nil
}

// is_playing(sound): Check if the sound instance is currently playing
func AnimalIsPlaying(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("is_playing expects 1 argument: (sound)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	playing, _ := s["playing"].(bool)
	return playing
}


// get_duration(sound): Get the total duration of the sound in seconds
func AnimalGetDuration(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("get_duration expects 1 argument: (sound)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	dur, _ := s["duration"].(float64)
	return dur
}

// get_current_time(sound): Get the current playback time of the sound in seconds
func AnimalGetCurrentTime(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("get_current_time expects 1 argument: (sound)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	// placeholder: compute elapsed since started if playing
	if playing, _ := s["playing"].(bool); playing {
		if started, ok := s["started"].(time.Time); ok && !started.IsZero() {
			elapsed := time.Since(started).Seconds()
			// store and return
			s["current"] = elapsed
			return elapsed
		}
	}
	cur, _ := s["current"].(float64)
	return cur
}

// set_current_time(sound, time): Set the current playback time of the sound in seconds
func AnimalSetCurrentTime(args []interface{}) interface{} {
	if len(args) != 2 {
		return fmt.Errorf("set_current_time expects 2 arguments: (sound, time)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	t, ok := args[1].(float64)
	if !ok {
		return fmt.Errorf("set_current_time expects a time number")
	}
	if t < 0 {
		return fmt.Errorf("time must be non-negative")
	}
	s["current"] = t
	// adjust started timestamp so computed elapsed respects this
	if playing, _ := s["playing"].(bool); playing {
		s["started"] = time.Now().Add(-time.Duration(t) * time.Second)
	}
	return nil
}

// set_loop(sound, loop): Set whether the sound should loop when it reaches the end
func AnimalSetLoop(args []interface{}) interface{} {
	if len(args) != 2 {
		return fmt.Errorf("set_loop expects 2 arguments: (sound, loop)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	loop, ok := args[1].(bool)
	if !ok {
		return fmt.Errorf("set_loop expects a boolean")
	}
	s["loop"] = loop
	return nil
}

// get_loop(sound): Get whether the sound is set to loop
func AnimalGetLoop(args []interface{}) interface{} {
	if len(args) != 1 {
		return fmt.Errorf("get_loop expects 1 argument: (sound)")
	}
	s, err := resolveSoundArg(args[0])
	if err != nil {
		return err
	}
	loop, _ := s["loop"].(bool)
	return loop
}
