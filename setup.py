import json
import os
from selenium import webdriver
from pathlib import Path
from halo import Halo
from colorama import Fore
import log_neko


def create_defaultConfig():
    default_data ={
        "first_run" : True,
        "email" : "Email",
        "password" : "Password",
        "browser" : ""
        }    
    json_object = json.dumps(default_data)

    with open("config.json", "w") as file:
        file.write(json_object)

def load_config():
    with open("config.json", "r") as config_file:
        try:
            config = json.load(config_file)
        except json.decoder.JSONDecodeError:
            config = {}

        return config

def save_to_config(config):
    with open("config.json", "w") as config_file:
        json.dump(config, config_file)


def first_run():
    try:
        first_run = load_config().get("first_run")
    except FileNotFoundError:
        log_neko.message_info("no config file found")

        create_file_info = Halo(spinner='dots')
        create_file_info.start("Creating default config file", )

        create_defaultConfig()
        
        create_file_info.succeed("Default config file created")

        first_run = True

    if first_run is True or first_run is None:
        return True
    
    return False

def get_details():
    _email = str(input("Siakad Email : "))
    _password = str(input("Siakad Password : "))
    _browser = str(input("Browser : "))
    return _email, _password, _browser

def set_details():
    _email, _password, _browser = get_details()

    try:
        config = load_config()
    except json.decoder.JSONDecodeError:
        config = {}

    config["first_run"] = False
    config["email"] = _email
    config["password"] = _password
    config["browser"] = _browser

    save_to_config(config)

@Halo(text=log_neko.compose_info("Getting webdriver..."), spinner="unicorn")
def setup_webdriver():
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False' #remove the space from log
    os.environ['WDM_LOG_LEVEL'] = '0' #silent the webdriver_manager log

    browser = load_config().get('browser').lower()
    driver = ""
    if browser == "firefox":
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser == "chrome":
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "edge":
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    return driver
    

if __name__ == '__main__':
    if not first_run():
        log_neko.message_W("This is not your first run, are you sure to reconfigure?")
        try:
            input("Press enter to continue or Ctrl+C to quit ")
        except KeyboardInterrupt:
            exit(log_neko.message_info("Exiting"))

    Path("config.json").touch(exist_ok=True)

    set_details()
