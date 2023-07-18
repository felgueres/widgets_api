import yaml

def load_yaml(path): 
    return yaml.safe_load(open(path,'r'))