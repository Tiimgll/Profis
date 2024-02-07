# ВОЗВРАТ

1. Открыть PowerShell, который в папке, от имени администратора.
2. Скопировать скрипт ниже, вставить в PowerShell и запустить.

Get-AppXPackage -allusers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register "$($_.InstallLocation)\AppXManifest.xml"}
