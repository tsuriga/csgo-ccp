; Use delays for keypresses to mimic natural behaviour
SetKeyDelay, 50, 0

; Contains matching
SetTitleMatchMode, 2

; Only act if Twitch window is active and opened to a specific channel
IfWinActive, - Twitch
{
    ; Wait for the Twitch window to be active before acting on it
    ; This can take a moment when tabbing out of CS:GO just before a round ends
    WinActivate, - Twitch
    WinWaitActive, , , 10

    ; If we have managed to escape CS:GO
    IfEqual, ErrorLevel, 0
    {
        ; Click in the Twitch window gain focus
        WinGetPos, X, Y, Width, Height, - Twitch
        MouseMove, Width/2 - 80, Height/2 - 80, 10
        Click,

        ; Exit fullscreen (if on)
        SendInput, {Esc}

        ; Click again to make sure we have focus
        WinGetPos, X, Y, Width, Height, - Twitch
        MouseMove, Width/2 - 120, Height/2 - 80, 10
        Click,

        ; Pause video
        SendInput, {Space}
    }
}

; Exact matching
SetTitleMatchMode, 3

; Activate CS:GO window if not already active
IfWinNotActive, Counter-Strike: Global Offensive
{
    WinActivate, Counter-Strike: Global Offensive
}