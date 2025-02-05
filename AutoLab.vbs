Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName
driveLetter = Left(scriptPath, 2)

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c cd \ && " & driveLetter & "\autolab\venv\Scripts\python.exe " & driveLetter & "\autolab\project\interface.py", 0, False