# Ghostty

Install and upgrade via the Makefile (`make install`, `make update`). Apt package.

## X11 backend on bleepblop only

Tab switch is slow on bleepblop (Ubuntu 26.04, GNOME Wayland, RTX 2070, driver 580.178.04). Same binary is fast on the laptop bleepbleep (Intel UHD 620, Wayland). Do not apply this there.

Cause is Ghostty's per-tab `GtkGLArea` presenting through NVIDIA's EGL Wayland path. The desktop stays on Wayland. Ghostty alone starts with `GDK_BACKEND=x11` (XWayland).

On bleepblop:

- Dock and D-Bus: `~/.config/systemd/user/app-com.mitchellh.ghostty.service.d/x11.conf` sets `Environment=GDK_BACKEND=x11` on `app-com.mitchellh.ghostty.service`.
- Typed `ghostty`: `~/mybin/ghostty` exports the same variable and execs `/usr/bin/ghostty`.

`--gtk-single-instance=false` was only the test, so the new process would not join an already-running Wayland instance. The permanent launch keeps single-instance.

`window-vsync=false` does nothing on this build. The option is macOS-only. Do not switch the GNOME session to Xorg. Ubuntu 26.04 has no GNOME on Xorg session.

XWayland costs: clipboard between this window and Wayland apps is the worse path, and Ghostty's quick terminal does not work on X11.
