import os
import yaml

from src.builddescription import BuildDescription


class DocumentColllection:
    """Class to hold a collection incl. how it should be arranged"""

    verbose: bool = True
    """Set to True for verbose info"""

    ### CLASS VARIABLES

    def __init__(self,
                 path_builddescription: str):
        # Set Instance Variables

        self.path_builddescription = os.path.abspath(path_builddescription)
        """Filepath to the build descriptor file. Absolute. Will be used as working directory."""

        self.builddescription: BuildDescription = None #holds build description

        # Run functions
        self.load_builddescriptor()

        return
    

    ### PUBLIC


    ### PRIVATE

    def load_builddescriptor(self):
        """attempts to load the builddescription from the path given during init.
        On error: raises errors"""
        absolute_path = self.path_builddescription

        # check for existence of file
        if not os.path.exists(self.path_builddescription):
            raise ValueError(f"The path '{self.path_builddescription}' does not exist!")
        if not os.path.isfile(self.path_builddescription):
            raise ValueError(f"The path '{self.path_builddescription}' does not lead to a file!")

        # load (and watch for errors)
        with open(self.path_builddescription, "r", encoding="utf-8") as f:
            data = yaml.load(f,Loader=yaml.Loader)
            if type(data) != BuildDescription: #check if it is the right YAML object (if this hits, probably the YAML file is formatted wrongly)
                raise ValueError(f"The Build Descriptor File was is not of the right type but it is a {type(data)}")
            self.builddescription = data                

        # change the working directory
        directory = os.path.dirname(absolute_path)
        os.chdir(directory)

        if DocumentColllection.verbose:
            print(f"Successfully loaded the build descriptor file at {self.path_builddescription}"
                  +" and changed the working directory to there.")
        return
    

