Param()

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

Function Get-FrontMatter {
  Param([string]$Path)
  $lines = Get-Content -Encoding UTF8 $Path -ErrorAction Stop
  $i1 = ($lines | Select-String -Pattern '^---\s*$' | Select-Object -First 1).LineNumber
  $i2 = ($lines | Select-String -Pattern '^---\s*$' | Select-Object -Skip 1 -First 1).LineNumber
  if (-not $i1 -or -not $i2 -or $i2 -le $i1) { return @{} }
  $front = $lines[($i1) .. ($i2-2)]
  $dict = @{}
  foreach ($line in $front) {
    if ($line -match '^(\w+):\s*(.*)$') {
      $k = $matches[1]
      $v = $matches[2].Trim()
      if ($v -eq 'null') { $v = $null }
      elseif ($v -match '^[0-9]+$') { $v = [int]$v }
      elseif ($v.StartsWith('"') -and $v.EndsWith('"')) { $v = $v.Trim('"') }
      $dict[$k] = $v
    }
  }
  return $dict
}

$rows = @()
Get-ChildItem -Path (Join-Path $RootDir 'scenes') -File -Filter '*.md' | ForEach-Object {
  $fm = Get-FrontMatter -Path $_.FullName
  if ($fm.Count -gt 0) {
    $rows += [PSCustomObject]@{
      Chapter = [int]$fm['chapter']
      Scene = [int]$fm['scene']
      ChapterTitle = $fm['chapter_title']
      SceneTitle = $fm['title']
      Words = [int]$fm['word_count']
      ReadMin = [int]$fm['reading_time_min']
      File = ('scenes/' + $_.Name)
    }
  }
}

$rows = $rows | Sort-Object Chapter, Scene
$totalScenes = $rows.Count
$totalWords = ($rows | Measure-Object -Property Words -Sum).Sum
$totalRead = ($rows | Measure-Object -Property ReadMin -Sum).Sum

$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('# Scenes Inventory')
[void]$sb.AppendLine()
[void]$sb.AppendLine('A quick reference of all scenes.')
[void]$sb.AppendLine()
[void]$sb.AppendLine('| Ch | Sc | Chapter | Scene | Words | Read (min) | File |')
[void]$sb.AppendLine('|---:|---:|---|---|---:|---:|---|')
foreach ($r in $rows) {
  $line = "| {0} | {1} | {2} | {3} | {4} | {5} | [{6}]({6}) |" -f `
    $r.Chapter, $r.Scene, $r.ChapterTitle, $r.SceneTitle, $r.Words, $r.ReadMin, $r.File
  [void]$sb.AppendLine($line)
}
[void]$sb.AppendLine()
[void]$sb.AppendLine(("Total scenes: {0}  " -f $totalScenes))
[void]$sb.AppendLine(("Total words: {0}" -f $totalWords))
[void]$sb.AppendLine(("Total reading time (min): {0}" -f $totalRead))

Set-Content -Encoding UTF8 -NoNewline -Path (Join-Path $RootDir 'scenes_inventory.md') -Value $sb.ToString()
