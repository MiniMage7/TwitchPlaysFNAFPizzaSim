# Twitch Chat Play Pizza Sim
A bot that takes twitch chat messages and makes them into game actions

## Notes before running
Replace all variables at the top of the program as needed.  
Specifically, oauthToken, clientSecret, twitchChannels, and moderators.

## How to use for Moderators
- "?start **0.0**" - starts the game actions. The number is the amount of seconds between actions
- "?stop" - stops the game actions.
- "?changeSpeed **0.0**" - Changes game action interval. Note: this works by basically executing the stop and then start commands, so votes may be lost in this process
- "?mode **name**" - switch between different parts of the game. Valid modes are "night", "salvage", "shop", "game", and "wasd". The program defaults to "night" when started. Note: "wasd" had vastly different behaviour
- "?disable **command**" - disables the specific command until it is re-enabled
- "?enable **command**" - enables a disabled command
- "?enableall" - enables all commands

## How to use for chatters
Chatters can cause game actions by typing one of the many actions (in the above twitch chat). I listed all the current commands here. They do NOT have to put a ? or ! at the start of their message.

#### In night mode
- left vent - looks at left vent
- right vent - looks at right vent
- computer - looks at computer
- motion detector - opens motion detector tab and turns it on
- audio left - opens audio lure tab and set left lure
- audio right - opens audio lure tab and set right lure
- silent vent - opens silent vent tab and turns it on
- boop - boop
- mute - presses the mute button (n1)
- computer power - toggles computer power
- toggle fan - toggles fan
- skip ad - hits all the possible skip ad places (currently only has the first ad)
- tasks - opens the tasks tab
- order supplies - opens task tab, opens order supplies tab, clicks all the order supplies actions (this means this will basically do the bottom most undone task)
- advertising - see above
- maintenance - see above
- buy printer - opens task tab, opens equipment tab, buys printer upgrade
- upgrade internet - opens task tab, opens equipment tab, buys internet upgrade
- hire handyman - opens task tab, opens equipment tab, buys handyman upgrade
- logout - opens task tab and clicks logout
- enter - hits the enter key
- wait - does nothing

#### In salvage mode
- start salvage - clicks start salvage button
- skip salvage - throws the animatronic back into the alley
- skip - clicks the skip button for the dialogue
- paper - flicks the paper up and down quickly
- zap - zaps the animatronic
- space - hits the space bar
- enter - hits the enter key
- wait - does nothing

#### In shop mode
- next item - clicks right arrow in catalog menu
- previous item - clicks left arrow in catalog menu
- buy - clicks the buy item button
- dumpster - clicks the dumpster diver catalog
- stans - clicks the Stan's catalog
- smiles - clicks the smiles catalog
- rare - clicks the rare finds catalog
- blueprint - clicks the button to change to blueprint mode
- catalog - clicks the button to change to catalog mode
- mute - clicks the button to mute the voice in the shop
- sponsorship - clicks the sponsorship and accept sponsorship buttons
- floor plan - clicks the upgrade floor plan button
- space - hits the space bar
- enter - hits the enter key
- wait - does nothing

#### In game mode
- space - hits the space bar
- random duck - moves the mouse to a random duck in the duck pond
- click - clicks the mouse in the current position (to be used with the above command)
- wait - does nothing

## Notes for wasd mode
This mode has some vastly different behaviour due to the need for quick responses in this mode. It does not use the voting system for commands and therefore stops votes. It also will not allow you to restart the votes while in this mode. Instead, every command sent in chat will be executed immediately, and that command will last until the next chatter provides a command. Changing out of this mode will release all held keys automatically. You will also have to rerun the ?start command after leaving this mode if you want to start another mode. Running the ?stop command while in this mode will also switch the mode to night mode, as there is no way to "stop" this mode

- up - holds the w key until the next up/left/down/right command
- left - holds the a key until the next up/left/down/right command
- down - holds the s key until the next up/left/down/right command
- right - holds the d key until the next up/left/down/right command
- shift up - releases the held shift key
- shift down - holds the shift key
- stop - removes the current up/left/down/right commands

## Extra Notes
Make sure the game is in focus, it uses your actual computer mouse and keyboard to play.
To close the bot, type ctrl c in the console window or close it. The bot will also die if it tries to move the mouse and your mouse is in the corner of your screen (fail safe)

### Credits
Made by Katarina aka Winterveil  
Discord: seasonsveil  