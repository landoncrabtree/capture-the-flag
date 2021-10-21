$bytes = [System.IO.File]::ReadAllBytes('chairman')

$prev = [byte] 173

$dec = $(for ($i = 0; $i -lt $bytes.length; $i++) {
    $prev = $bytes[$i] -bxor $prev
    $prev
})

Write-Output([System.Text.Encoding]::UTF8.GetString($dec))
#iex([System.Text.Encoding]::UTF8.GetString($dec))