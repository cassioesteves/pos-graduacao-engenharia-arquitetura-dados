$HadoopBin = "l:\pos-graduacao-engenharia-arquitetura-dados\Hadoop\bin"
Force-mkdir $HadoopBin

# URLs for Hadoop 3.3.5 (compatible with Spark 3.5/Hadoop 3.4 usually)
# Using cdarlint repo which is a standard source for these binaries
$BaseUrl = "https://github.com/cdarlint/winutils/blob/master/hadoop-3.2.2/bin"
$WinutilsUrl = "$BaseUrl/winutils.exe?raw=true"
$HadoopDllUrl = "$BaseUrl/hadoop.dll?raw=true"

Write-Host "Downloading winutils.exe..."
Invoke-WebRequest -Uri $WinutilsUrl -OutFile "$HadoopBin\winutils.exe"

Write-Host "Downloading hadoop.dll..."
Invoke-WebRequest -Uri $HadoopDllUrl -OutFile "$HadoopBin\hadoop.dll"

Write-Host "Download complete. Files placed in $HadoopBin"
Write-Host "Please ensure your antivirus doesn't block winutils.exe"
