import ast
from configparser import ConfigParser


class ConfigManager(object):
    config_file = "settings.ini"
    config = ConfigParser()

    def __init__(self):
        # Init default settings
        self.default_config = ConfigParser(allow_no_value=True)
        self.init_default()
        # Check config file exists
        try:
            with open(self.config_file) as config:
                print("\033[32m{}\033[0m".format("Settings file found!"))
        except FileNotFoundError:
            print("\033[31m{}".format("Configuration file not found!\nCreating new..."))
            self.config_create()
        self.config.read(self.config_file)

    def init_default(self):
        self.default_config.add_section("GeneralSettings")
        self.set_default("# Get in https://discord.com/developers/applications/ \n"
                         "# Create and select your application, after copy APPLICATION ID in "
                         "\"General Information\".")
        self.set_default("application_id", "")
        self.set_default("# General Status settings.\n"
                         "# Edit if you need:")
        self.set_default("next_layer_time", "7")
        self.set_default("reloading_after_exception_time", "10")
        self.set_default("start_after_launch", "False")
        self.set_default("\n#########################################################################################\n"
                         "# Layers configuration\n"
                         "# You can use <[\"text1\", \"text2\", \"...\"]> structure for randomize activity status or "
                         "<[\"text\"]> structure for single text! \n"
                         "# Contact me (https://vk.com/devildesigner) if you have some troubles.\n"
                         "#########################################################################################\n")
        self.set_default("# Buttons")
        self.set_default("first_button_layer_1_text", '["Layer 1 first Button Text"]')
        self.set_default("first_button_layer_1_url", '["https://first_button_url_here"]')
        self.set_default("second_button_layer_1_text", '["Layer 1 second Button Text"]')
        self.set_default("second_button_layer_1_url", '["https://second_button_url_here"]')
        self.set_default("first_button_layer_2_text", '["Layer 2 first Button Text"]')
        self.set_default("first_button_layer_2_url", '["https://discord.gg/YkyN4ws8C9"]')
        self.set_default("# LayersQuotes")
        self.set_default("quotes_large_image_text", '["Large Image text!"]')
        self.set_default("quotes_small_image_text", '["Small Image text!"]')
        self.set_default("window_error_large_text", '["#404: Problems Not Found."]')
        self.set_default("window_error_small_text", '["Small Image text!"]')
        self.set_default("# LayerImages")
        self.set_default("quotes_large_image", '["your_image_1_name", "your_image_2_name"]')
        self.set_default("quotes_small_image", '["your_image_3_name"]')
        self.set_default("window_error_large_image", '["your_image_4_name"]')
        self.set_default("window_error_small_image", '["your_image_5_name"]')

    def config_create(self):
        self.config = self.default_config
        self.config_update()

    def config_update(self):
        with open(self.config_file, 'w') as fp:
            self.config.write(fp)

    def set_default(self, option, value=None, section="GeneralSettings"):
        self.default_config.set(section, option, value)

    def set(self, option, value, section="GeneralSettings"):
        self.config.set(section, option, str(value))
        self.config_update()

    def get(self, option, section="GeneralSettings"):
        if self.config.has_option(section, option):
            param_value = self.config.get(section, option)
            param_value = False if param_value == '' else param_value
            try:
                param_value = ast.literal_eval(param_value)
            finally:
                return param_value

        else:
            if self.default_config.has_option(section, option):
                default_value = self.default_config.get(section, option)
                self.set(option, default_value)
                return default_value
            else:
                return None
