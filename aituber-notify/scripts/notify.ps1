#Requires -Version 7
<#
.SYNOPSIS
  Claude Code Stop hook — AITuber に作業完了を通知する。

  Claude Code がセッションを終了するときに Stop hook 経由で呼ばれる。
  stdin の JSON payload から transcript_path を取り出し、以下を抽出して
  POST /api/notify/completion を叩く:
    summary      : transcript の ai-title（Claude がセッションに付けたタイトル）
    duration_sec : transcript 最初の timestamp と現在時刻の差（秒）
    project      : transcript_path のプロジェクト名部分（basename）

  AITuber 未起動時 / 接続エラー時は silent fail（exit 0）で Claude Code を妨げない。
#>

param()

$AITUBER_URL = 'http://localhost:8080/api/notify/completion'
$TIMEOUT_SEC = 5

# ------------------------------------------------------------------
# 1. stdin から Stop hook payload を読む
# ------------------------------------------------------------------
$payload = $null
try {
    $raw = [Console]::In.ReadToEnd()
    if ($raw.Trim()) {
        $payload = $raw | ConvertFrom-Json -ErrorAction Stop
    }
} catch {
    # payload が読めなくても silent fail
}

$transcriptPath = $payload?.transcript_path

# ------------------------------------------------------------------
# 2. transcript JSONL を解析して summary / duration_sec を取得
# ------------------------------------------------------------------
$summary     = $null
$durationSec = $null
$project     = $null

if ($transcriptPath -and (Test-Path $transcriptPath)) {
    try {
        $lines = Get-Content $transcriptPath -Encoding UTF8 -ErrorAction Stop

        $firstTimestamp = $null

        foreach ($line in $lines) {
            if (-not $line.Trim()) { continue }
            $entry = $line | ConvertFrom-Json -ErrorAction SilentlyContinue
            if (-not $entry) { continue }

            # ai-title → summary
            if ($entry.type -eq 'ai-title' -and $entry.aiTitle -and -not $summary) {
                $summary = $entry.aiTitle
            }

            # file-history-snapshot の最初の timestamp → 開始時刻
            if ($entry.type -eq 'file-history-snapshot' -and $entry.snapshot?.timestamp -and -not $firstTimestamp) {
                $firstTimestamp = [datetime]::Parse($entry.snapshot.timestamp, $null, [System.Globalization.DateTimeStyles]::RoundtripKind)
            }

            # 両方取れたら break
            if ($summary -and $firstTimestamp) { break }
        }

        if ($firstTimestamp) {
            $durationSec = [int]([datetime]::UtcNow - $firstTimestamp).TotalSeconds
            if ($durationSec -lt 0) { $durationSec = $null }
        }
    } catch {
        # transcript 読み取り失敗は無視
    }

    # transcript_path からプロジェクト名を取得
    # 例: C:\Users\shuhe\.claude\projects\C--Users-shuhe-repo-aituber\<uuid>.jsonl
    # → フォルダ名 C--Users-shuhe-repo-aituber → 末尾の basename → aituber
    try {
        $projectFolder = Split-Path (Split-Path $transcriptPath -Parent) -Leaf
        # C--Users-shuhe-repo-aituber → -- 区切りで最後のセグメント
        $parts = $projectFolder -split '--'
        $project = $parts[-1]
    } catch {
        # 失敗時は null のまま
    }
}

# summary が取れなかった場合のフォールバック
if (-not $summary) {
    $summary = 'Claude Code 作業セッション'
}

# ------------------------------------------------------------------
# 3. POST /api/notify/completion
# ------------------------------------------------------------------
$body = @{
    summary  = $summary
    sync     = $false
}
if ($durationSec) { $body['duration_sec'] = $durationSec }
if ($project)     { $body['project']      = $project }

$json = $body | ConvertTo-Json -Compress

try {
    $response = Invoke-RestMethod `
        -Uri $AITUBER_URL `
        -Method POST `
        -ContentType 'application/json; charset=utf-8' `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) `
        -TimeoutSec $TIMEOUT_SEC `
        -ErrorAction Stop

    # 成功ログ（stderr に出す — Claude Code の出力には混ざらない）
    Write-Error "aituber-notify: OK — mode=$($response.mode) summary=$summary duration=${durationSec}s project=$project" -ErrorAction Continue

} catch {
    # 接続失敗 / タイムアウト は silent fail
    Write-Error "aituber-notify: skipped (AITuber not available)" -ErrorAction Continue
}

exit 0
