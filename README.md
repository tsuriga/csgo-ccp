# CS:GO Casual Couch Potato - CSGO-CCP v1.0.0

Keep getting yourself killed early into the rounds and can't be bothered to
watch the rest of the round play out but don't want to miss out on any action
when a new round starts? Boy have I got the tool for you right here! This CS:GO
Game State Integration program can tab you out of CS:GO automagically and into
the procrastination activity of your choosing when you die, and back in to CS:GO
when a new round begins.

You can create your own AutoHotkey scripts to decide what happens during your
timeout from the game. If you download the binary build, it includes Netflix and
Twitch potato programs that switch to resume your currently paused Netflix show
or Twitch stream when you die and pause it before tabbing back to CS:GO when a
new round starts.

[Binary download ](https://www.dropbox.com/s/jcv7s96k8wgqtkd/csgo-ccp-v1.1.0.zip?dl=0)

MD5 signature of *csgo-ccp-v1.1.0.zip*: **e56b77b9feeccffdf9aa51c218ed7636**

You can use something like [RapidCRC](http://rapidcrc.sourceforge.net/) to
verify the signature.

Scroll down for [usage guide](#usage-instructions).

**WARNING!** Potato programs are likely to make assumptions on window titles and
active windows. They search for windows based on their titles and emulate
keyboard presses and mouse clicks on your system. For example the Netflix potato
program will attempt to find a window starting with the title "Netflix", and
emit keypresses and mouseclicks assuming that those peripheral inputs land on
the browser window to resume/pause and enter/exit full screen mode.

This means that if you have multiple windows matching the search criterion or
other programs running that pop up to foreground on their own, or you are simply
doing something else manually when the potato programs run, it is possible to
inadvertently feed input to the wrong window. This could cause you to e.g. click
a button you don't want to click or send a message you don't want to send.

You can check all the source files and build them from source to make sure they
work exactly (or as close to) as you'd expect.

**Only use the program if you understand these pitfalls!**

**NOTE!** Not tested on Community servers. Probably does not work. I also have
no idea how this handles timeouts (they probably won't break anything but there
is no functionality to tab out&in during opponent's timeout or anything).

Windows only at the moment due to AutoHotkey. If there is great demand from *nix
users I might try to recreate this in Java (or some AHK equivalent for *nix). I
built this on a 64-bit system, let me know if this doesn't work on 32-bit.

Comments, suggestions, error reports, and especially new potato scripts for HBO,
Viaplay, YouTube, etc. in the form of push requests are more than welcome.


## Usage instructions

0. Set up configurations in *config.ini*. If you need to change the server port,
   make sure to change it in *gamestate_integration_csgo-ccp.cfg* as well.
1. Copy the *gamestate_integration_csgo-ccp.cfg* to your CS:GO config folder
   (normally *Steam\SteamApps\common\Counter-Strike Global Offensive\csgo\cfg*).
2. Prepare the requirements of the potato program you're using (see below).
3. Build the .ahk AutoHotkey scripts into executables if you're running the
   programme from source and not the pre-built binaries.
4. Run `csgo-ccp.bat` (or `python csgo-ccp.py` under *src/* for the source
   version).
5. Run CS:GO and join a game.
6. When you quit CS:GO, you can quit *csgo-ccp* with Ctrl+C.

### Netflix potato set up

0. Set up configurations in *src\potatoes\NetflixPotato.ini*.
1. Log into Netflix (I only tested on Chrome and Firefox).
2. Pick a title to watch. Hit play and set it on pause.
3. Leave the browser with the Netflix tab open.

**Note!** If you use Silverlight to play Netflix media, the playback will time
out when left on pause for too long. When it does, Netflix potato doesn't know
how to resume the playback anymore. The HTML5 player will not time out so I
would suggest using that if possible.

### Twitch potato set up

0. Set up configurations in *src\potatoes\TwitchPotato.ini*.
1. Open up a Twitch stream in a browser (I only tested in Chrome). Make sure
   it's on a channel page and not on Twitch front page, i.e., the address should
   be twitch.tv/channelname.
2. Make sure the area in which the video is playing reaches the middle of the
   window because the potato program will rely on clicking near the middle of
   the browser window to gain the video player's focus.
3. Pause the stream and leave the browser tab with the Twitch channel open.

**Note!** I don't know how this functions with the Twitch HTML5 player. Maybe
just fine?


## How it works

You'll run a server program on your computer and tell your CS:GO client to send
information from your game to the server. From that information the server will
determine when you die and when a new round begins, and run programs at death
and respawn. You can configure the exact potato program execution phases and
which program to execute upon the forementioned events via a config file.


## Modifications

You can build your own potato programs by installing AutoHotkey and compiling
AHK scripts. If you wish to modify the potato server itself you'll need
*Python 3.4* (later versions are not supported by py2exe) and
*cx_Freeze >= 4.3.4* or *py2exe >= 0.9.2.2* for compiling the server.

- [AutoHotkey](https://www.autohotkey.com/)
- [Python >= 3.4](https://www.python.org/)
- [cx_Freeze >= 4.3.4](http://cx-freeze.sourceforge.net/)
- [py2exe >= 0.9.2.2](https://pypi.python.org/pypi/py2exe)
- [Quick Start Guide to CS:GO GSI](https://github.com/tsuriga/csgo-gsi-qsguide)

### Building

- **Potato programs:** Right-Click on *MyScript.ahk* and choose *Compile Script*
- **Potato server:** `build_exe csgo-ccp.py` or
`cxfreeze csgo-ccp.py --target-dir dist -c -O -OO`

If you encounter errors during potato server build, make sure you have *py2exe*
(*build_exe.exe*) installed in the correct Python version's Script folder and
that same folder in your Windows PATH. For example I have Python versions 2.7
and 3.4 installed, and I've named Python 3's executable to *python3.exe*, so I
installed py2exe via pip by calling `python3 -m pip install py2exe`. As for
cxfreeze make sure you have cxfreeze.bat file in your Python version's Script
folder. If not, you can generate that by running `python cxfreeze-postinstall`
(and possibly fixing the newly created .bat files if you have renamed your
Python executable).


## Changelog

v0.1.1 (2016-03-27): First release

## About

- **Author:** tsuriga, 2018
- **License:** MIT

*-Are you a wizard? -Yes.*
