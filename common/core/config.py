"""A config class object that loads the yaml file and enables the retrieval of their values"""
import yaml


class Config():

    def __init__(self, filePath: str):
        self.currentFilePath = filePath
        self.currentConfig = None

    def loadCurrentYAML(self):
        try:
            with open(self.currentFilePath, 'r') as f:
                self.currentConfig = yaml.safe_load(f)
        except FileNotFoundError:
            print("File could not be found. Please provide a valid file path")
            return None
        except yaml.YAMLError as e:
            print("YAML error: " + (e))
            return None
