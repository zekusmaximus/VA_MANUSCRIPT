Param()

$RootDir = Split-Path -Parent $PSScriptRoot
"RootDir=$RootDir" | Out-File -Encoding UTF8 -FilePath (Join-Path $PSScriptRoot 'normalize-scenes.log')
Set-Location $RootDir

Function Get-ChapterMap {
  $map = @{}
  Get-ChildItem -Path (Join-Path $RootDir "chapters") -File | ForEach-Object {
    $lines = Get-Content -Encoding UTF8 -TotalCount 200 $_.FullName
    $i1 = ($lines | Select-String -Pattern '^---\s*$' -SimpleMatch:$false | Select-Object -First 1).LineNumber
    if (-not $i1) { return }
    $i2 = ($lines | Select-String -Pattern '^---\s*$' -SimpleMatch:$false | Select-Object -Skip 1 -First 1).LineNumber
    if (-not $i2) { return }
    $chapter = $null; $title = $null; $slug = $null
    for ($i = $i1; $i -lt ($i2-1); $i++) {
      $line = $lines[$i]
      if ($line -match '^chapter:\s*(.+)$') { $chapter = $matches[1].Trim('"') }
      elseif ($line -match '^title:\s*(.+)$') { $title = $matches[1].Trim('"') }
      elseif ($line -match '^slug:\s*(.+)$') { $slug = $matches[1].Trim('"') }
    }
    if ($chapter) { $map[$chapter] = @{ title = $title; slug = $slug } }
  }
  return $map
}

Function Get-SceneOrder {
  $scenes = Get-ChildItem -Path (Join-Path $RootDir "scenes") -File | ForEach-Object {
    $name = $_.BaseName
    if ($name -match '^ch(\d+)-sc(\d+)-(.+)$') {
      [PSCustomObject]@{
        Path = $_.FullName
        FileName = $_.Name
        Base = $name
        Chapter = [int]$matches[1]
        Scene = [int]$matches[2]
        Tail = $matches[3]
        Slug = $name
      }
    }
  } | Sort-Object Chapter, Scene
  return ,$scenes
}

Function Get-FrontMatterAndBody {
  Param([string]$Path)
  $lines = Get-Content -Encoding UTF8 $Path -ErrorAction Stop
  if (-not $lines) { return @{ Front = ""; Body = ""; HasFront = $false } }
  $i1 = ($lines | Select-String -Pattern '^---\s*$' | Select-Object -First 1).LineNumber
  $i2 = ($lines | Select-String -Pattern '^---\s*$' | Select-Object -Skip 1 -First 1).LineNumber
  if ($i1 -and $i2 -and $i2 -gt $i1) {
    $frontLines = $lines[($i1) .. ($i2-2)]
    $bodyLines = $lines[($i2) .. ($lines.Count-1)]
    $front = ($frontLines -join "`n").Trim()
    $body = ($bodyLines -join "`n").TrimStart()
    return @{ Front = $front; Body = $body; HasFront = $true }
  } else {
    $text = ($lines -join "`n")
    return @{ Front = ""; Body = $text; HasFront = $false }
  }
}

Function Parse-FrontMatter {
  Param([string]$Front)
  $dict = @{}
  $Front -split "\n" | ForEach-Object {
    if ($_ -match '^(\w+):\s*(.*)$') {
      $k = $matches[1]
      $v = $matches[2].Trim()
      if ($v.StartsWith('"') -and $v.EndsWith('"')) { $v = $v.Trim('"') }
      if ($v -eq 'null') { $v = $null }
      elseif ($v -match '^[0-9]+$') { $v = [int]$v }
      $dict[$k] = $v
    }
  }
  return $dict
}

Function Compute-Metrics {
  Param([string]$Body)
  $clean = ($Body -replace "<!--.*?-->", " ") -replace "\s+"," "
  $clean = $clean.Trim()
  if ([string]::IsNullOrWhiteSpace($clean)) { return @{ word_count = 0; reading_time_min = 0; est_tokens = 0 } }
  $words = ($clean -split ' ').Count
  $reading = [int][Math]::Ceiling($words / 250)
  $tokens = [int][Math]::Round($words * 1.3)
  return @{ word_count = $words; reading_time_min = $reading; est_tokens = $tokens }
}

Function Build-FrontMatter {
  Param([hashtable]$fm)
  $order = @(
    'chapter','scene','chapter_title','chapter_slug','title','slug','order','prev','next','word_count','reading_time_min','est_tokens','id'
  )
  $sb = New-Object System.Text.StringBuilder
  foreach ($k in $order) {
    if ($fm.ContainsKey($k)) {
      $v = $fm[$k]
      if ($null -eq $v) { $val = 'null' }
      elseif ($v -is [int]) { $val = $v }
      elseif ($v -is [string] -and $v -match '^[0-9]+$' -and $k -in @('chapter','scene','order')) { $val = [int]$v }
      elseif ($v -is [string] -and ($v.Contains(':') -or $v.Contains('#') -or $v -match '^\s|\s$')) { $val = '"' + $v + '"' }
      elseif ($v -is [string] -and $k -in @('title','chapter_title','id')) { $val = '"' + $v + '"' }
      else { $val = $v }
      [void]$sb.AppendLine("$($k): $($val)")
    }
  }
  return $sb.ToString().TrimEnd()
}

$chapterMap = Get-ChapterMap
("Chapter map keys: {0}" -f ($chapterMap.Keys -join ',')) | Add-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'normalize-scenes.log')
$scenes = Get-SceneOrder
("Found {0} scenes" -f $scenes.Count) | Add-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'normalize-scenes.log')

# Build global prev/next map by slug order
$slugs = $scenes | ForEach-Object { $_.Slug }

for ($i=0; $i -lt $scenes.Count; $i++) {
  $scene = $scenes[$i]
  ("Updating {0}" -f $scene.FileName) | Add-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'normalize-scenes.log')
  $prev = if ($i -gt 0) { $slugs[$i-1] } else { $null }
  $next = if ($i -lt ($scenes.Count-1)) { $slugs[$i+1] } else { $null }

  $parts = Get-FrontMatterAndBody -Path $scene.Path
  $fm = Parse-FrontMatter -Front $parts.Front

  # Derive defaults
  $chapterStr = $scene.Chapter.ToString()
  $chapterInfo = $chapterMap[$chapterStr]
  $fm['chapter'] = $scene.Chapter
  $fm['scene'] = $scene.Scene
  if ($chapterInfo) {
    $fm['chapter_title'] = $chapterInfo.title
    $fm['chapter_slug'] = $chapterInfo.slug
  }
  if (-not $fm.ContainsKey('title') -or [string]::IsNullOrWhiteSpace($fm['title'])) { $fm['title'] = "Scene $($scene.Scene)" }
  $fm['slug'] = $scene.Slug
  $fm['order'] = $scene.Scene
  $fm['prev'] = $prev
  $fm['next'] = $next
  if (-not $fm.ContainsKey('id') -or [string]::IsNullOrWhiteSpace($fm['id'])) { $fm['id'] = ([guid]::NewGuid()).ToString() }

  $metrics = Compute-Metrics -Body $parts.Body
  $fm['word_count'] = $metrics.word_count
  $fm['reading_time_min'] = $metrics.reading_time_min
  $fm['est_tokens'] = $metrics.est_tokens

  $newFront = Build-FrontMatter -fm $fm
  $out = "---`n$($newFront)`n---`n`n$($parts.Body.TrimStart())"
  # Ensure trailing newline
  if (-not $out.EndsWith("`n")) { $out += "`n" }
  Set-Content -Encoding UTF8 -NoNewline -Path $scene.Path -Value $out
  ("Wrote {0}" -f $scene.FileName) | Add-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'normalize-scenes.log')
}

("Normalized {0} scene files." -f $scenes.Count) | Add-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'normalize-scenes.log')
