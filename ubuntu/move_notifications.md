THIS WORKED:

https://extensions.gnome.org/extension/708/panel-osd/ ... you need to install from the site, then hit reload, then see the settings appear on the page and click that.


BUT NOT THIS:

https://askubuntu.com/questions/1389775/how-to-put-notifications-back-to-top-righ-on-ubuntu-21-10/1389780#1389780

    gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell --method org.gnome.Shell.Eval string:'Main.panel._centerBox.remove_child(Main.panel.statusArea.dateMenu.container); Main.panel._rightBox.insert_child_at_index(Main.panel.statusArea.dateMenu.container, 0);'


