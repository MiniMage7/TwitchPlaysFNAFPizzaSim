# This only works on 1920x1080

from twitchio.ext import commands
from twitchio.ext import routines
import pyautogui
import random

OauthToken = 'PUT_YOUR_TOKEN_HERE'
clientSecret = 'PUT_YOUR_CLIENT_SECRET_HERE'
botPrefix = '?'
twitchChannels = ["#TWITCH_CHANNEL_1"]

moderator = 'TWITCH_USERNAME_MODERATOR'
moderator2 = 'TWITCH_USERNAME_MODERATOR2'

# Possible Commands
nightVoteInfo = {
    "left vent": 0,
    "right vent": 0,
    "computer": 0,
    "motion detector": 0,
    "audio left": 0,
    "audio right": 0,
    "silent vent": 0,
    "boop": 0,
    "mute": 0,
    "computer power": 0,
    "toggle fan": 0,
    "skip ad": 0,
    "tasks": 0,
    "order supplies": 0,
    "advertising": 0,
    "maintenance": 0,
    "buy printer": 0,
    "upgrade internet": 0,
    "hire handyman": 0,
    "logout": 0,
    "enter": 0,
    "wait": 0
}

salvageVoteInfo = {
    "start salvage": 0,
    "skip salvage": 0,
    "paper": 0,
    "zap": 0,
    "skip": 0,
    "enter": 0,
    "space": 0,
    "wait": 0
}

shopVoteInfo = {
    "next item": 0,
    "previous item": 0,
    "buy": 0,
    "dumpster": 0,
    "stans": 0,
    "smiles": 0,
    "rare": 0,
    "blueprint": 0,
    "catalog": 0,
    "mute": 0,
    "sponsorship": 0,
    "floor plan": 0,
    "enter": 0,
    "space": 0,
    "wait": 0
}

gameVoteInfo = {
    "space": 0,
    "random duck": 0,
    "click": 0,
    "wait": 0
}

disabledCommands = []

totalRequests = 0
moveCycle = 5.0
position = 'computer'
botMode = 'night'
keyPressed = 'none'

class Bot(commands.Bot):

    # Creates the bot
    def __init__(self):
        super().__init__(token=OauthToken, client_secret=clientSecret, prefix=botPrefix, initial_channels=twitchChannels)

    # Runs when bot is ready
    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    # Adds chat votes
    async def event_message(self, ctx):
        global totalRequests
        global disabledCommands
        messageText = ''

        if ctx.echo:
            return

        # This try might be unnecessary, but since the bot sees itself as having no author,
        # I'm worried it'll break with other bots, so this just makes sure that every message
        # has an author. If someone tests this and tells me its unnecessary, I'll remove it
        try:
            ctx.author
        except:
            return

        # Checks if vote is allowed
        try:
            messageText = ctx.content.lower()

            if messageText in disabledCommands:
                return
        except:
            await bot.handle_commands(ctx)

        # If it's night, checks if vote is valid
        if botMode == 'night':
            try:
                global nightVoteInfo
                nightVoteInfo.update({messageText: nightVoteInfo[messageText] + 1})

                totalRequests += 1
            except:
                await bot.handle_commands(ctx)

        # If it's salvage, checks if vote is valid
        elif botMode == "salvage":
            try:
                global salvageVoteInfo
                salvageVoteInfo.update({messageText: salvageVoteInfo[messageText] + 1})

                totalRequests += 1
            except:
                await bot.handle_commands(ctx)

        # If it's shop, checks if vote is valid
        elif botMode == "shop":
            try:
                global shopVoteInfo
                shopVoteInfo.update({messageText: shopVoteInfo[messageText] + 1})

                totalRequests += 1
            except:
                await bot.handle_commands(ctx)

        # If it's game, checks if vote is valid
        elif botMode == "game":
            try:
                global gameVoteInfo
                gameVoteInfo.update({messageText: gameVoteInfo[messageText] + 1})

                totalRequests += 1
            except:
                await bot.handle_commands(ctx)

        # If it's wasd, do wasd commands as soon as they're sent
        elif botMode == "wasd":
            match messageText:
                case "up":
                    pressW()
                case "left":
                    pressA()
                case "down":
                    pressS()
                case "right":
                    pressD()
                case "shift up":
                    pyautogui.keyUp('shift')
                case "shift down":
                    pyautogui.keyDown('shift')
                case "stop":
                    releaseKeys()
                    global keyPressed
                    keyPressed = 'none'
                case _:
                    await bot.handle_commands(ctx)


    # Start the game bot
    @commands.command()
    async def start(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        # Get the time between moves and start the routine
        try:
            message = ctx.message.content
            global botPrefix
            message = message.replace(botPrefix, '')
            message = message.replace('start', '')
            message = message.strip()

            global botMode

            if botMode == 'wasd':
                await ctx.send("Failed to start. You can't start in wasd mode.")
                return

            global moveCycle
            moveCycle = float(message)
            print("Game Actions Started")
            print("Current Mode: " + botMode)
            print("Current Interval: " + str(moveCycle))

            resetVotes()
            takeGameAction.start()
            takeGameAction.change_interval(seconds=moveCycle)
        except:
            await ctx.send("Failed to start. Remember to put your interval")

    # Stop the game actions
    @commands.command()
    async def stop(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        global botMode
        if botMode == 'wasd':
            botMode = 'night'

        print("Game Actions Stopped")
        print("Current Mode: " + botMode)
        print("Current Interval: " + str(moveCycle))

        try:
            takeGameAction.stop()
        except:
            pass

    # Changes command execution interval
    @commands.command()
    async def changeSpeed(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        # Get the time between moves and start the routine
        try:
            message = ctx.message.content
            global botPrefix
            message = message.replace(botPrefix, '')
            message = message.replace('changeSpeed', '')
            message = message.strip()

            global moveCycle
            global botMode
            moveCycle = float(message)
            takeGameAction.change_interval(seconds=moveCycle)
            print("Command Interval Edited")
            print("Current Mode: " + botMode)
            print("Current Interval: " + str(moveCycle))
        except:
            await ctx.send("Failed to edit interval, if the bot is off, try setting the interval with ?start")

    # Sets the bot mode
    @commands.command()
    async def mode(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        try:
            message = ctx.message.content
            global botMode
            message = message.replace(botPrefix, '')
            message = message.replace('mode', '')
            message = message.strip().lower()

            # Check if it's an allowed mode
            allowedBotModes = ['night', 'salvage', 'shop', 'game', 'wasd']

            if message in allowedBotModes:
                # If the bot was in wasd mode, make sure no keys are still pressed
                if botMode == 'wasd':
                    releaseKeys()
                    pyautogui.keyUp('shift')
                    global keyPressed
                    keyPressed = 'none'

                botMode = message
            else:
                await ctx.send("Failed to change mode. Possible modes: night, salvage, shop, game, wasd")
                return

            print("Bot mode set to " + botMode)
            if botMode == 'wasd':
                print("This stopped the recurring votes to operate")
                print("To restart votes, switch out of this mode and run the ?start command")
                try:
                    takeGameAction.stop()
                except:
                    pass
        except:
            await ctx.send("Failed to change mode.")

    # Enables a disabled command
    @commands.command()
    async def enable(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        try:
            message = ctx.message.content
            global botMode
            message = message.replace(botPrefix, '')
            message = message.replace('enable', '')
            message = message.strip().lower()

            global disabledCommands
            disabledCommands.remove(message)
            print("\nEnabled command " + message)
        except:
            await ctx.send("Failed to enable " + message)

    # Disables a command
    @commands.command()
    async def disable(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        try:
            message = ctx.message.content
            global botMode
            message = message.replace(botPrefix, '')
            message = message.replace('disable', '')
            message = message.strip().lower()

            global disabledCommands

            if message in disabledCommands:
                print("\nCommand is already disabled.")
                return

            disabledCommands.append(message)
            print("\nDisabled command " + message)
        except:
            await ctx.send("Failed to disable " + message)

    # Enables all commands
    @commands.command()
    async def enableall(self, ctx: commands.Context):
        # Check that the person running the command has permission
        if not checkPerms(ctx):
            return

        global disabledCommands
        disabledCommands = []
        print("\nEnabled all commands.")


# Bot does action every cycle
@routines.routine(seconds=moveCycle)
async def takeGameAction():
    proccessVotes()
    resetVotes()


# Check that the person running a command has permission
def checkPerms(ctx):
    try:
        if ctx.author.name.lower() != moderator and ctx.author.name.lower() != moderator2:
            return False
    except:
        return False
    return True

# Resets all the votes
def resetVotes():
    global totalRequests
    totalRequests = 0

    global nightVoteInfo
    for x in nightVoteInfo:
        nightVoteInfo.update({x: 0})

    global salvageVoteInfo
    for x in salvageVoteInfo:
        salvageVoteInfo.update({x: 0})

    global shopVoteInfo
    for x in shopVoteInfo:
        shopVoteInfo.update({x: 0})

    global gameVoteInfo
    for x in gameVoteInfo:
        gameVoteInfo.update({x: 0})


# Count votes and call corresponding function
def proccessVotes():
    mostVoted = "wait"
    mostVotes = 0

    if botMode == 'night':
        global nightVoteInfo

        for x in nightVoteInfo:
            if nightVoteInfo[x] > mostVotes:
                mostVoted = x
                mostVotes = nightVoteInfo[x]

        print("\nExecuting " + mostVoted)
        print(str(mostVotes) + " / " + str(totalRequests))

        # This massive switch case is for calling each function for night mode
        match mostVoted:
            case "left vent":
                leftVent()
            case "right vent":
                rightVent()
            case "computer":
                lookAtComputer()
            case "motion detector":
                motionDetector()
            case "audio left":
                leftAudio()
            case "audio right":
                rightAudio()
            case "silent vent":
                silentVent()
            case "boop":
                boop()
            case "mute":
                muteNightVoice()
            case "computer power":
                computerPower()
            case "toggle fan":
                toggleFan()
            case "skip ad":
                skipAd()
            case "tasks":
                tasks()
            case "order supplies":
                orderSupplies()
            case "advertising":
                advertising()
            case "maintenance":
                maintenance()
            case "buy printer":
                buyPrinter()
            case "upgrade internet":
                upgradeInternet()
            case "hire handyman":
                hireHandyman()
            case "logout":
                logout()
            case "enter":
                enter()
            case "wait":
                pass
            case _:
                print("Something broke; tell Kat what you did to get here")

    elif botMode == 'salvage':
        global salvageVoteInfo

        for x in salvageVoteInfo:
            if salvageVoteInfo[x] > mostVotes:
                mostVoted = x
                mostVotes = salvageVoteInfo[x]

        print("\nExecuting " + mostVoted)
        print(str(mostVotes) + " / " + str(totalRequests))

        # This massive switch case is for calling each function for salvage mode
        match mostVoted:
            case "start salvage":
                startSalvage()
            case "skip salvage":
                skipSalvage()
            case "skip":
                skipSalvageDialogue()
            case "paper":
                flickPaper()
            case "zap":
                zap()
            case "enter":
                enter()
            case "space":
                space()
            case "wait":
                pass
            case _:
                print("Something broke; tell Kat what you did to get here")

    elif botMode == 'shop':
        global shopVoteInfo

        for x in shopVoteInfo:
            if shopVoteInfo[x] > mostVotes:
                mostVoted = x
                mostVotes = shopVoteInfo[x]

        print("\nExecuting " + mostVoted)
        print(str(mostVotes) + " / " + str(totalRequests))

        # This massive switch case is for calling each function for shop mode
        match mostVoted:
            case "next item":
                nextShopItem()
            case "previous item":
                previousShopItem()
            case "buy":
                buyShopItem()
            case "dumpster":
                dumpsterCatalog()
            case "stans":
                stansCatalog()
            case "smiles":
                smilesCatalog()
            case "rare":
                rareCatalog()
            case "blueprint":
                blueprintMode()
            case "catalog":
                catalogMode()
            case "mute":
                muteShop()
            case "sponsorship":
                takeSponsorship()
            case "floor plan":
                upgradeFloorPlan()
            case "enter":
                enter()
            case "space":
                space()
            case "wait":
                pass
            case _:
                print("Something broke; tell Kat what you did to get here")

    elif botMode == 'game':
        global gameVoteInfo

        for x in gameVoteInfo:
            if gameVoteInfo[x] > mostVotes:
                mostVoted = x
                mostVotes = gameVoteInfo[x]

        print("\nExecuting " + mostVoted)
        print(str(mostVotes) + " / " + str(totalRequests))

        # This massive switch case is for calling each function for game mode
        match mostVoted:
            case "space":
                space()
            case "random duck":
                randomDuck()
            case "click":
                pyautogui.click()
            case "wait":
                pass
            case _:
                print("Something broke; tell Kat what you did to get here")



# Individual night actions
def leftVent():
    pyautogui.moveTo(0, 500)
    global position
    position = "left vent"

def rightVent():
    pyautogui.moveTo(1900, 500)
    global position
    position = "right vent"

def lookAtComputer():
    global position
    if position == "left vent":
        pyautogui.moveTo(1900, 500)
    elif position == "right vent":
        pyautogui.moveTo(0, 500)

    pyautogui.moveTo(1000, 500)
    position = "computer"

def motionDetector():
    pyautogui.click(1050, 435)
    pyautogui.click(1350, 920)

def leftAudio():
    pyautogui.click(1230, 435)
    pyautogui.click(870, 680)

def rightAudio():
    pyautogui.click(1230, 435)
    pyautogui.click(1430, 680)

def silentVent():
    pyautogui.click(1400, 435)
    pyautogui.click(1400, 915)

def boop():
    pyautogui.click(890, 140)

def muteNightVoice():
    pyautogui.click(960, 35)

def computerPower():
    pyautogui.keyDown('z')
    pyautogui.sleep(.1)
    pyautogui.keyUp('z')

def toggleFan():
    pyautogui.keyDown('x')
    pyautogui.sleep(.1)
    pyautogui.keyUp('x')

def skipAd():
    # First and fourth ad
    pyautogui.click(1310, 900)
    # Second and third ad
    pyautogui.click(1320, 710)
    # Fifth ad
    pyautogui.click(980, 870)

def tasks():
    pyautogui.click(900, 435)

def orderSupplies():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 555)
    pyautogui.PAUSE = .01
    pyautogui.click(980, 530)
    pyautogui.click(980, 570)
    pyautogui.click(980, 620)
    pyautogui.click(980, 665)
    pyautogui.click(980, 710)
    pyautogui.PAUSE = .1

def advertising():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 600)
    pyautogui.PAUSE = .01
    pyautogui.click(980, 530)
    pyautogui.click(980, 570)
    pyautogui.click(980, 620)
    pyautogui.PAUSE = .1

def maintenance():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 645)
    pyautogui.PAUSE = .01
    pyautogui.click(980, 530)
    pyautogui.click(980, 570)
    pyautogui.click(980, 620)
    pyautogui.PAUSE = .1

def buyPrinter():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 690)
    pyautogui.click(980, 530)

def upgradeInternet():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 690)
    pyautogui.click(980, 570)

def hireHandyman():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 690)
    pyautogui.click(980, 620)

def logout():
    pyautogui.click(900, 435)
    pyautogui.click(1140, 735)

def enter():
    pyautogui.keyDown('enter')
    pyautogui.sleep(.1)
    pyautogui.keyUp('enter')


# Individual salvage actions
def startSalvage():
    pyautogui.click(950, 550)

def skipSalvage():
    pyautogui.click(950, 390)

def skipSalvageDialogue():
    pyautogui.click(1830, 50)

def flickPaper():
    pyautogui.moveTo(960, 1050)
    pyautogui.moveTo(960, 500)
    pyautogui.sleep(.2)
    pyautogui.moveTo(960, 1050)
    pyautogui.moveTo(960, 500)

def zap():
    pyautogui.keyDown('ctrl')
    pyautogui.sleep(.1)
    pyautogui.keyUp('ctrl')

def space():
    pyautogui.keyDown('space')
    pyautogui.sleep(.1)
    pyautogui.keyUp('space')


# Individual shop actions
def nextShopItem():
    pyautogui.click(1535, 825)

def previousShopItem():
    pyautogui.click(1435, 825)

def buyShopItem():
    pyautogui.click(1400, 940)

def dumpsterCatalog():
    pyautogui.click(300, 200)

def stansCatalog():
    pyautogui.click(300, 300)

def smilesCatalog():
    pyautogui.click(300, 400)

def rareCatalog():
    pyautogui.click(300, 500)

def blueprintMode():
    pyautogui.click(1840, 360)

def catalogMode():
    pyautogui.click(50, 170)

def muteShop():
    pyautogui.click(165, 1030)

def takeSponsorship():
    pyautogui.click(1800, 225)
    pyautogui.click(1130, 890)

def upgradeFloorPlan():
    pyautogui.click(1790, 960)

# Individual game actions
def randomDuck():
    match random.randint(0, 15):
        case 0:
            pyautogui.moveTo(650, 190)
        case 1:
            pyautogui.moveTo(875, 195)
        case 2:
            pyautogui.moveTo(1165, 120)
        case 3:
            pyautogui.moveTo(450, 400)
        case 4:
            pyautogui.moveTo(740, 375)
        case 5:
            pyautogui.moveTo(1030, 410)
        case 6:
            pyautogui.moveTo(1285, 330)
        case 7:
            pyautogui.moveTo(740, 570)
        case 8:
            pyautogui.moveTo(1130, 585)
        case 9:
            pyautogui.moveTo(1460, 510)
        case 10:
            pyautogui.moveTo(475, 695)
        case 11:
            pyautogui.moveTo(710, 770)
        case 12:
            pyautogui.moveTo(1040, 730)
        case 13:
            pyautogui.moveTo(1365, 770)
        case 14:
            pyautogui.moveTo(795, 955)
        case 15:
            pyautogui.moveTo(1160, 930)

# Individual wasd actions
def pressW():
    global keyPressed
    if keyPressed == 'w':
        return
    releaseKeys()
    keyPressed = 'w'
    pyautogui.keyDown('w')

def pressA():
    global keyPressed
    if keyPressed == 'a':
        return
    releaseKeys()
    keyPressed = 'a'
    pyautogui.keyDown('a')

def pressS():
    global keyPressed
    if keyPressed == 's':
        return
    releaseKeys()
    keyPressed = 's'
    pyautogui.keyDown('s')

def pressD():
    global keyPressed
    if keyPressed == 'd':
        return
    releaseKeys()
    keyPressed = 'd'
    pyautogui.keyDown('d')

def releaseKeys():
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')


# Main
if __name__ == '__main__':
    random.seed()
    bot = Bot()
    bot.run()
