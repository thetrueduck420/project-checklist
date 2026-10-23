import toml
import os

ConfigPath = "src/config.toml"

def ReInitConfig():
    # The default configuration
    DefaultConf = open("src/defaultconfig.toml", "r").read()
    DefaultConf = DefaultConf.replace("__USERNAMEREPLACE__", os.getlogin())

    # Write the default config if a config isnt already present
    if not os.path.exists(ConfigPath):
        open(ConfigPath, 'w').write(DefaultConf)

# Turn the configuration into a dictionary (more of a QOL function)
def IntoDict():
    with open(ConfigPath, "r") as TomlFile:
        Config = toml.load(TomlFile)
    
    return Config

# Turn a request.form into a configuration
def ConstructIntoConf(Form):
    ConfigSections = IntoDict()

    NewConfig = {}
    Settings  = []

    # split the settings into their sections, and their variable names
    for Key in Form.keys():
        Setting = Key.split(".")
        Settings.append(Setting)
    
    # Builds the toml sections
    for Setting in Settings:
        if not Setting[0] in NewConfig.keys():
            NewConfig[Setting[0]]= {}
    
    # puts toml variables into their corresponding sections
    for Setting in Settings:
        NewSetting = {Setting[1]: Form[f"{Setting[0]}.{Setting[1]}"]}
        NewConfig[Setting[0]].update(NewSetting)
        
    return NewConfig

# Write a config
def WriteConf(Config: dict):
    with open(ConfigPath, "w") as TomlFile:
        toml.dump(Config, TomlFile)

# Reset the config
def ResetConfig():
    os.remove(ConfigPath)
    ReInitConfig()

ReInitConfig()
