; Exact matching
SetTitleMatchMode, 3

; Don't do anything if CS:GO isn't active
IfWinActive, Counter-Strike: Global Offensive
{
    ; Starts-with matching
    SetTitleMatchMode, 1

    ; Activate Netflix window and set it to play in fullscreen
    IfWinExist, Netflix
    {
        WinActivate, Netflix

        ; Tabbing out of CS:GO may be slow so wait for it for 10 seconds
        WinWaitActive, Netflix, , 10

        ; If we managed to escape CS:GO
        IfEqual, ErrorLevel, 0
        {
            ; Check if we're using Silverlight for playback
            IniRead, UseSilverlight, ./potatoes/NetflixPotato.ini, Netflix, silverlight

            WinGetPos, X, Y, Width, Height, Netflix

            ; Set Netflix to fullscreen if that's requested
            IniRead, UseFullscreen, ./potatoes/NetflixPotato.ini, Netflix, fullscreen

            IfEqual, UseFullscreen, yes
            {
                IfEqual, UseSilverlight, yes
                {
                    ; Click in the Netflix window to focus it
                    MouseMove, Width/2 - 10, Height/2 - 10, 20
                    Click,
                }

                ; Sleep for a moment to mimic somewhat natural behaviour
                Sleep, 50

                ; Go fullscreen
                SendInput, f

                ; Move the mouse a bit so that it'll go away on Firefox+HTML5
                MouseMove, 1, 1, 1, R
            }

            ; Unpause the show
            IfEqual, UseSilverlight, yes
            {
                ; Click in the Netflix window to focus it
                MouseMove, Width/2 + 10, Height/2 + 10, 20
                Click,
            }
            SendInput, {Space}

            ; Move the mouse out of the way when not in fullscreen
            IfNotEqual, UseFullscreen, yes
            {
                MouseMove, 0, 0, 0
            }
        }
    }
}