This dir of code gives you the starting point for the common components of most games - often this is 
called 'boilerplate code' because you will re-use it time and time again without any changes. It includes:

* Keyboard input state reading
* Standard pygame initialisation
* Quit event handling
* A game-state list (well, technically a dictionary) that allows 
  you to 'swap' between game screens - start, play, high scores etc.

== Structure ==
The core concept to understand is the game-state. For each screen you want
to show - including the main 'game in play' screen - you define it in terms of a name 
and the name its associated update and draw functions.

* Define an update function and a draw function for each screen (game-state),
* Define a custom_game_init() function
* In this function, use: 
  - add_game_state("state-name", "update_function_name", "draw_function_name")

To add it to available states in the game. 

* Call:

set_game_state("state_game") to start the named update and draw functions for this state.

Use this initially in your custom_game_init to kick things off with a start screen and then 
use it inside the game-state update function in response to input or events to swap between 
states. 

== To Use The Master Copy ==
* Copy the dir 'MyGame' to your own files location (home dir)
 - Click on the MyGame folder *once* to select it
 - Click Home on the explorer window menu bar
 - Click Copy
 - Open your home dir
 - Click Home->Paste to create a copy of the folder
* Rename the copy
 - Click the new folder copy once to ensure it is selected
 - Click Home->Rename and change the folder name to the name of your new game idea
* Start coding!
 - Edit the existing game_start and game_running functions to create your first game.
 - Add new game-states as required using the same structure.

== Useful globals ==
* screen - is the main display surface
* keys, last_keys - the state of the keyboard now and last frame. This allows you to see if a 
  key has been pressed just once.
* background_surface - if you declare a global background_image_path, the framework will load
  this image into this surface and also size the game window to match.




