@echo off
pushd "%~dp0.."
python -m cache_sync
popd
pause
