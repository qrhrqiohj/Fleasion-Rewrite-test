from colorama import Fore, Style, init
init()
import importlib.util
import os

# user guide for making your own
# addon/addon2 will set replacee/replacement to a string. addon can be a list (optional), addon2 cant
# start_key/start_key2 will start the user in a json from a set position (make sure the set position doesnt share a name or ill go to the first one)
# return json_data, start_key, start_key2, addon, addon2, skip finishes an area and returns all the data back and finishes this codes use
# add a line push(json_data, start_key, start_key2, addon, addon2, skip) for doing multiple changes of seperate things in the same case
# if you want to skip then set skip to True
# leaving empty and only returning will make the user enter 2 from the json starting from the top

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


def push(json_data, start_key, start_key2, addon, addon2, skip):
    spec = importlib.util.spec_from_file_location("backbone_module", "main.py")
    backbone_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(backbone_module)

    if hasattr(backbone_module, "backbone"):
        json_data, start_key, start_key2, addon, addon2, skip = backbone_module.backbone(json_data, start_key, start_key2, addon, addon2, skip)
    else:
        print(f"Error: The file {backbone_module} does not contain a `backbone` function.")


def run(json_data, start_key, start_key2, addon, addon2, skip):

    while True:
        options = input(f"""Asset replacements:
1:  {Fore.LIGHTMAGENTA_EX}Sights{Style.RESET_ALL}
2:  {Fore.LIGHTMAGENTA_EX}Sleeves{Style.RESET_ALL}
3:  {Fore.LIGHTMAGENTA_EX}Custom skyboxes (not added yet,,, maybe in future){Style.RESET_ALL}
4:  {Fore.LIGHTMAGENTA_EX}Gun Sounds{Style.RESET_ALL}
5:  {Fore.LIGHTMAGENTA_EX}Hit tweaks{Style.RESET_ALL}
6:  {Fore.LIGHTMAGENTA_EX}Grenade tweaks{Style.RESET_ALL}
7:  {Fore.LIGHTMAGENTA_EX}Start-up swoosh{Style.RESET_ALL}
Type 'back' to return to the previous menu.
: """).strip().lower()

        if options == "back":
            return skip
        
        try:
            match int(options):
                case 1:

                    while True:
                        sight_option = get_valid_input(
                            f"\nEnter sight option:\n"
                            f"1: {Fore.LIGHTMAGENTA_EX}Reticle tweaks{Style.RESET_ALL}\n"
                            f"2: {Fore.LIGHTMAGENTA_EX}Sight model tweaks{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )
                        if sight_option == 'back':
                            print(f"{Fore.CYAN}Returning to Asset replacements.\n{Style.RESET_ALL}")
                            break

                        match sight_option:
                            case 1:
                                start_key = "reticles"
                                start_key2 = "dumbstupidness reticles"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                while True:
                                    sightedit = get_valid_input(
                                        f"\nChoose a sight you'd like to edit:\n"
                                        f"1: {Fore.LIGHTMAGENTA_EX}Izhmash{Style.RESET_ALL}\n"
                                        f"Type 'back' to return to the previous menu.\n: ",
                                        valid_values=[1]
                                    )
                                    if sightedit == 'back':
                                        print(f"{Fore.CYAN}Returning to sight options.{Style.RESET_ALL}")
                                        break
                                    
                                    match sightedit:
                                        case 1:
                                                izhmashedit = get_valid_input(
                                                    f"\nWhat part of the Izhmash iron sights would you like deleted?:\n"
                                                    f"1: {Fore.LIGHTMAGENTA_EX}Rear{Style.RESET_ALL}\n"
                                                    f"2: {Fore.LIGHTMAGENTA_EX}Rear (detail){Style.RESET_ALL}\n"
                                                    f"3: {Fore.LIGHTMAGENTA_EX}Front{Style.RESET_ALL}\n"
                                                    f"4: {Fore.LIGHTMAGENTA_EX}Front (detail){Style.RESET_ALL}\n"
                                                    f"Type 'back' to return to the previous menu.\n: ",
                                                    valid_values=[1, 2, 3, 4]
                                                )
                                                if izhmashedit == 'back':
                                                    print(f"{Fore.CYAN}Returning to sight model tweaks.{Style.RESET_ALL}")
                                                    break
                                                match izhmashedit:
                                                    case 1:
                                                        addon = "0d910831a0fe0b50fe2c50125e7b8f52"
                                                        addon2 = "058e54ef5ad3fb914c34a6f446a36702"
                                                        return json_data, start_key, start_key2, addon, addon2, skip
                                                    case 2:
                                                        addon = "edc7f492f5384f4db6f306bf8be26341"
                                                        addon2 = "058e54ef5ad3fb914c34a6f446a36702"
                                                        return json_data, start_key, start_key2, addon, addon2, skip
                                                    case 3:
                                                        addon = "80e288c6f1ee8597b93ca2e748d1ab68"
                                                        addon2 = "058e54ef5ad3fb914c34a6f446a36702"
                                                        return json_data, start_key, start_key2, addon, addon2, skip
                                                    case 4:
                                                        addon = "ca6de453e3071d01016a0fb31d68648d"
                                                        addon2 = "058e54ef5ad3fb914c34a6f446a36702"
                                                        return json_data, start_key, start_key2, addon, addon2, skip
                case 2:
                    addon = "8813bbc8c0f7c0901fc38c1c85935fec"
                    start_key2 = "dumbstupidness skins"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 3:
                    print(f"{Fore.RED}I said it wasn't added yet, goofball.{Style.RESET_ALL}")            
                case 4:
                    start_key = "gun sounds"
                    start_key2 = "dumbstupidness sounds"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 5:
                    while True:
                        hit_option = get_valid_input(
                            f"\nEnter hit option:\n"
                            f"1: {Fore.LIGHTMAGENTA_EX}Hit sounds{Style.RESET_ALL}\n"
                            f"2: {Fore.LIGHTMAGENTA_EX}Kill sounds{Style.RESET_ALL}\n: "
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )
                        if hit_option == 'back':
                            print(f"{Fore.CYAN}Returning to Asset replacements.\n{Style.RESET_ALL}")
                            break

                        match hit_option:
                            case 1:
                                addon = "a177d2c00abd3e550b873d76c97ad960"
                                start_key2 = "dumbstupidness sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                start_key = "kill default"
                                addon2 = "dumbstupidness sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 6:
                    while True:
                        grenade_option = get_valid_input(
                            f"\nEnter grenade option:\n"
                            f"1: {Fore.LIGHTMAGENTA_EX}Explosion sound{Style.RESET_ALL}\n"
                            f"2: {Fore.LIGHTMAGENTA_EX}Grenade sound{Style.RESET_ALL}\n: "
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )
                        if grenade_option == 'back':
                            print(f"{Fore.CYAN}Returning to Asset replacements.\n{Style.RESET_ALL}")
                            break

                        match grenade_option:
                            case 1:
                                start_key = "explosions default"
                                start_key2 = "dumbstupidness sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                start_key = "grenade sound"
                                start_key2 = "dumbstupidness sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 7:
                    addon = "fdbab7608661dafc624b781910efd953"
                    start_key2 = "replacement sounds"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case _:
                    print(f"{Fore.RED}Invalid number.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")