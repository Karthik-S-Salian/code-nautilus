from gi.repository import Nautilus, GObject
import subprocess
import os

def check_ok(command):
    try:
        subprocess.run([command, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (FileNotFoundError, PermissionError):
        return False
    
    
def get_vscode_details():

    vscode_path = os.getenv("VSCODEPATH")
    
    for path in [vscode_path,"code","/usr/bin/code","/var/lib/flatpak/exports/bin/com.visualstudio.code"]:
        return ("code",path)
    
    for path in ["codium","/usr/bin/codium","/var/lib/flatpak/exports/bin/com.vscodium.codium"]:
        return ("codium",path)
    
    raise Exception("could not find valid vscode path set VSCODEPATH env to specify custom path")


VSCODENAME,VSCODE = get_vscode_details()

# always create new window?
NEWWINDOW = False
    
    

class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):

    def launch_vscode(self, menu, files):
        safepaths = ''
        args = ''

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

            # If one of the files we are trying to open is a folder
            # create a new instance of vscode
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = '--new-window '

        if NEWWINDOW:
            args = '--new-window '

        subprocess.call(VSCODE + ' ' + args + safepaths + '&', shell=True)

    def get_file_items(self, *args):
        files = args[-1]
        item = Nautilus.MenuItem(
            name='VSCodeOpen',
            label='Open in ' + VSCODENAME,
            tip='Opens the selected files with VSCode'
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

