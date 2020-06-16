import os
from tkinter import Tk, filedialog
from winreg import *

tk = Tk

mpath = '/media_soviet/workshop_wip'
regpath = r'SOFTWARE\WR Mod Installer'

def main():
    basepath = ''
    steamid = ''

    regkey = CreateKey(HKEY_CURRENT_USER, regpath)

    try:
        basepath = str(QueryValueEx(regkey, 'Path')[0])
        steamid = str(QueryValueEx(regkey, 'Id')[0])
    except:
        pass
    if basepath == '':
        basepath = filedialog.askdirectory(title="Select W&R directory")
        SetValueEx(regkey, 'Path', 0, REG_SZ, basepath)
    if steamid == '':
        steamid = input('Enter your steam id: ')
        SetValueEx(regkey, 'Id', 0, REG_SZ, steamid)
    modpath = basepath + mpath
    count = 0
    for mod in os.scandir(modpath):
        if not mod.is_dir():
            continue
        name = mod.name
        if not name.isdecimal() or len(name) > 10:
            inipath = f'{modpath}/{name}/workshopconfig.ini'
            replaceid(inipath, steamid)
            newname = name[0:10]
            os.rename(mod.path, f'{modpath}/{newname}')
            count += 1
    print(str(count) + ' mods installed')

def replaceid(filepath: str, id: str):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('$OWNER_ID'):
            lines[i] = f'$OWNER_ID {id}\n'
            break
    with open(filepath, 'w') as f:
        f.writelines(lines)


if __name__=='__main__':
    main()
    os.system("pause")
