Audio Functions
===============

Animal includes a handful of helpers for lightweight audio playback. For now, these are just placeholders, you can't do much with them yet, because audio files can't be loaded.

Loading Sounds
--------------

``load_sound(path)``
   Loads the file located at *path* and returns a sound handle. The path can be absolute or relative to the current working directory.

   .. code-block:: animal

      bark -> load_sound("assets/bark.wav")

Playback Control
----------------

The following functions expect a handle returned from ``load_sound``:

``play_sound(sound)``
   Starts playback from the current position. Calling it again while already playing restarts the sound.

``stop_sound(sound)``
   Stops playback and resets the position to the beginning.

``set_volume(sound, value)``
   Sets the volume. ``value`` must be between ``0.0`` (mute) and ``1.0`` (full volume).

``set_loop(sound, should_loop)``
   Enables or disables looping when the end of the sound is reached.

``set_current_time(sound, seconds)``
   Seeks to a specific playback position, expressed in seconds.

Query Helpers
-------------

``is_playing(sound)``
   Returns ``true`` if the sound is currently playing.

``get_duration(sound)``
   Returns the total length of the sound in seconds.

``get_current_time(sound)``
   Returns the current playback position in seconds.

``get_loop(sound)``
   Returns ``true`` when looping is enabled.

Example
-------

.. code-block:: animal

   howl play_intro() {
       intro -> load_sound("sfx/intro.wav") :: NOT WORKING FOR NOW
       set_volume(intro, 0.6)
       set_loop(intro, false)

       play_sound(intro)
       pounce is_playing(intro) {
           :: wait until the intro finishes
       }
   }

   play_intro()
