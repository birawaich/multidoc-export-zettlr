import os
import yaml
import warnings

from src.builddescription import BuildDescription
from src.builddescription import Section
from src.singledocument import SingleDocument

from src.functions import merge_documents
from src.functions import set_metadata_merged
from src.functions import compile_latex


class DocumentColllection:
    """Class to hold a collection incl. how it should be arranged"""

    verbose: bool = False
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
        self.check_builddescripton()

        return

    ### PUBLIC

    def export_collection(self):
        """Run an export or a Collection"""
        if self.builddescription is None:
            warnings.warn("Tried to export a collection without a Build Description. Abort.")
            return
        
        # Note: Rebuilding old code, can be adjusted

        SingleDocument.FILEPATH_SOURCE = self.builddescription.filepath_source
        SingleDocument.FILEPATH_OUTPUT = self.builddescription.filepath_destination

        filenames = self.extract_filenames()
        documents = []
        for filename in filenames:
            documents.append(SingleDocument(filename))
        

        latex_total = merge_documents(documents=documents)
        latex_total = set_metadata_merged(latex_total,
                                          author=self.builddescription.author_name,
                                          title=self.builddescription.title)

    # Compile (2 times for correct references)
        for i in range(2):
            compile_latex(latex_total
                        ,output_directory=self.builddescription.filepath_destination)

        return 


    ### PRIVATE

    def load_builddescriptor(self):
        """attempts to load the builddescription from the path given during init.
        On error: raises errors"""

        # check for existence of file
        if not os.path.exists(self.path_builddescription):
            raise ValueError(f"The path '{self.path_builddescription}' does not exist!")
        if not os.path.isfile(self.path_builddescription):
            raise ValueError(f"The path '{self.path_builddescription}' does not lead to a file!")

        # load (and watch for errors)
        with open(self.path_builddescription, "r", encoding="utf-8") as f:
            try:
                data = yaml.load(f, Loader=yaml.Loader)
            except yaml.YAMLError as e:
                raise ValueError(f"The Build Descriptor File is faulty: {e}")
                
            if type(data) != BuildDescription: #check if it is the right YAML object (if this hits, probably the YAML file is formatted wrongly)
                raise ValueError(f"The Build Descriptor File was is not of the right type but it is a {type(data)}")
            
            self.builddescription = data                

        if DocumentColllection.verbose:
            print(f"Successfully loaded the build descriptor file at {self.path_builddescription}"
                  +" and changed the working directory to there.")
        return
    
    def check_builddescripton(self):
        """checks whether the values given in a builddescripton make sense

        also makes the filepaths absolute
        
        outputs warnings if not"""
        custom_header = "[Build Description Validation] "

        # do not check if it is empty
        assert self.builddescription is not None, \
            "Trying to validate an empty Build Decription"

        # source filepath
        if not os.path.exists(self.builddescription.filepath_source):
            warnings.warn(custom_header
                          + f"Source Filepath '{self.builddescription.filepath_source}' does not exist!")
        if not os.path.isdir(self.builddescription.filepath_source):
            warnings.warn(custom_header
                          + f"Source Filepath '{self.builddescription.filepath_source}' is not a directory!")
        # destination filepath
        if not os.path.exists(self.builddescription.filepath_destination):
            warnings.warn(custom_header
                          + f"Destination Filepath '{self.builddescription.filepath_destination}' does not exist!")
        if not os.path.isdir(self.builddescription.filepath_destination):
            warnings.warn(custom_header
                          + f"Destination Filepath '{self.builddescription.filepath_destination}' is not a directory!")
        # ensure that they filepath source and destination are absolute
        self.builddescription.make_filepath_sourcedest_absolute(self.path_builddescription)

        # files

        if DocumentColllection.verbose:
            print("Successfully checked that the Build Description is valid.")
        return

    def extract_filenames(self) -> list[str]:
        """Extract all files of the Build Description
        
        Calls the recursive function `extract_filenames_recursive` under the hood."""
        local_list = []
        for elem in self.builddescription.include:
            if type(elem) == str:
                local_list.append(elem)
            elif type(elem) == Section:
                local_list.extend(self.extract_filenames_recursive(elem))
            else:
                warnings.warn(f"Unkown element in Section {type(elem)}. Ignoring it.")

        if DocumentColllection.verbose:
            print(f"Extracted {len(local_list)} files from the Build Descriptor.")

        return local_list
        
    def extract_filenames_recursive(self,
                                    section: Section) -> list[str]:
        """Recursive part of the function to collect all filenames"""
        local_list = []
        content = section.content
        for elem in content:
            if type(elem) == str:
                local_list.append(elem)
            elif type(elem) == Section:
                local_list.extend(self.extract_filenames_recursive(elem))
            else:
                warnings.warn(f"Unkown element in Section {type(elem)}. Ignoring it.")

        return local_list

