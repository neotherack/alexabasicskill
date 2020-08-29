import configparser

def load_config(file):
  config = configparser.ConfigParser()
  config.read(file)
  return config
