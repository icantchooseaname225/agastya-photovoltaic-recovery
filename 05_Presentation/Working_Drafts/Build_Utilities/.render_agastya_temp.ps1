$ErrorActionPreference = 'Stop'
$inputFile = 'D:\Agastya\05_Presentation\Existing_Presentations\Agastya_Presentation_Enhanced.pptx'
$outputFile = 'D:\Agastya\05_Presentation\Working_Drafts\Build_Utilities\Agastya_Presentation_Enhanced_QA.pdf'
$app = New-Object -ComObject PowerPoint.Application
$app.Visible = -1
$pres = $app.Presentations.Open($inputFile, -1, 0, 0)
$pres.ExportAsFixedFormat($outputFile, 2)
$pres.Close()
$app.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($pres) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
Write-Output "Rendered $outputFile"


