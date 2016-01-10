#The Playground of Yiggles
from path import Path
from plugins.info import PluginInfo
from messages import SayText2, HintText
from menus import SimpleMenu, SimpleOption, Text
from events import Event
from players.entity import Player
from players.helpers import index_from_userid, playerinfo_from_index, userid_from_playerinfo
from commands.say import SayCommand
from commands.client import ClientCommand, ClientCommandFilter
from commands.server import ServerCommand
from commands import CommandReturn

from colors import Color

from listeners.tick import Delay

from filters.recipients import RecipientFilter
 
from core import AutoUnload
 
base_path = Path(__file__).parent
MODNAME = base_path.namebase
 
info = PluginInfo()
info.author = "Yiggles Moto"
info.basename = MODNAME
info.description = "Testing Area"
info.name = "Playground - Work Area"
info.version = "0.1.2 Alpha"
info.url = ""
 
GOD_MODE = "god"
CHAT_COMMAND = "cut"
CLIENT_COMMAND = "kill"
HEALTH_COMMAND = "sethealth"
MENU_COMMAND = "menu"
RESPAWN_COMMAND = "respawn"

EXTRA_HP = 100
BOT_EXTRA_HP = 400

def load():
    SayText2('%s{0}%s: Plugin Loaded'.format(info.name) % (Color(0,153,0), Color(0,200,255))).send()

def unload():
    SayText2('{0}: Plugin Unloaded'.format(info.name)).send()
    
@Event("round_start")
def greeting(game_event):
    SayText2("Welcome to Yiggles' Zombie Mod").send()
    SayText2("Type !god for way too much health").send()

@Event("player_spawn")
def player_spawn(game_event):
        userid = game_event.get_int("userid")
        index = index_from_userid(userid)
        player = Player(index)
        playerinfo = playerinfo_from_index(index)
        if playerinfo.is_fake_client():
            player.health += BOT_EXTRA_HP
        else:
            player.health += EXTRA_HP

# @SayCommand(("team", "!team"))
# def team_switch(command, index, team_only):

@SayCommand(("/kill"))
def on_command(command, index, team_only):
    player = Player(index)

@Event("player_death")
def respawn_bots(game_event):
        userid = game_event.get_int("userid")
        index = index_from_userid(userid)
        player = Player(index)
        playerinfo = playerinfo_from_index(index)
        if playerinfo.is_fake_client():
            SayText2("Respawning {0}".format(player.name)).send()
            Delay(2, player=Player(index))
            player.respawn()

@SayCommand(("/{0}".format(RESPAWN_COMMAND), "!{0}".format(RESPAWN_COMMAND)))
def on_command(command, index, team_only):
    player = Player(index)
    player.respawn()
    if command[0][0] == "/":
        return CommandReturn.BLOCK
    

@SayCommand((MENU_COMMAND, "!{0}".format(MENU_COMMAND)))
def on_command(command, index, team_only):
    player = Player(index)

@Event("player_disconnect")
def on_event(game_event):
    userid = game_event.get_int("userid")
    index = index_from_userid(userid)
    player = Player(index)
    reason = game_event.get_string("reason")
    SayText2("%s {0} %shas left. Reason: \"%s{1}%s\"".format(player.name, reason) % (Color(0,153,0), Color(255,255,51), Color(255,255,255), Color(255,255,51))).send()
    return CommandReturn.BLOCK

@SayCommand((CHAT_COMMAND, "!{0}".format(CHAT_COMMAND)))
def on_command(command, index, team_only):
     player = Player(index)
     player.health -= 5
     try:
         command[1]
     except IndexError:
         cut_with = "knife"
     else:
         cut_with = command[1] 
     SayText2("{0} has cut themself with {1}".format(player.name, cut_with)).send()
     return CommandReturn.BLOCK

#Gives Player A Lot Of Health
@SayCommand((GOD_MODE, "!{0}".format(GOD_MODE)))
def on_command(command, index, team_only):
    player = Player(index)
    player.health += 99999999
    SayText2("{0} has activated god mode... Beware.".format(player.name)).send()


#Tells players when a player has been blinded
@Event("player_blind")
def stevie_wonder(game_event):
    userid = game_event.get_int("userid")
    index = index_from_userid(userid)
    player = Player(index)
    SayText2("{0} has been blinded by the light! Attack!".format(player.name)).send()
    
#Going To Make A Menu To Set Healths (just for practice) W.I.P.
@SayCommand((HEALTH_COMMAND, "!{0}".format(HEALTH_COMMAND)))
def on_command(command, index, team_only):
    player = Player(index)


#Don't let jerks kill hostages
@Event("hostage_killed")
def superhero(game_event):
    userid = game_event.get_int("userid")
    index = index_from_userid(userid)
    player = Player(index)
    if not player.isdead:
        player.say("I'm dumb and I kill hostages")
    
@ClientCommand(CLIENT_COMMAND)
def on_command(command, index, teamonly=False):
        player = Player(index)
        player.health -= 10
        SayText2('You can\'t commit suicide here...').send(index)
        return CommandReturn.BLOCK



from cvars import ConVar
from cvars.flags import FCVAR_NOTIFY

kill_as_convar = ConVar("kill", "", "", FCVAR_NOTIFY)