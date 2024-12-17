import json
import re
import os
import shutil
import ast
import importlib.util
import threading
from colorama import Fore, Style, init

init(autoreset=True)
session_history = []
temp_hack = "" # fix at later date, bandaid code.py push fix

def traverse_json(data, NoMulti, start_key=None):
    def recursive_search(obj, search_key, path=""):
        results = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_path = f"{path}.{k}" if path else k
                if re.search(search_key, k):
                    results.append((new_path, v))
                results.extend(recursive_search(v, search_key, new_path))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                results.extend(recursive_search(item, search_key, new_path))
        return results

    current = data
    history = []
    combined = []

    if start_key:
        try:
            results = recursive_search(data, start_key)
            if not results:
                raise ValueError(f"{Fore.RED}Invalid start key: {start_key}")
            path, value = results[0]
            print(f"{Fore.GREEN}Starting at key: {path}")
            current = value
            history.append((data, path))
        except (KeyError, TypeError, ValueError) as e:
            print(f"{Fore.RED}Error: {e}")
            return

    backtrack_limit = len(history)

    while isinstance(current, (dict, list)):
        if isinstance(current, dict):
            print(f"\n{Fore.CYAN}Keys available:")
            keys = list(current.keys())
            for i, key in enumerate(keys):
                print(f"{i+1}: {' ' if i < 9 else ''}{Fore.GREEN}{key}")

            top_level_display = "'back' to go back, " if len(history) > backtrack_limit else ""
            prompt = "Enter a number to explore a key, " + top_level_display + "'search:<key>' to search, 'exit' to exit"
            if not NoMulti:
                prompt += ", or 'all' to collect all values"
                prompt += ", or comma-separated numbers to select multiple keys"
            prompt += ".\n: "

            user_input = input(prompt).strip()

            if user_input.lower() == 'exit':
                print("Exiting traversal.")
                return

            if user_input.lower() == 'back':
                if len(history) > backtrack_limit:
                    current, _ = history.pop()
                else:
                    print(f"{Fore.RED}Cannot backtrack beyond the start key.")
                continue

            if user_input.lower().startswith('search:'):
                search_key = user_input.split('search:', 1)[1]
                try:
                    results = recursive_search(data, search_key)
                    if results:
                        print(f"\n{Fore.CYAN}Search results:")
                        d = 0
                        for i, (path, value) in enumerate(results):
                            value_str = value if not isinstance(value, (dict, list)) else '[Nested structure]'
                            if NoMulti and value_str == '[Nested structure]':
                                pass
                            else:
                                d += 1
                                print(f"{d}. {Fore.GREEN}Path: {path}, Value: {value_str}")
                        selection = input("Enter a number to navigate to the result or 'back' to return: ").strip()
                        a = d-i
                        if selection.isdigit():
                            idx = int(selection)-a
                            if 0 <= idx < len(results):
                                path, value = results[idx]
                                print(f"Navigating to path: {path}")
                                history.append((current, path))
                                current = [value]
                            else:
                                print("Invalid selection.")
                        continue
                    else:
                        print(f"No results found for key matching '{search_key}'.")
                except re.error as e:
                    print(f"Invalid regex: {e}")
                continue

            if not NoMulti and user_input.lower() == 'all':
                combined.extend(collect_all_values(current))
                break

            if not NoMulti and ',' in user_input:
                try:
                    indices = [int(x) for x in user_input.split(',')]
                    selected_keys = [keys[i] for i in indices if 0 <= i < len(keys)]
                    valid_keys = []

                    for key in selected_keys:
                        valid_keys.append(key)

                    if not valid_keys:
                        print(f"{Fore.RED}No valid keys selected. All selected keys contain nested structures.")
                        continue

                    for key in valid_keys:
                        if isinstance(current[key], list):
                            combined.extend(current[key])
                        else:
                            combined.append(current[key])
                    break
                except (ValueError, IndexError):
                    print("Invalid input. Please enter valid numbers.")
            else:
                try:
                    index = int(user_input) - 1
                    if 0 <= index < len(keys):
                        key = keys[index]
                        if isinstance(current[key], list):
                            combined.extend(current[key])
                            return combined
                        else:
                            history.append((current, key))
                            current = current[key]
                    else:
                        print(f"{Fore.RED}Invalid index. Please try again.")
                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter a valid number.")

        elif isinstance(current, list):
            break

    result = combined if combined else current; return result

def collect_all_values(obj):
    values = []
    if isinstance(obj, dict):
        for v in obj.values():
            values.extend(collect_all_values(v))
    elif isinstance(obj, list):
        for item in obj:
            values.extend(collect_all_values(item))
    else:
        values.append(obj)
    return values

def replacer(result, result2):
    game_pre = temp_hack
    folder_path = os.path.join(os.getenv('TEMP'), 'roblox', 'http')
    session_history.extend([result, result2])

    def find_cached_file_path():
        if game_pre:
            return f"{game_pre}cached_files"
        
        search_dirs = ["assets/games", "assets/community"]
        for base_dir in search_dirs:
            if not os.path.exists(base_dir):
                continue
            for sub_folder in os.listdir(base_dir):
                cached_files_path = os.path.join(base_dir, sub_folder, "cached_files")
                target_file_path = os.path.join(cached_files_path, result2)
                if os.path.exists(target_file_path):
                    return cached_files_path
        return None

    local_cached_files_path = find_cached_file_path()
    if not local_cached_files_path:
        print(f'{Fore.RED}No valid cached_files directory found for {result2}.{Style.RESET_ALL}')
        return

    try:
        copy_file_path = os.path.join(local_cached_files_path, result2)
        if os.path.exists(copy_file_path):
            for file_to_delete in result:
                delete_file_path = os.path.join(folder_path, file_to_delete)
                if os.path.exists(delete_file_path):
                    os.remove(delete_file_path)

                new_file_path = os.path.join(folder_path, file_to_delete)
                shutil.copy(copy_file_path, new_file_path)
                print(f'{Fore.BLUE}{file_to_delete} has been replaced with {result2}.{Style.RESET_ALL}')
        else:
            print(f'{Fore.RED}{result2} not found in {local_cached_files_path}.{Style.RESET_ALL}')

    except Exception as e:
        if hasattr(e, 'winerror') and e.winerror == 183:
            pass
        else:
            print(f'{Fore.RED}An error occurred: {e}{Style.RESET_ALL}\n')

def backbone(json_data, start_key, start_key2, addon, addon2, skip):
    if not skip:
        result = collect_all_values(addon if addon else traverse_json(json_data, NoMulti=False, start_key=start_key))
        result = [result] if not isinstance(result, list) else result
        if result and all(r is not None for r in result):
            result2 = addon2 if addon2 else traverse_json(json_data, NoMulti=True, start_key=start_key2)
            if isinstance(result2, list) and len(result2) == 1:
                result2 = result2[0]
            
            if result2:
                replacer(result, result2)

            return json_data, start_key, start_key2, result, result2, skip

def game_runner(game_pre):
    global temp_hack
    json_file_path = f"{game_pre}assets.json"
    game_code = f"{game_pre}code.py"

    start_key, start_key2, addon, addon2 = "", "", "", ""
    skip = False

    try:
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)

    try:
        spec = importlib.util.spec_from_file_location("game_code_module", game_code)
        game_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(game_module)

        if hasattr(game_module, "run"):
            temp_hack = game_pre
            json_data, start_key, start_key2, addon, addon2, skip = game_module.run(json_data, start_key, start_key2, addon, addon2, skip)
            backbone(json_data, start_key, start_key2, addon, addon2, skip)
        else:
            print(f"Error: The file {game_code} does not contain a `run` function.")
    except FileNotFoundError:
        print(f"Error: The file {game_code} was not found.")
        exit(1)
    except Exception as e:
        if str(e) == "cannot unpack non-iterable bool object":
            pass
        else:
            print(f"Error executing run(): {e}")

def load_settings():
    global startup_launch, startup_preset

    with open("storage/settings.json", 'r') as f:
        data = json.load(f)
    startup_launch = data.get('startup_launch', None)
    startup_preset = data.get('startup_preset', None)
    return data

def background_autolaunch():
    import psutil
    import time

    def get_roblox_pids():
        roblox_pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            if 'Roblox' in proc.info['name']:
                roblox_pids.append(proc.info['pid'])
        return roblox_pids

    def track_roblox_pids():
        known_pids = set(get_roblox_pids())
        preset_dir = "assets/presets"
        skip = False

        while True:
            if startup_launch:
                time.sleep(0.25)
                current_pids = set(get_roblox_pids())
                new_pids = current_pids - known_pids

                if new_pids:
                    for pid in new_pids:
                        if skip: skip = False; continue
                        selected_folder = f"{startup_preset}.txt"
                        preset_path = os.path.join(preset_dir, selected_folder)

                        try:
                            with open(preset_path, 'r') as file:
                                preset_choice = ast.literal_eval(file.read())
                                
                                if preset_choice:
                                    print(f"\n\nApplied {startup_preset}:")
                                    for i in range(0, len(preset_choice), 2):
                                        replacer(preset_choice[i], preset_choice[i+1])
                                    print("\nContinue selecting changes\n: ", end="")
                                else:
                                    print(f"{Fore.RED}Error running startup launch{Style.RESET_ALL}\n")
                        except Exception as e:
                            print(f"\n\n{Fore.RED}Error loading preset as preset does not exist: {e}{Style.RESET_ALL}\nContinue selecting previous changes\n: ", end="")
                        
                        skip = True

                known_pids = current_pids
            else:
                time.sleep(0.25)
                pass

    thread = threading.Thread(target=track_roblox_pids)
    thread.daemon = True
    thread.start()

def find_preset(selected_folder):
    if not folders:
        print(f"{Fore.RED}\nNo presets available in the directory.{Style.RESET_ALL}")
        return 
    else:
        print("\nAvailable presets:")
        for idx, folder in enumerate(folders):
            folder_name = folder.replace('.txt', '')
            print(f"{idx + 1}: {Fore.GREEN}{folder_name}{Style.RESET_ALL}")

        try:
            choice = int(input("Select a preset by number.\n: ")) - 1
            if 0 <= choice < len(folders):
                selected_folder = folders[choice]
                return selected_folder
            else:
                print("\nInvalid selection.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")

def get_valid_input(prompt, valid_values=None):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'back':
            return 'back'
        try:
            if valid_values is None or int(user_input) in valid_values:
                return int(user_input)
            else:
                print(f"{Fore.RED}\nInvalid option. Please choose from {valid_values}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}\nInvalid input. Please enter a valid number.{Style.RESET_ALL}")

if __name__ == "__main__":
    load_settings()
    background_autolaunch()
    print("For news and more resources, check out our discord server!\ndiscord.gg/hXyhKehEZF")

    while True:
        game_pre = ""
        run_option = input(f"\nWelcome to: Fleasion!\n"
                           f"1: {Fore.GREEN}Games{Style.RESET_ALL}\n"
                           f"2: {Fore.GREEN}Community{Style.RESET_ALL}\n"
                           f"3: {Fore.GREEN}Presets{Style.RESET_ALL}\n"
                           f"4: {Fore.GREEN}Previewer{Style.RESET_ALL}\n"
                           f"5: {Fore.GREEN}Blocker{Style.RESET_ALL}\n"
                           f"6: {Fore.GREEN}Cache Settings{Style.RESET_ALL}\n"
                           f"7: {Fore.GREEN}Fleasion Settings{Style.RESET_ALL}\n"
                           f"8: {Fore.GREEN}Credits{Style.RESET_ALL}\n"
                           f"Enter which option you want to select.\n: ").strip().lower()
        try:
            match int(run_option):
                case 1:
                    games_dir = "assets/games"
                    folders = [f for f in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, f))]

                    if not folders:
                        print(f"{Fore.RED}\nNo games available in the directory.{Style.RESET_ALL}")
                    else:
                        while True:
                            print("\nAvailable games:")
                            for idx, folder in enumerate(folders):
                                print(f"{idx + 1}: {Fore.GREEN}{folder}{Style.RESET_ALL}")

                            try:
                                choice = input("Type 'back' to return to the previous menu.\n: ")
                                if choice == 'back':
                                    break
                                choice = int(choice)-1
                                if 0 <= choice < len(folders):
                                    selected_folder = folders[choice]
                                    game_pre = os.path.join(games_dir, selected_folder, "")
                                    print(f"\nViewing: {selected_folder}")
                                    game_runner(game_pre)
                                    break
                                else:
                                    print("\nInvalid selection.")
                            except ValueError:
                                print("\nInvalid input. Please enter a number.")
                case 2:
                    community_dir = "assets/community"
                    folders = [f for f in os.listdir(community_dir) if os.path.isdir(os.path.join(community_dir, f))]

                    if not folders:
                        print(f"{Fore.RED}\nNo tweaks available in the directory.{Style.RESET_ALL}")
                    else:
                        while True:
                            print("\nAvailable tweaks:")
                            for idx, folder in enumerate(folders):
                                print(f"{idx + 1}: {Fore.GREEN}{folder}{Style.RESET_ALL}")

                            try:
                                choice = input("Select a tweak by number.\n: ")
                                if choice == 'back':
                                    break
                                choice = int(choice)-1
                                if 0 <= choice < len(folders):
                                    selected_folder = folders[choice]
                                    game_pre = os.path.join(community_dir, selected_folder, "")
                                    print(f"\nViewing: {selected_folder}")
                                    game_runner(game_pre)
                                    break
                                else:
                                    print("\nInvalid selection.")
                            except ValueError:
                                print("\nInvalid input. Please enter a number.")
                case 3:
                    preset_dir = "assets/presets"
                    folders = [f for f in os.listdir(preset_dir) if f.endswith('.txt')]                    
                    while True:                    
                        preset_option = get_valid_input(
                                        f"\nSelect preset option:\n"
                                        f"1: {Fore.GREEN}Load Preset{Style.RESET_ALL}\n"
                                        f"2: {Fore.GREEN}Create Preset{Style.RESET_ALL}\n"
                                        f"3: {Fore.GREEN}Delete Preset{Style.RESET_ALL}\n"
                                        f"Type 'back' to return to the previous menu.\n: ",
                                        valid_values=[1,2,3]
                        )
                        if preset_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to main menu.{Style.RESET_ALL}")
                            break

                        try:
                            match preset_option:
                                case 1:                    
                                    selected_folder = find_preset("")
                                    if selected_folder:
                                        with open(os.path.join(preset_dir, selected_folder), 'r') as file:
                                            preset_choice = ast.literal_eval(file.read())
                                            for i in range(0, len(preset_choice), 2):
                                                result = preset_choice[i]
                                                result2 = preset_choice[i+1]
                                                replacer(result, result2)
                                    break
                                case 2:
                                    if not session_history:
                                        print(f"{Fore.RED}\nNo history to snapshot.{Style.RESET_ALL}")
                                        break
                                    else:
                                        while True:
                                            preset_name = input("\nEnter preset name\n: ")
                                            invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
                                            if re.search(invalid_chars, preset_name):
                                                print(f"\n{Fore.RED}Invalid preset name! Preset must not contain any of the following: {invalid_chars}{Style.RESET_ALL}"); pass
                                            else:
                                                break
                                        file_path = os.path.join(preset_dir, preset_name + ".txt")
                                        try:
                                            with open(file_path, 'w') as file:
                                                file.write(str(session_history))
                                            print(f"{Fore.GREEN}\nSnapshot saved successfully as {preset_name}.{Style.RESET_ALL}")
                                        except Exception as e:
                                            print(f"{Fore.RED}\nFailed to save snapshot: {e}{Style.RESET_ALL}")
                                        break
                                case 3:
                                    selected_folder = find_preset("")
                                    if selected_folder:
                                        file_path = os.path.join(preset_dir, selected_folder)
                                        try:
                                            os.remove(file_path)
                                            print(f"File '{file_path}' was successfully deleted.")
                                        except Exception as e:
                                            print(f"An error occurred while deleting '{file_path}': {e}")
                                    break
                        except Exception as e:
                            print(f"{Fore.RED}\nAn error occurred: {e}{Style.RESET_ALL}")
                case 4:
                    pass
                case 5:
                    FILE_PATH = r"C:\Windows\System32\drivers\etc\hosts"

                    def get_confirmation():
                        """Prompt the user to confirm they want to proceed."""
                        warning_message = (
                            f"\n{Fore.RED}Warning: This script modifies the hosts file. Run as admin and proceed with caution."
                            f"\nType 'proceed' to proceed or anything else to cancel.\n: {Style.RESET_ALL}"
                        )
                        return input(warning_message).strip().lower() == "proceed"

                    def parse_hosts_file(content):
                        """Parse the hosts file to identify blocked and unblocked entries."""
                        blocked, unblocked = [], []
                        for prefix in ("c", "t"):
                            for i in range(8):
                                entry = f"127.0.0.1 {prefix}{i}.rbxcdn.com"
                                if f"#{entry}" in content:
                                    unblocked.append(f"{prefix}{i}")
                                elif entry in content:
                                    blocked.append(f"{prefix}{i}")
                        return blocked, unblocked

                    def get_user_input():
                        """Collect website block/unblock requests from the user."""
                        print("Enter c(num)/t(num) to block/unblock (type 'done' when finished):")
                        entries = []
                        while True:
                            entry = input("Enter string: ").strip().lower()
                            if entry == "done":
                                break
                            entries.append(entry)
                        return entries

                    def modify_hosts_file(content, entries):
                        """Modify the hosts file content based on user input."""
                        modified_content = content
                        for entry in entries:
                            target = f"127.0.0.1 {entry}.rbxcdn.com"
                            commented_target = f"#{target}"
                            
                            if commented_target in content:
                                modified_content = modified_content.replace(commented_target, target)
                                print(f"{entry} - Blocked!")
                            elif target in content:
                                modified_content = modified_content.replace(target, commented_target)
                                print(f"{entry} - Unblocked!")
                            else:
                                modified_content += f"\n{target}"
                                print(f"{entry} - Newly blocked!")
                        return modified_content

                    def block_main():
                        if not get_confirmation():
                            return

                        try:
                            with open(FILE_PATH, "r") as file:
                                content = file.read()
                        except Exception as e:
                            print(f"{Fore.RED}Error reading hosts file: {e}{Style.RESET_ALL}")
                            return

                        blocked, unblocked = parse_hosts_file(content)
                        print("\nCurrently blocked:", ", ".join([f"{Fore.RED}{item}{Style.RESET_ALL}" for item in blocked]))
                        print("Currently unblocked:", ", ".join([f"{Fore.GREEN}{item}{Style.RESET_ALL}" for item in unblocked]))

                        entries = get_user_input()
                        try:
                            updated_content = modify_hosts_file(content, entries)
                            with open(FILE_PATH, "w") as file:
                                file.write(updated_content)
                            print(f"{Fore.RED}Hosts file updated successfully!{Style.RESET_ALL}")
                        except Exception as e:
                            print(f"{Fore.RED}Error writing to hosts file: {e}{Style.RESET_ALL}")
                    
                    block_main()
                case 6:
                    folder_path = os.path.join(os.getenv('TEMP'), 'roblox', 'http')
                    def clear_full_cache():
                        if os.path.exists(folder_path):
                            if not os.listdir(folder_path):
                                print(f"{Fore.YELLOW}The directory {folder_path} is already empty.{Style.RESET_ALL}")
                                return
                            for filename in os.listdir(folder_path):
                                file_path = os.path.join(folder_path, filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.unlink(file_path)
                                    elif os.path.isdir(file_path):
                                        shutil.rmtree(file_path)
                                except Exception as e:
                                    print(f"Failed to delete {file_path}. Reason: {e}")
                            print(f"\n{Fore.GREEN}Cleared cache!{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}The directory {folder_path} does not exist.{Style.RESET_ALL}")

                    def delete_filtered_files():
                        def flatten(lst):
                            result = []
                            for item in lst:
                                if isinstance(item, list):
                                    result.extend(flatten(item))
                                else:
                                    result.append(item)
                            return result
                        
                        flattened_history = flatten(filtered_history)

                        for file_name in flattened_history:
                            file_path = os.path.join(folder_path, file_name)
                            
                            if os.path.exists(file_path):
                                try:
                                    os.remove(file_path)
                                    print(f"{Fore.BLUE}Deleted: {file_name}{Style.RESET_ALL}")
                                except Exception as e:
                                    print(f"{Fore.RED}Error deleting {file_name}{Style.RESET_ALL}: {e}")
                            else:
                                print(f"{Fore.RED}File not found: {file_name}{Style.RESET_ALL}")
                        
                        global session_history; session_history = []

                    while True:
                        cache_option = get_valid_input(
                                    "\nEnter cache replacement option:\n"\
                                    f"1: {Fore.GREEN}Revert Session Replacements{Style.RESET_ALL}\n"\
                                    f"2: {Fore.GREEN}Clear Full Cache{Style.RESET_ALL}\n"\
                                    f"Type 'back' to return to the previous menu.\n: ",
                                    valid_values=[1,2]
                        )
                        if cache_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to main menu.{Style.RESET_ALL}")
                            break

                        try:
                            match cache_option:
                                case 1:
                                    if not session_history:
                                        print("\nSession is empty, try making a change!"); continue
                                    filtered_history = []
                                    i = 0
                                    while i < len(session_history):
                                        item = session_history[i]
                                        if isinstance(item, list) and i + 1 < len(session_history):
                                            filtered_history.append(item)
                                            i += 2
                                        else:
                                            filtered_history.append(item)
                                            i += 1

                                    delete_filtered_files()
                                case 2:
                                    clear_full_cache()
                        except Exception as e:
                            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
                case 7:
                    settings = load_settings()
                    while True:
                        color = Fore.GREEN if startup_launch else Fore.RED
                        settings_option = get_valid_input(
                                        f"\nSelect setting option:\n"
                                        f"1: {Fore.GREEN}Apply preset on launch{Style.RESET_ALL}: {color}{startup_preset if startup_preset else 'N/A'}{Style.RESET_ALL}\n"
                                        f"2: {Fore.GREEN}Clear session history{Style.RESET_ALL}\n"
                                        f"Type 'back' to return to the previous menu.\n: ",
                                        valid_values=[1,2]
                        )
                        if settings_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to main menu.{Style.RESET_ALL}")
                            break

                        try:
                            match settings_option:
                                case 1:
                                    while True:
                                        launch_option = get_valid_input(
                                                        f"\nSelect launch option:\n"
                                                        f"1: {Fore.GREEN}Apply preset on launch:{Style.RESET_ALL} {startup_launch}\n"
                                                        f"2: {Fore.GREEN}Preset to apply on launch: {Style.RESET_ALL}{startup_preset if startup_preset else 'N/A'}\n"
                                                        f"Enter which option you want to select.\n: ",
                                                        valid_values=[1,2]
                                        )
                                        if launch_option == 'back':
                                            print(f"{Fore.CYAN}\nReturning to Fleasion settings.\n{Style.RESET_ALL}")
                                            break

                                        try:
                                            match launch_option:
                                                case 1:
                                                    settings['startup_launch'] = not settings['startup_launch']
                                                case 2:
                                                    preset_dir = "assets/presets"
                                                    folders = [f for f in os.listdir(preset_dir) if f.endswith('.txt')]
                                                    user_input = find_preset("")[:-4]
                                                    if not user_input:
                                                        break
                                                    settings['startup_preset'] = user_input
                                            with open('storage/settings.json', 'w') as file:
                                                json.dump(settings, file, indent=4)

                                            print(f"\n{Fore.GREEN}Settings have been updated.{Style.RESET_ALL}")
                                            load_settings()
                                            break
                                        except Exception as e:
                                            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
                                case 2:
                                    if not session_history:
                                        print(f"\n{Fore.GREEN}History is already empty!{Style.RESET_ALL}")
                                    else:
                                        session_history = []
                                        print(f"\n{Fore.GREEN}Reset session history!{Style.RESET_ALL}")
                                    break
                            break
                        except Exception as e:
                            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
                case 8:
                    credits = input(f"""
{Fore.YELLOW}Founded by:{Style.RESET_ALL} 
    - Crop {Fore.BLUE}@cro.p{Style.RESET_ALL}
{Fore.YELLOW}Made and continued support by:{Style.RESET_ALL}
    - Tyler {Fore.BLUE}@8ar{Style.RESET_ALL}
{Fore.YELLOW}Contributed to by:{Style.RESET_ALL} 
    - etcy {Fore.BLUE}@3tcy{Style.RESET_ALL} (run.bat)
    - yolo {Fore.BLUE}@yoloblokers{Style.RESET_ALL} (maintaining)
    - mo   {Fore.BLUE}@modraws{Style.RESET_ALL} (maintaining)
{Fore.YELLOW}Thanks to the community for supporting this project!{Style.RESET_ALL}
    - All of your supported and continued enthusiasm despite issues I may impose - Tyler
{Fore.YELLOW}Special thanks to server boosters:{Style.RESET_ALL}
    - {Fore.MAGENTA}@.ecr{Style.RESET_ALL}, {Fore.MAGENTA}@brigh.t{Style.RESET_ALL}, {Fore.MAGENTA}@gotchylds{Style.RESET_ALL}, {Fore.MAGENTA}@ihopethish_rts{Style.RESET_ALL}, {Fore.MAGENTA}@quad_tank{Style.RESET_ALL}, {Fore.MAGENTA}@riiftt{Style.RESET_ALL}, {Fore.MAGENTA}@slithercrip{Style.RESET_ALL}

Enter to return: """
                    )
                case _:
                    print(f"{Fore.RED}Invalid number.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")