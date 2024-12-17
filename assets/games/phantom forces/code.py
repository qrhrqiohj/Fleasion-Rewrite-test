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


def bloxstrap():
    base_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Modifications')
    nested_folders = ["PlatformContent", "pc", "textures", "sky"]

    if not os.path.exists(base_path):
        print(f"{Fore.RED}bloxstrap not found{Style.RESET_ALL}")
    else:
        path = base_path
        for folder in nested_folders:
            path = os.path.join(path, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created folder: {path}")
            else:
                print(f"Folder already exists: {path}")

        print("All folders created successfully! Import your skyboxes into the opened folder.")
        os.startfile(path)


def run(json_data, start_key, start_key2, addon, addon2, skip):

    while True:
        options = input(f"Asset replacements:\n"
                        f"0:  {Fore.GREEN}Custom{Style.RESET_ALL}\n"
                        f"1:  {Fore.GREEN}Sights{Style.RESET_ALL}\n"
                        f"2:  {Fore.GREEN}Arm model tweaks{Style.RESET_ALL}\n"
                        f"3:  {Fore.GREEN}Sleeves{Style.RESET_ALL}\n"
                        f"4:  {Fore.GREEN}No textures{Style.RESET_ALL}\n"
                        f"5:  {Fore.GREEN}Default skyboxes{Style.RESET_ALL}\n"
                        f"6:  {Fore.GREEN}Gun skins{Style.RESET_ALL}\n"
                        f"7:  {Fore.GREEN}Gun Sounds{Style.RESET_ALL}\n"
                        f"8:  {Fore.GREEN}Gun smoke{Style.RESET_ALL}\n"
                        f"9:  {Fore.GREEN}Hit tweaks{Style.RESET_ALL}\n"
                        f"10: {Fore.GREEN}Grenade tweaks{Style.RESET_ALL}\n"
                        f"11: {Fore.GREEN}Misc tweaks{Style.RESET_ALL}\n"
                        f"Type 'back' to return to the previous menu.\n: ").strip().lower()

        if options == "back":
            return skip
        
        try:
            match int(options):
                case 0:
                    while True:
                        custom_option = get_valid_input(
                            f"\nEnter sight option:\n"
                            f"1: {Fore.GREEN}From database{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}My own{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )
                        if custom_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to Asset replacements.\n{Style.RESET_ALL}")
                            break

                        match custom_option:
                            case 1:
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                addon = input("\nEnter asset to change: ")
                                addon2 = input("\nEnter replacement: ")
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 1:
                    while True:
                        sight_option = get_valid_input(
                            f"\nEnter sight option:\n"
                            f"1: {Fore.GREEN}Reticle tweaks{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}Sight model tweaks{Style.RESET_ALL}\n"
                            f"3: {Fore.GREEN}Ballistics tracker tweaks{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2, 3]
                        )
                        if sight_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to Asset replacements.\n{Style.RESET_ALL}")
                            break

                        match sight_option:
                            case 1:
                                start_key = "reticles"
                                start_key2 = "reticle replacement"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                while True:
                                    sightbackground = get_valid_input(
                                        f"\nEnter background tweak:\n"
                                        f"1: {Fore.GREEN}clear coyote blue background{Style.RESET_ALL}\n"
                                        f"2: {Fore.GREEN}clear reflex blue background{Style.RESET_ALL}\n"
                                        f"3: {Fore.GREEN}clear okp-7 blue background{Style.RESET_ALL}\n"
                                        f"4: {Fore.GREEN}clear delta black ring{Style.RESET_ALL}\n"
                                        f"5: {Fore.GREEN}remove sniper black circle{Style.RESET_ALL}\n"
                                        f"6: {Fore.GREEN}remove glass hack border{Style.RESET_ALL}\n"
                                        f"Type 'back' to return to the previous menu.\n: ",
                                        valid_values=[1, 2, 3, 4, 5, 6]
                                    )
                                    if sightbackground == 'back':
                                        print(f"{Fore.CYAN}\nReturning to sight options.{Style.RESET_ALL}")
                                        break

                                    match sightbackground:
                                        case 1:
                                            addon = "3fc9141fc7c1167c575b9361a98f04c0"
                                            addon2 = "5873cfba79134ecfec6658f559d8f320"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 2:
                                            addon = "2eaae4fe3a9fce967af993d27ad68d52"
                                            addon2 = "5873cfba79134ecfec6658f559d8f320"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 3:
                                            addon = "2eaae4fe3a9fce967af993d27ad68d52"
                                            addon2 = "5873cfba79134ecfec6658f559d8f320"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 4:
                                            addon = ['30c4d2bb30b6b8c9ac7cfeec5db25a85', '7d5652167ec33ed349e569a55a398705']
                                            addon2 = "75205be5a167842c7ed931d9d5a904ca"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 5:
                                            addon = ['a883a2373ad6931556dce946c50c3690', '5a2a41b0da7ec98bf25780bb3f5d071f']
                                            addon2 = "75205be5a167842c7ed931d9d5a904ca"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 6:
                                            addon = '1764672fe43c9f1d129b3d51dc3c40ee'
                                            addon2 = '75205be5a167842c7ed931d9d5a904ca'
                                            return json_data, start_key, start_key2, addon, addon2, skip
                            case 3:
                                addon = "0847bd551fe2cbe953a3c3670eac79b1"
                                start_key2 = "ballistics tracker"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 2:
                    while True:
                        arm_option = get_valid_input(
                            f"\nEnter arm option:\n"
                            f"1: {Fore.GREEN}Remove options{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}Bone arms{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )

                        if arm_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to Asset replacements.\n{Style.RESET_ALL}")
                            break

                        match arm_option:
                            case 1:
                                start_key = "arm models"
                                addon2 = "5873cfba79134ecfec6658f559d8f320"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                start_key = "bare arms"
                                addon2 = "5873cfba79134ecfec6658f559d8f320"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 3:
                    addon = "8813bbc8c0f7c0901fc38c1c85935fec"
                    start_key2 = "skins"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 4:
                    start_key = "textures"
                    addon2 = "75205be5a167842c7ed931d9d5a904ca"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 5:
                    while True:
                        sky_option = get_valid_input(
                            f"\nIs Bloxstrap sky folder setup?\n"
                            f"1: {Fore.GREEN}yes{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}no{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2]
                        )

                        if sky_option == 'back':
                            print(f"\n{Fore.CYAN}\nReturning to Asset replacements.{Style.RESET_ALL}")
                            break

                        match sky_option:
                            case 1:
                                start_key = "skyboxes"
                                addon2 = "75205be5a167842c7ed931d9d5a904ca"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                bloxstrap()
                                start_key = "skyboxes"
                                addon2 = "75205be5a167842c7ed931d9d5a904ca"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 6:
                    start_key = "gun skins"
                    start_key2 = "skins"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 7:
                    start_key = "gun sounds"
                    start_key2 = "replacement sounds"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 8:
                    addon = "8194373fb18740071f5e885bab349252"
                    start_key2 = "gun smoke"
                    return json_data, start_key, start_key2, addon, addon2, skip
                case 9:
                    while True:
                        hit_option = get_valid_input(
                            f"\nEnter hit option:\n"
                            f"1: {Fore.GREEN}Hitmarkers{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}Hit sounds{Style.RESET_ALL}\n"
                            f"3: {Fore.GREEN}Kill sounds{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2, 3]
                        )
                        if hit_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to Asset replacements.{Style.RESET_ALL}")
                            break

                        match hit_option:
                            case 1:
                                addon = "097165b476243d2095ef0a256320b06a"
                                start_key2 = "hitmarker"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                addon = "a177d2c00abd3e550b873d76c97ad960"
                                start_key2 = "replacement sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 3:
                                start_key = "kill default"
                                start_key2 = "replacement sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 10:
                    while True:
                        grenade_option = get_valid_input(
                            f"\nEnter grenade option:\n"
                            f"1: {Fore.GREEN}Model tweaks{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}Explosion sound{Style.RESET_ALL}\n"
                            f"3: {Fore.GREEN}Grenade sound{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2, 3]
                        )
                        if grenade_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to Asset replacements.{Style.RESET_ALL}")
                            break

                        match grenade_option:
                            case 1:
                                while True:
                                    grenade_model_option = get_valid_input(
                                        f"\nEnter model option:\n"
                                        f"1: {Fore.GREEN}RGD{Style.RESET_ALL}\n"
                                        f"2: {Fore.GREEN}Bundle{Style.RESET_ALL}\n"
                                        f"Type 'back' to return to the previous menu.\n: ",
                                        valid_values=[1, 2]                                        
                                    )

                                    if grenade_model_option == 'back':
                                        print(f"{Fore.CYAN}\nReturning to Asset replacements.{Style.RESET_ALL}")
                                        break

                                    match grenade_model_option:
                                        case 1:
                                            start_key = "rgd main"
                                            addon2 = "5873cfba79134ecfec6658f559d8f320"
                                            push(json_data, start_key, start_key2, addon, addon2, skip)
                                            start_key = "rgd junk"
                                            start_key2 = "grenades"
                                            push(json_data, start_key, start_key2, addon, addon2, skip)
                                            start_key = "rgd texture"
                                            start_key2 = "grenades"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 2:
                                            start_key = "bundle main"
                                            addon2 = "5873cfba79134ecfec6658f559d8f320"
                                            push(json_data, start_key, start_key2, addon, addon2, skip)
                                            start_key = "bundle junk"
                                            start_key2 = "grenades"
                                            push(json_data, start_key, start_key2, addon, addon2, skip)
                                            start_key = "bundle texture"
                                            start_key2 = "grenades"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                start_key = "explosions default"
                                start_key2 = "replacement sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 3:
                                start_key = "grenade sound"
                                start_key2 = "replacement sounds"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case 11:
                    while True:
                        misc_option = get_valid_input(
                            f"\nEnter misc option:\n"
                            f"1: {Fore.GREEN}M21 Garand Ping{Style.RESET_ALL}\n"
                            f"2: {Fore.GREEN}BFG Machina Sounds{Style.RESET_ALL}\n"
                            f"3: {Fore.GREEN}Damage Affect Tweaks{Style.RESET_ALL}\n"
                            f"4: {Fore.GREEN}Remove Flashlight Beam{Style.RESET_ALL}\n"
                            f"5: {Fore.GREEN}Remove Bullet Casing Sounds{Style.RESET_ALL}\n"
                            f"Type 'back' to return to the previous menu.\n: ",
                            valid_values=[1, 2, 3, 4, 5]
                        )

                        if misc_option == 'back':
                            print(f"{Fore.CYAN}\nReturning to Asset replacements.\n{Style.RESET_ALL}")
                            break   

                        match misc_option:
                            case 1:
                                addon = ["07fe5c19cdd350a4922412d00d567edd", "17bb7bd20bf6e1b41214619d16698ff4", "b36ed668aea77715747e3ebadce8a439", "fbc5302726777295ae2ccd092d2748f9"]
                                addon2 = "5873cfba79134ecfec6658f559d8f320"
                                push(json_data, start_key, start_key2, addon, addon2, skip)
                                addon = "877cb2de0924e058860135f72e800aad"
                                addon2 = "9296d1de6b6a994aee0f95c1f5206b58"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 2:
                                addon = "9d1808db108b86ddaeda18968a23a804"
                                addon2 = "1689699496f4cf0e2f0fade63f68b83a"
                                push(json_data, start_key, start_key2, addon, addon2, skip)
                                addon = ["3ad4ddcb4c77ab8bdfc83cf9c0cfafa9", "edf091bb925fa87900910e501da97018", "768131a75f0d2d95e6799a0a5acd67c6", "3d92b91e96ef916b6717a53ef3f3a442", "32e321c27457289889ac0d5fa72f7d97"]
                                addon2 = "5873cfba79134ecfec6658f559d8f320"
                                push(json_data, start_key, start_key2, addon, addon2, skip)
                                addon = "160883329152d9abc5434a1b0982ec7d"
                                addon2 = "0d05028f1eaeb0b97ecd0c473b484371"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 3:                              
                                while True:
                                    damage_option = get_valid_input(
                                        f"\nEnter misc option:\n"
                                        f"1: {Fore.GREEN}Remove Damage Effect{Style.RESET_ALL}\n"
                                        f"2: {Fore.GREEN}Anti Damage Affect{Style.RESET_ALL}\n"
                                        f"Type 'back' to return to the previous menu.\n: ",
                                        valid_values=[1, 2]
                                    )

                                    if damage_option == 'back':
                                        print(f"{Fore.CYAN}\nReturning to misc tweaks.{Style.RESET_ALL}")
                                        break    
                                    
                                    match damage_option:
                                        case 1:
                                            addon = "a0542ee89ad3cc311bb3f7d23ef94fe4"
                                            addon2 = "5873cfba79134ecfec6658f559d8f320"
                                            return json_data, start_key, start_key2, addon, addon2, skip
                                        case 2:
                                            addon = "a0542ee89ad3cc311bb3f7d23ef94fe4"
                                            addon2 = "614546fcea8e0411a1c94d669809a459"
                                            return json_data, start_key, start_key2, addon, addon2, skip                                           
                            case 4:
                                addon = "960b11e6e7d549c8b12044201025093f"
                                addon2 = "ac59980bedb36f4b240633b08b532d08"
                                return json_data, start_key, start_key2, addon, addon2, skip
                            case 5:
                                addon = ["7b11fe3312b0801492d3e0f8dce62043", "853395973e94bf11a1c9edb8110da786", "1a566c1fd2deac2677bfa26b357b5cf9", "134d345ef675a18d2c73cdbb5ca03394", "f191e4a1f7ff200c57229c8c65c2e763", "18957c939764efa83229b65a05ab3fa7"]
                                addon2 = "5873cfba79134ecfec6658f559d8f320"
                                return json_data, start_key, start_key2, addon, addon2, skip
                case _:
                    print(f"{Fore.RED}Invalid number.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")