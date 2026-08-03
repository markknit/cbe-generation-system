@echo off
setlocal EnableDelayedExpansion
REM ===========================================================================
REM  sync_to_drive.bat - Windows -> Google Drive sync for CBE lesson-plan output
REM ===========================================================================
REM  Run on the Windows box AFTER `git pull`. Nothing is generated here - node
REM  and python are not needed. This only mirrors already-committed output.
REM
REM  Usage:
REM      scripts\sync_to_drive.bat            actually sync
REM      scripts\sync_to_drive.bat preview    dry run, writes nothing (/L)
REM
REM  Two independent jobs, because the two trees serve different audiences and
REM  need DIFFERENT delete behaviour:
REM
REM    1. docx + json  ->  G:\My Drive\CBE Outputs        /E    (no purge)
REM       The editable master, per docs/PDF_GENERATION.md - Mark, the partner's
REM       contract checker, and anyone doing manual content edits. NOT mirrored:
REM       /PURGE here would delete anything a human added to that folder.
REM       Cost of this choice: renamed/removed sub-strands leave stale files
REM       behind. That is deliberate - visible clutter beats silent data loss.
REM
REM    2. pdf + html   ->  G:\My Drive\CBE Outputs\PDF    /MIR  (purge on)
REM       Pure generated, read-only distribution for teachers. Nobody hand-edits
REM       a PDF, and sub-strand renames DO happen (the Phase 3 filePrefix change
REM       orphaned files), so stale PDFs should be removed. Mirroring is correct.
REM       *** This job is a TRUE MIRROR: anything you put in the Drive PDF
REM       folder by hand WILL be deleted on the next run. Keep it output-only.
REM
REM  Path handling that matters:
REM    - job 1 excludes the PDF subdirectory (/XD), or it walks into the PDF
REM      tree and syncs it a second time into the wrong destination.
REM    - job 2 uses NO file mask - see the comment above that robocopy call.
REM
REM  Close Word before running. Robocopy skips locked files and still reports
REM  success for everything else, so an open lesson plan silently stays stale.
REM ===========================================================================

REM --- Configuration --------------------------------------------------------
REM Repo root is this script's parent directory (scripts\..), resolved to a full
REM path so logs and echoed paths do not contain a literal "\..".
for %%I in ("%~dp0..") do set "REPO=%%~fI"
set "SRC_DOCX=%REPO%\data\outputs\v2"
set "SRC_PDF=%REPO%\data\outputs\v2\PDF"
set "DRIVE_ROOT=G:\My Drive"
set "DEST_DOCX=%DRIVE_ROOT%\CBE Outputs"
set "DEST_PDF=%DRIVE_ROOT%\CBE Outputs\PDF"

REM /FFT  - 2-second timestamp granularity. Google Drive is a virtual filesystem
REM         and without this robocopy re-copies unchanged files every run.
REM /R:2 /W:5 - 2 retries, 5s apart, instead of robocopy's default 1,000,000.
REM /NP   - no per-file progress percentages (keeps the log readable).
set "COMMON=/FFT /R:2 /W:5 /NP /TEE"

REM --- Preview mode ---------------------------------------------------------
set "DRYRUN="
if /i "%~1"=="preview" (
    set "DRYRUN=/L"
    echo.
    echo *** PREVIEW MODE - nothing will be written or deleted. ***
    echo *** Lines marked EXTRA under job 2 are what /MIR would DELETE.  ***
)

REM --- Log file -------------------------------------------------------------
REM PowerShell rather than wmic - wmic is deprecated and absent on newer Win11.
set "STAMP="
for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss" 2^>nul') do set "STAMP=%%I"
if not defined STAMP set "STAMP=nodate"
set "LOGDIR=%REPO%\logs"
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
set "LOG=%LOGDIR%\sync_to_drive_%STAMP%.log"

REM --- Pre-flight checks ----------------------------------------------------
if not exist "%SRC_DOCX%\" (
    echo ERROR: source tree not found: "%SRC_DOCX%"
    echo        Run this from the repo, and check you have pulled.
    exit /b 1
)
if not exist "%SRC_PDF%\" (
    echo ERROR: PDF tree not found: "%SRC_PDF%"
    echo        Run generate_pdfs.js on jhm-spark and git pull, or the PDF
    echo        job below would purge the whole Drive PDF folder.
    exit /b 1
)
if not exist "%DRIVE_ROOT%\" (
    echo ERROR: "%DRIVE_ROOT%" not found - is Google Drive running and mounted there?
    echo        Aborting BEFORE the mirror job, which would otherwise delete
    echo        nothing locally but could create a stray local G: folder.
    exit /b 1
)

echo.
echo Repo:      %REPO%
echo Log:       %LOG%
echo.

REM --- Job 1: docx + json (no purge) ----------------------------------------
echo ============================================================
echo  JOB 1/2  docx + json  ^-^>  %DEST_DOCX%   (/E, no delete)
echo ============================================================
robocopy "%SRC_DOCX%" "%DEST_DOCX%" *.docx *.json /E /XD "%SRC_PDF%" %COMMON% %DRYRUN% /LOG+:"%LOG%"
set "RC1=%ERRORLEVEL%"

REM --- Job 2: pdf + html (mirror) -------------------------------------------
echo.
echo ============================================================
echo  JOB 2/2  pdf + html   ^-^>  %DEST_PDF%   (/MIR, deletes stale)
echo ============================================================
REM No file mask here, deliberately. Two reasons:
REM  1. /MIR + a file mask is a robocopy trap: source files excluded by the mask
REM     count as "not present", so /PURGE can delete destination files that do
REM     not match it. Mirroring the whole tree removes that failure mode.
REM  2. It structurally guarantees index.html syncs. The old job used a *.pdf
REM     mask and had to remember *.html separately or the teacher browse page
REM     silently never synced (see docs/PDF_GENERATION.md).
REM The source tree is pure generated output - verified 255 *.pdf + 1 *.html and
REM nothing else - so there is no stray file here to sweep up.
robocopy "%SRC_PDF%" "%DEST_PDF%" /MIR %COMMON% %DRYRUN% /LOG+:"%LOG%"
set "RC2=%ERRORLEVEL%"

REM --- Result ---------------------------------------------------------------
REM Robocopy exit codes are a bitmask: 0-7 are success (1=copied, 2=extra,
REM 4=mismatched, 8=failed, 16=fatal). Anything >=8 is a real failure.
echo.
echo ============================================================
echo  docx/json job exit code: %RC1%
echo  pdf/html  job exit code: %RC2%
if %RC1% GEQ 8 goto :failed
if %RC2% GEQ 8 goto :failed
echo  RESULT: OK  (codes under 8 mean success)
echo  Log: %LOG%
echo ============================================================
if defined DRYRUN echo Preview only - nothing was changed. Re-run without "preview" to sync.
exit /b 0

:failed
echo  RESULT: FAILED - at least one job returned 8 or higher.
echo  Check the log: %LOG%
echo  Common cause: a .docx open in Word, or Google Drive not finished syncing.
echo ============================================================
exit /b 1
