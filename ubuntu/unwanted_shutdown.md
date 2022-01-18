# 2022-01-18

When on lock screen, appears to still shut down. Persisted through updates to 21.10.

This seems fine.

    $ gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type
    'nothing'

Trying this:
* go to dconf editor (easier to browse) and toggle settings to trigger a rewrite. Note there is both a 'blank' and a 'nothing'.
* set sleep-inactive-ac-timeout to 0 (was 3600)


