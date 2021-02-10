import os
import shutil
from tkinter import Tk, filedialog
from winreg import *

tk = Tk

mpath = '/media_soviet/workshop_wip/'
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
    action = input('Workers&Resources: Soviet Republic Mod Installer\nPress 1 to install mods\nPress 2 to change id or path\nPress 3 to view installed mods\n')
    if action == '1': 
        count = 0
        alr_installed = 0

        for mod in os.scandir(modpath):
            if not mod.is_dir():
                continue
            name = mod.name
            if not name.isdecimal() or len(name) > 10:
                newname = name[0:10]
                if os.path.exists(modpath + newname):
                    shutil.rmtree(modpath + name)
                    alr_installed += 1
                else:
                    inipath = f'{modpath}{name}/workshopconfig.ini'
                    replaceid(inipath, steamid)
                    os.rename(mod.path, modpath + newname)
                    count += 1
        print(f'{count} mods installed. {alr_installed} mods were already installed')

    elif action == '2':
        x = input(f'Your current id is {steamid}. Do you want to change it?(Y/N):')
        if x.lower() == 'y':
            steamid = input('Enter your steam id: ')
            SetValueEx(regkey, 'Id', 0, REG_SZ, steamid)
        x = input(f'Your current path is {basepath}. Do you want to change it?(Y/N):')
        if x.lower() == 'y':
            basepath = filedialog.askdirectory(title="Select W&R directory")
            SetValueEx(regkey, 'Path', 0, REG_SZ, basepath)
    elif action == '3':
        count = 0
        for mod in os.scandir(modpath):
            if not mod.is_dir():
                continue
            name = mod.name
            if name.isdecimal() and len(name) <= 10:
                print('----------')
                count += 1
                inipath = f'{modpath}{name}/workshopconfig.ini'
                with open(inipath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                for line in lines:
                    if line.startswith('$ITEM_ID') or line.startswith('$ITEM_NAME') or line.startswith('$ITEM_DESC'):
                        print(line[:-1])
        print(f'{count} mods are installed')

    else:
        print('Invalid input')
def replaceid(filepath: str, id: str):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('$OWNER_ID'):
            lines[i] = f'$OWNER_ID {id}\n'
            break
    with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
        f.writelines(lines)


if __name__=='__main__':
    main()
    os.system("pause")
