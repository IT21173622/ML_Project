from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT ='-e .'
def get_requirments(file_path:str)->List[str]:
    """
    this function return the list of requirments
    
    """
    requirments=[]
    with open (file_path) as file:
        requirments =file.readlines()
        requirments=[i.replace("\n","") for i in requirments]
        
        if HYPEN_E_DOT in requirments:
            requirments.remove(HYPEN_E_DOT)

    return requirments



setup(
    name='mlproject',
    version='0.0.1',
    author='Shazny',
    author_email='shazny4137@gmail.com',
    packages=find_packages(),
    install_requires=get_requirments('requirements.txt')
)


