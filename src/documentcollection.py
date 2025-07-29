import os
import yaml
import warnings

from src.builddescription import BuildDescription
from src.builddescription import Section
from src.singledocument import SingleDocument

from src.functions import set_metadata_merged
from src.functions import compile_latex


class SectionHeader:
    """
    Header between single documents within the document collection, specifies a section

    Attributes
    ----------
    title: str
        Title as it should be displayed
    level: int
        Level of the header: first level is 0, then increasing
    """

    def __init__(self,
                 title: str,
                 level: int=0):
        assert level >= 0, f"Invalid level {level}. Must be >= 0."
        self.title = title
        self.level = level

class SectionEnd:
    """
    Class to mark the end of a section.

    Attributes
    ----------
    level: int
        Leve of the section that ends now
    """
    def __init__(self,
                 level: int=0):
        assert level >= 0, f"Invalid level {level}. Must be >= 0."
        self.level = level        

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
        self._load_builddescriptor()
        self._check_builddescripton()

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
        SingleDocument.SHOW_TAGS = True

        # filenames = self._extract_filenames()
        # documents = []
        # for filename in filenames:
        #     documents.append(SingleDocument(filename))

        document_list = self._extract_documents()        

        latex_total = self._merge_documents(documents=document_list)
        latex_total = set_metadata_merged(latex_total,
                                          author=self.builddescription.author_name,
                                          email=self.builddescription.author_email,
                                          title=self.builddescription.title)

    # Compile (2 times for correct references)
        for i in range(2):
            compile_latex(latex_total
                        ,output_directory=self.builddescription.filepath_destination)

        return 


    ### PRIVATE

    def _load_builddescriptor(self):
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
    
    def _check_builddescripton(self):
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
    
    def _extract_documents(self,
                           entry_point: None|Section = None,
                           level: int = 0) -> list[SingleDocument | SectionHeader | SectionEnd]:
        """
        Extract all files and sections as a flat list

        Calls itself recursivly.

        Parameters
        ----------
        entry_point: None | Section
            where to start. If None is given, start at the very top
        level: int
            how deep in the hierachy the entry point is. If not supplied picks 0

        Returns
        -------
        A list of SingleDocuments and SectionHeaders that describe how the document collection looks like (flat)
        """
        if entry_point is None:
            entry_point = self.builddescription.include

        documents = []
        for elem in entry_point:
            if isinstance(elem,str): #filenname
                documents.append(SingleDocument(elem))
            elif type(elem) == Section:
                documents.append(SectionHeader(title=elem.title,
                                               level=level))
                documents.extend(self._extract_documents(
                    entry_point=elem.content,
                    level=level+1
                ))
                documents.append(SectionEnd(level=level+1))
            else:
                raise NotImplementedError(f"Unkown Element Type {type(elem)}. PANIC!")

        if level == 0 and DocumentColllection.verbose:
            print(f"Extracted {len(documents)} documents and headers from the Build Descriptor.")

        return documents

    def _extract_filenames(self) -> list[str]:
        """Extract all files of the Build Description
        
        Calls the recursive function `extract_filenames_recursive` under the hood."""
        local_list = []
        for elem in self.builddescription.include:
            if type(elem) == str:
                local_list.append(elem)
            elif type(elem) == Section:
                local_list.extend(self._extract_filenames_recursive(elem))
            else:
                warnings.warn(f"Unkown element in Section {type(elem)}. Ignoring it.")

        if DocumentColllection.verbose:
            print(f"Extracted {len(local_list)} files from the Build Descriptor.")

        return local_list
        
    def _extract_filenames_recursive(self,
                                    section: Section) -> list[str]:
        """Recursive part of the function to collect all filenames"""
        local_list = []
        content = section.content
        for elem in content:
            if type(elem) == str:
                local_list.append(elem)
            elif type(elem) == Section:
                local_list.extend(self._extract_filenames_recursive(elem))
            else:
                warnings.warn(f"Unkown element in Section {type(elem)}. Ignoring it.")

        return local_list

    def _merge_documents(self,
                         documents: list[SingleDocument|SectionHeader|SectionEnd]) -> str:
        """Merges a bunch of documents and section headers into a single latex stirng"""

        concat = ''
        current_level = 0
        for elem in documents:
            # extract elements
            if isinstance(elem, SingleDocument):
                # print(f"Adding SingleDocument {elem._filename} at level {current_level}.")
                concat += f"% DOCUMENT FROM {elem._filename}\n"\
                    +elem.get_latex_text(level=current_level)
            elif isinstance(elem, SectionHeader):
                # print(f"Adding SectionHeader {elem.title} at level {current_level}.")
                concat += "\n\n\columnbreak\n"
                concat += f"% SECTION {elem.title}\n"\
                    +"\mezsectiontitle{"+str(current_level)+"}{"+elem.title+"}"
                current_level += 1
            elif isinstance(elem,SectionEnd):
                # print(f"Adding SectionEnd")
                current_level = current_level-1
            else:
                raise NotImplementedError(f"Cannot handle an element of type {elem} here. Please try again tomorrow.")

        # put it into the tempalte
        with open('template/template_outputfile.tex','r') as templatefile:
            template_latex = templatefile.read()

        merged = template_latex.replace('%%<content_placeholder>%%',concat)

        return merged