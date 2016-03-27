; Use delays for keypresses to mimic natural behaviour
SetKeyDelay, 50, 0

;Exact matching
SetTitleMatchMode, 3

; Don't do anything if CS:GO isn't active
IfWinActive, Counter-Strike: Global Offensive
{
    ; Contains matching
    SetTitleMatchMode, 2

    ; Activate Twitch window and set it to play in fullscreen
    IfWinExist, - Twitch
    {
        WinActivate,

        ; Tabbing out of CS:GO may be slow so wait for it for 10 seconds
        WinWaitActive, , , 10

        ; If we managed to escape CS:GO
        IfEqual, ErrorLevel, 0
        {
            WinGetPos, X, Y, Width, Height, - Twitch

            ; Click near the middle to gain focus but try to avoid the unpause button
            MouseMove, Width/2 - 100, Height/2 - 100, 10
            Click,

            SendInput, {Space}

            ; Set Twitch to fullscreen if that's requested
            IniRead, UseFullscreen, ./potatoes/TwitchPotato.ini, Twitch, fullscreen

            IfEqual, UseFullscreen, yes
            {
                ; Double-click in the middle of the browser window to fullscreen the video player
                MouseMove, Width/2, Height/2, 10
                Click 2

                ; Do the mousemove just in case so that the cursor fades away if it wouldn't otherwise
                MouseMove, 1, 1, 1, R
            }

            ; Move the mouse out of the way when not in fullscreen
            IfNotEqual, UseFullscreen, yes
            {
                MouseMove, 0, 0, 0
            }
        }
    }
}