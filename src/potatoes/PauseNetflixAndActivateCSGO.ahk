; Starts-with matching
SetTitleMatchMode, 1

NetflixActive := false

; Get active window's title since Silverlight uses its own window in fullscreen
WinGetTitle, Title, A

; If Silverlight window is active, assume it's Netflix in fullscreen
; Could be some other program in fullscreen, but we can't easily know that
IfEqual, Title, Microsoft Silverlight
{
    NetflixActive := true
}

; With HTML5 playback it's the browser window that is active even in fullscreen
IfWinActive, Netflix
{
    NetflixActive := true
}

if NetflixActive
{
    ; Wait for the Netflix window to be active before acting on it
    ; This can take a moment when tabbing out of CS:GO just before a round ends
    WinActivate, Netflix
    WinWaitActive, Netflix, , 10

    ; If we have managed to escape CS:GO
    IfEqual, ErrorLevel, 0
    {
        ; Check if we're using Silverlight for playback
        IniRead, UseSilverlight, ./potatoes/NetflixPotato.ini, Netflix, silverlight

        IfEqual, UseSilverlight, yes
        {
            ; Click in the Netflix window to focus it
            WinGetPos, X, Y, Width, Height, Netflix
            MouseMove, Width/2 - 20, Height/2 - 20, 20
            Click,
        }

        ; Exit fullscreen (if on)
        SendInput, {Esc}

        IfEqual, UseSilverlight, yes
        {
            ; Click in the Netflix window to focus it
            WinGetPos, X, Y, Width, Height, Netflix
            MouseMove, Width/2 + 20, Height/2 + 20, 20
            Click,
        }

        ; Sleep for a moment to mimic somewhat natural behaviour
        Sleep, 50

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