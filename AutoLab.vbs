Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName
driveLetter = Left(scriptPath, 2)

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd \ && " & driveLetter & "\bats-fiap\venv\Scripts\python.exe " & driveLetter & "\bats-fiap\project\interface.py", 0, False