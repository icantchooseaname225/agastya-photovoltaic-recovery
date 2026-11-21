# Start and stop AGASTYA-EYE on demand

AGASTYA-EYE does not start automatically when Windows boots. This is intentional: the Python process and vision models use laptop memory only while EYE is running.

## Start EYE

1. On the Windows desktop, double-click **Start AGASTYA-EYE**.
2. Wait for the local site to open. The launcher checks its Python environment, starts the server in the background, waits for the API, and opens the browser. The address is normally `http://127.0.0.1:8765`; if that port is busy, use the address printed by the launcher.
3. If the site says it cannot connect, use the desktop shortcut again. The site is served by the EYE process, so it cannot start that process after it has stopped.

If the desktop shortcut is missing, open `C:\Agastya\Agastya-EYE` in File Explorer and double-click `Start-EYE.bat`.

## Stop EYE and free its memory

Double-click **Stop AGASTYA-EYE** on the desktop. This calls the existing graceful shutdown script and verifies that the launcher-managed process stopped. Closing the browser tab alone does not stop EYE.

If the shortcut is missing, double-click `Stop-EYE.bat` in `C:\Agastya\Agastya-EYE`. If EYE was started directly with `app.py` instead of the launcher, use Ctrl+C in that PowerShell window.

## If startup fails

The launcher pauses and reports the error. Check the `.out.log` and `.err.log` files it names under `%TEMP%`. For missing Python dependencies, follow the interpreter guidance in [the main README](../README.md); the launcher uses an existing compatible environment and does not create another environment automatically.

## Memory behavior

The desktop shortcuts do not keep a service running. Start EYE only when you need the local inspection site and stop it when you are done. No Windows startup task or always-on background monitor is installed by this setup.
