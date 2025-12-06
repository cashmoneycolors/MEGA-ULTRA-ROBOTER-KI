param([string]$Name = "neue_datei.txt")
$path = "$env:USERPROFILE\Desktop\$Name"
New-Item -Path $path -ItemType File -Force
code $path
