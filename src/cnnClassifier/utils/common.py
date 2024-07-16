import os
from box.exceptions import BoxValueError
import yaml
from src.cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    '''read yaml file and returns
    Args:
        path_to_yaml (str): path to yaml file
    Raises:
        ValueError: if the yaml is empty
        e: empty file
    returns:
        ConfigBox: config box object
    
    '''
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'yaml file: {path_to_yaml} loaded successfully')
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError('yaml file is empty')
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose =True):
    '''Create list of directories

    Args:
    path_to_directories (list): list of directories
    ignore_log (bool, optional): Ignores if multiple dirs is to be created. Defaults to False.
    
    '''
    for  path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f'directory created at {path}')

@ensure_annotations
def save_json(path:Path, data:dict):
    '''save json file
    Args:
    path (str): path to json file
    data (dict): data to be saved in json file
    '''

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    logger.info(f'json file saved at {path}')


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    '''load the json file
    Args: 
        path(Path): path to json file
    returns:
        ConfigBox: config box object(data as a class attribute insted of dict)
    '''

    with open (path, 'r') as f:
        content = json.load(f)
    logger.info(f'json successfully loaded from : {path}')
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    '''Save any file in binary format
    args:
        data: which is to be saved as binary file
        path: path to save the file
    '''
    joblib.dump(value=data, filename=path)
    logger.info(f'binary file saved at {path}')


@ensure_annotations
def load_bin(path: Path) -> Any:
    '''load binary file
    args:
    path: path to binary file
    returns:
    data: data loaded from binary file
    '''
    data = joblib.load(path)
    logger.info(f'binary file loaded from {path}')
    return data


@ensure_annotations
def get_size(path: Path)-> str:
    '''get the size of the file in KB
    Args:
    path: path to file
    returns:
    size: size of the file
    '''
    size_in_kb = round(os.path.getsize(path)/1024)
    return f'~ {size_in_kb} KB'
    

@ensure_annotations
def decodeImage(imgstring, fileName):
    '''decode image from base64 string'''
    imagedata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imagedata)
        f.close


@ensure_annotations
def encodeImageIntoBase64(croppedImagePath):
    '''encode image to base64 string'''
    with open(croppedImagePath, 'rb') as f:
        return base64.b64encode(f.read())
        
