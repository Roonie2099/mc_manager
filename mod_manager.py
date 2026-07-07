import os
from pathlib import Path
import shutil
import json
import sys


if getattr(sys, "frozen", False):
    main_path = Path(sys.executable)
else:
    main_path = Path(__file__)

mods_path = main_path.parent.parent / "mods"
mods_storage_path = main_path.parent / "mods_storage"
json_path = main_path.parent / "mod_instance_data.json"


if not json_path.exists():
    with open(json_path,"w",encoding="utf-8") as f:
        json.dump({"Always_mods":[]},f,indent=4)


with open(json_path,"r",encoding="utf-8") as f:
    temp_data = f.read().strip()
    if temp_data == "" or temp_data == "{}":
        with open(json_path,"w",encoding="utf-8") as file:
            json.dump({"Always_mods":[]},file,indent=4)
temp_data = None


#Các task
def read_json():
    with open(json_path,"r",encoding="utf-8") as file:
        return json.load(file)


def write_json(data):
    with open(json_path,"w",encoding="utf-8") as file:
        json.dump(data,file,indent=4)


def finish_task():
    print()
    print("Task succeed")
    refresh()
    choose = str(input("Do you want to return to menu?(y/n): "))
    if choose == "y":
        return
    else:
        sys.exit()

def select_mod(list_select):
    if not list_select:
        print("No mod available")
        print( )
        choose = str(input("Return to menu(y/n): "))
        if choose == "y":
            return None
        else:
            exit()    
            return None
    
    for i in range(len(list_select)):
        print(str(i+1) +".",list_select[i].name)
    
    print()
    choose = input("Select mod(select many mod by using \",\" with no space between): ").split(",")
    list_c = [str(x+1) for x in range(len(list_select))]
    while False in [n in list_c for n in choose]:
        choose = input("Wrong input, please select mod again: ").split(",")
    choose = [int(i) for i in choose] 
    return sorted(set(choose))


def refresh():
    global mod_in_use
    global mod_in_storage
    global mod_not_in_use
    global instance_using
    instance_using = "Costume"

    mod_in_use = [
        mod
        for mod in mods_path.iterdir()
        if mod.suffix == ".jar"
    ]

    mod_in_storage = [
        mod
        for mod in mods_storage_path.iterdir()
        if mod.suffix == ".jar"
    ]

    mod_not_in_use = [
        mod
        for mod in mod_in_storage
        if mod.name not in [n.name for n in mod_in_use]
    ]

    data = read_json()

    for ins in data:
        data[ins] = [
            mod
            for mod in data[ins]
            if (mods_storage_path / mod).exists()
        ]

    write_json(data)
    data = read_json()
    
    if not mod_in_use:
        instance_using = "No mod or ins detected"
    else:
        for ins in data:
            mod_list = sorted(data[ins])
            if sorted([mod.name for mod in mod_in_use]) == mod_list:
                instance_using = ins
                break
    

#Các màn hình chính
def menu():
    refresh()
    os.system("cls")
    print("Minecraft Mod Manager (v1.2)  -by Roonie-")
    print()
    print("Mod using:",len(mod_in_use))
    print("Instace using:",instance_using)
    print()
    print("1. Add mod to use")
    print("2. Delet mod from using")
    print("3. Add new instance")
    print("4. Change instance to use")
    print("5. Delet all mod from using")
    print("6. Mod contol menu")
    print("7. Instance control menu")

    choose = input("Select your choice: ")
    while choose not in [str(i+1) for i in range(7)]:
        choose = input("Select your choice again: ")
    choose = int(choose)
    menu_actions = {
        1: Add_new_mod,
        2: Delet_mod_from_use,
        3: Add_new_instance,
        4: Change_instance,
        5: Delete_all_mod_from_use,
        6: menu_mod_control,
        7: menu_ins_control,
    }
    menu_actions[choose]()


def menu_mod_control():
    refresh()
    os.system("cls")
    print("     MOD CONTROL MENU")
    print()
    print("1. Mod using list")
    print("2. All Mod in storage list")
    print("3. Always_mods control")

    choose = input("Select your choice: ")
    while choose not in [str(i+1) for i in range(3)]:
        choose = input("Select your choice again: ")
    choose = int(choose)
    print()
    if choose in [1,2]:
        if choose == 1:
            data = [mod.name for mod in mod_in_use]
        else:
            data = [mod.name for mod in mod_in_storage]
        
        if not data:
            print("No mod detected")
        else:
            print("Mod list:")
            for i in range(len(data)):
                print(str(i+1)+".",data[i])

        finish_task()

    else:
        Always_mods_control()
    return
        

def menu_ins_control():
    refresh()
    os.system("cls")
    print("     INSTANCE CONTROL MENU")
    print()
    print("1. All instance/mod list")
    print("2. Add/delet mod in instance")
    print("3. Delet instance")

    choose = input("Select your choice: ")
    while choose not in [str(i+1) for i in range(3)]:
        choose = input("Select your choice again: ")
    choose = int(choose)
    print()
    
    if choose == 1:
        data = read_json()

        temp_data = [ins for ins in data if data != "Always_mods"]
        if not temp_data:
            print("No instance detected")
        else:
            data_list = list(data.keys())
            print("Instance list:")
            for i in range(len(data)):
                print(str(i+1)+".",data_list[i]+":")
                for mod in data[data_list[i]]:
                    print(" -",mod)
                print()

        finish_task()
    
    elif choose == 2:
        Add_delete_mod_instance()
    else:
        Delet_instance()
    return
        

def Add_new_mod():
    refresh()
    os.system("cls")
    print("     ADD NEW MOD TO USE")
    print()
    choose = select_mod(mod_not_in_use)
    if choose is None:return
    
    for mod_num in choose:  
        selected_mod = mod_not_in_use[mod_num-1]
        shutil.copy2(
            selected_mod,
            mods_path)
    finish_task()
    return


def Delet_mod_from_use():
    refresh()
    os.system("cls")
    print("     DELET MOD FROM USING")
    print()
    choose = select_mod(mod_in_use)
    if choose is None:return

    for mod_num in choose:  
        selected_mod = mod_in_use[mod_num-1]
        shutil.copy2(
            selected_mod,
            mods_storage_path)
        selected_mod.unlink()
    finish_task()
    return


def Add_new_instance():
    refresh()
    os.system("cls")
    data = read_json()
    
    print("     ADD NEW INSTANCE")
    print()
    new_ins_name = str(input("New instance name: "))
    
    while new_ins_name in data:
        if new_ins_name == "Always_mods":
            new_ins_name = str(input("You cant use this name, please try something else: "))
        else:
            new_ins_name = str(input("This name has been used, please try something else: "))
   
    print()
    print("Mod list:")
    choose = select_mod(mod_in_storage)
    if choose is None: return
    mod_list_choose = [mod_in_storage[i-1].name for i in choose]
    data[new_ins_name] = mod_list_choose
    write_json(data)
   
    finish_task()
    return


def Change_instance():
    refresh()
    os.system("cls")
    print("     CHANGE INSTANCE TO USE")
    print()
    data = read_json()
    temp_data = [ins for ins in data if ins != "Always_mods"]
    if not temp_data:
        print("No instance in the list")
        finish_task()
        return
    
    print("Instance list")
    for i in range(len(temp_data)):
        print(str(i+1)+".",temp_data[i])
    print()
    
    choose = str(input("Choose instance to change: "))
    while choose not in [str(n+1) for n in range(i+1)]:
        choose = input("Wrong input, please choose instance to change again: ")
    choose = int(choose)

    for mod in mod_in_use:
        shutil.copy2(
            mod,
            mods_storage_path)
        mod.unlink()

    for mod in data[temp_data[choose-1]]:
        selected_mod = mods_storage_path / mod
        shutil.copy2(
            selected_mod,
            mods_path)
    
    choose_2 = input("Do you want to keep always-mods from using?(y/n): ")    
    while choose_2 not in ["y","n"]:
        choose_2 = input("Wrong input, please try again(y/n): ")
    if choose_2 == "y":
        for mod in data["Always_mods"]:
            selected_mod = mods_storage_path / mod
            shutil.copy2(
                selected_mod,
                mods_path)
    finish_task()
    return

    
def Delete_all_mod_from_use():
    refresh()
    os.system("cls")
    print("     DELETE ALL MOD FROM USING")
    print()
    data = read_json()
    
    choose = input("Are you sure to delete all mod from using?(y/n): ")
    while choose not in ["y","n"]:
        choose = input("Wrong input, please try again(y/n): ")
    if choose == "y":
        choose_2 = input("Do you want to keep always-mods from using?(y/n): ")
        
        while choose_2 not in ["y","n"]:
            choose_2 = input("Wrong input, please try again(y/n): ") 
        for mod in mod_in_use:  
            shutil.copy2(
                mod,
                mods_storage_path)
            mod.unlink()
       
        if choose_2 == "y":
            for mod in data["Always_mods"]:  
                selected_mod = mods_storage_path / mod
                shutil.copy2(
                    selected_mod,
                    mods_path)
    finish_task()
    return


def Always_mods_control():
    refresh()
    os.system("cls")
    print("     ALWAYS_MOD CONTROL")
    print()
    data = read_json()
    temp_data = [mod for mod in data["Always_mods"]]
    
    if not temp_data:
        print("No mod in the list")
        print()
        second_choose = input("Press 0 to add mod: ")
        while second_choose not in ["0"]:
            second_choose = input("Wrong input, please try again: ")
    else:
        print("Mod in always_mods list:")
        for i in range(len(temp_data)):
            print(str(i+1)+".", temp_data[i])
        print()
        second_choose = input("Press 0 to add mod, press 1 to delet mod: ")
        while second_choose not in ["0","1"]:
            second_choose = input("Wrong input, please try again: ")
    
    print()
    if second_choose == "0":
        mod_list = [mod for mod in mod_in_storage if mod.name not in data["Always_mods"]]
        print()
        data_choose = select_mod(mod_list)
        if data_choose is None:
            return
        for i in data_choose:
            mod = mod_list[i-1].name
            data["Always_mods"].append(mod)
    else:
        mod_list = [mods_storage_path / n for n in data["Always_mods"]]
        print()
        data_choose = select_mod(mod_list)
        if data_choose is None:
            return
        for i in sorted(data_choose, reverse=True):
            data["Always_mods"].pop(i-1)
    write_json(data)
    finish_task()
    return


def Add_delete_mod_instance():
    refresh()
    os.system("cls")
    print("     ADD/DELETE MOD IN INSTANCE")
    print()
    data = read_json()
    temp_data = list(data.keys())
    temp_data.remove("Always_mods")
    if not temp_data:
        print("No instance to change")
        finish_task()
        return

    print("Instance list:")
    for i in range(len(temp_data)):
        print(str(i+1)+".",temp_data[i])
    print()
    choose = str(input("Choose instance to change: "))
    while choose not in [str(n+1) for n in range(i+1)]:
        choose = input("Wrong input, please choose instance to change again: ")
    choose = int(choose)
   
    print()
    print("Instance chose:",temp_data[choose-1])
    second_choose = input("Press 0 to add mod, press 1 to delete mod: ")
    while second_choose not in ["0","1"]:
        second_choose = input("Wrong input, please try again: ")
    print()
    print("Mods list in instance: ")

    if second_choose == "0":
        mod_list = [n for n in mod_in_storage if n.name not in data[temp_data[choose-1]]]
        print()
        data_choose = select_mod(mod_list)
        if data_choose is None:
            return
        for i in data_choose:
            mod = mod_list[i-1].name
            data[temp_data[choose-1]].append(mod)
    else:
        mod_list = [mods_storage_path / n for n in data[temp_data[choose-1]]]
        print()
        data_choose = select_mod(mod_list)
        if data_choose is None:
            return
        for i in sorted(data_choose, reverse=True):
            data[temp_data[choose-1]].pop(i-1)
    write_json(data)
    finish_task()
    return


def Delet_instance():
    refresh()
    os.system("cls")
    print("     DELETE INSTANCE")
    print()
    data = read_json()
    temp_data = list(data.keys())
    temp_data.remove("Always_mods")
    if not temp_data:
        print("No instance detected")
        finish_task()
        return
    
    else:
        print("Instance list")
        for i in range(len(temp_data)):
            print(str(i+1)+".",temp_data[i])
        print()
        choose = input("Select your choice: ")
    while choose not in [str(i+1) for i in range(len(temp_data))]:
        choose = input("Select your choice again: ")
    choose = int(choose)
    choose_second = input("Are you sure?(y/n): ")
    if choose_second == "y":
        del data[temp_data[choose-1]]
        write_json(data)
    else:
        print("Task cancelled")
    finish_task()
    return


while True:
    refresh()
    menu()