# VSCode Nautilus Extension
#
# Place me in ~/.local/share/nautilus-python/extensions/,
# ensure you have python-nautilus package, restart Nautilus, and enjoy :)
#
# This script is released to the public domain.
from gi.repository import Nautilus, GObject
import subprocess
import os

def check_ok(command:str):
    try:
        subprocess.run([command, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, PermissionError, subprocess.CalledProcessError):
        return False
    
    
def get_vscode_details()->tuple[str,str]:

    vscode_path = os.getenv("VSCODEPATH")
    
    for path in [vscode_path,"code","/usr/bin/code","/var/lib/flatpak/exports/bin/com.visualstudio.code"]:
        if path and check_ok(path):
            return ("code",path)
    
    for path in ["codium","/usr/bin/codium","/var/lib/flatpak/exports/bin/com.vscodium.codium"]:
        if path and check_ok(path):
            return ("codium",path)
    
    raise Exception("could not find valid vscode path set VSCODEPATH env to specify custom path")


VSCODENAME,VSCODE = get_vscode_details()

# always create new window?
NEWWINDOW = False
    
    

class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):

    def launch_vscode(self, menu, files):
        args = []
        paths = []

        for file in files:
            filepath = file.get_location().get_path()
            paths.append(filepath)

            if os.path.isdir(filepath) and os.path.exists(filepath):
                args.append("--new-window")

        if NEWWINDOW and "--new-window" not in args:
            args.append("--new-window")

        cmd = [VSCODE] + args + paths
        subprocess.Popen(cmd)

    def get_file_items(self, *args):
        files = args[-1]
        item = Nautilus.MenuItem(
            name='VSCodeOpen',
            label='Open in ' + VSCODENAME,
            tip='Opens the selected files with VSCode',
            icon="code-nautilus"
        )
        item.connect('activate', self.launch_vscode, files)

        return [item]

    def get_background_items(self, *args):
        file_ = args[-1]
        item = Nautilus.MenuItem(
            name='VSCodeOpenBackground',
            label='Open in ' + VSCODENAME,
            tip='Opens the current directory in VSCode'
        )
        item.connect('activate', self.launch_vscode, [file_])

        return [item]