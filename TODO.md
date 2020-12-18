TODO:

* Views/game - Nicer 'Game Over' graphics
* Views/app - Retro background for app menu
* Views/app - Have the restart and quit buttons as consts / as singularly changeable stuff
  * They are consts RN, but can be changed for each keymap independently - Not good
* Views/app - Have a display with info about the current config when hovering over an option
* Views/app | app/app - Have a "NotImplementedError" screen for online multiplayer
* Views/app | app/app - Add logging and display error if scr too small for game
* server | app/app - Create online multiplayer feature
* main | Views/main | Views/game - Make the row dots alignment customizable
* BUGFIX - app - When one player gets a gameOver, the others are blocked

DONE TASKS:

* ~~player/player - Refactor~~
* ~~player/player - Implement wall kicks according to the SRS algorithm~~
* ~~player/player - Rethink centerpoint placement for blocks~~
* ~~Views/app - Make the multiplayer players amount changeable~~
* ~~Views/app - Display keys for both players~~
* ~~Refactor in general~~
* ~~Async run local multiplayer~~
* ~~Refactor graphics code~~
* ~~Create the settings menu~~
* ~~Make keys mappable~~
* ~~Make KEY_ENTER work~~
* ~~Slowly print menu on first time~~
* ~~Print options in the middle of active scr~~
* ~~Graphics for the app menu~~
* ~~Implement exit~~
* ~~Have a ready? set? go! screen~~
* ~~Implement return key~~
* ~~Display score~~
* ~~Display next piece~~
* ~~Display game over~~
* ~~Display instructions~~
* ~~Don't print arrow input~~
* ~~Fix movement jankyness~~
* ~~Fix rotation centerpoint bug~~
* ~~Try to rotate again when next to wall~~
* ~~Implement hard drop~~
* ~~Implement hold~~
* ~~Implement levels~~
