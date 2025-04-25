import yaml
import os.path
import warnings

class Section(yaml.YAMLObject):
    """
    YAML OBject to describe a section.
    """
    yaml_tag = u'!Section'

    def __init__(self, title, content):
        self.title = title #title of the section
        self.content = content  #list of strings which are paths to files and/or sections

    def __repr__(self):
        return f"Section(title={self.title},...)"


class BuildDescription(yaml.YAMLObject):
    """
    YAML Object to represent a build description.

    Allows for easy parsing of the build description files.
    """
    yaml_tag = u'!BuildDescription'

    def __init__(self,
                 title,
                 author_name,
                 author_email,
                 filepath_source,
                 filepath_destination,
                 include):
        
        #general metadata
        self.title = title #Title of the Build
        self.author_name = author_name #Name of the Author
        self.author_email = author_email #E-Mail of the Author

        #general paths
        self.filepath_source = filepath_source #source file path (relative to build file OR absolute), paths at files will be relative to it!
        self.filepath_destination = filepath_destination #destination file path (relative to build file OR absolute), where files should be stored

        #files
        self.include = include #all files that need to be included: list of filepoths and/or sections

    def __repr__(self):
        """Official Way to print this object as a string."""
        return f"BuildDescrition(title={self.title},...)"
    
    def make_filepath_sourcedest_absolute(self, anchorpoint):
        """makes the filepath of the source and destination absolute (in case it was relative to anchorpoint)"""
        is_destination_abs = os.path.isabs(self.filepath_destination)
        is_source_abs = os.path.isabs(self.filepath_source)

        if is_destination_abs and is_source_abs:
            return

        anchor_dir = os.path.abspath(os.path.dirname(anchorpoint))
        if not os.path.isdir(anchor_dir):
            warnings.warn("The path to which the source and destination path is relative is not valid! Will not modify paths.")
    
        # proceed
        if not is_source_abs:
            self.filepath_source = os.path.abspath(
                os.path.join(anchor_dir,self.filepath_source)
            )
        if not is_destination_abs:
            self.filepath_destination = os.path.abspath(
                os.path.join(anchor_dir,self.filepath_destination)
            )

        return

### TEMPORARY TESTING
print("TEST START")

# test_yaml_str = """
# !BuildDescription
# title: "Sample Export"
# author_name: "Arthur Dent"
# author_email: "myemail@mydomain.org"
# filepath_source: ""
# filepath_destination: "../out"
# include: [
#     "sample1.md",
#     !Section {
#         title: "Supersection 1",
#         content: [
#             "sample2.md",
#             "sample3.md"
#         ]
#     },
#     !Section {
#         title: "Supersection 2",
#         content: [
#             "sample4.md",
#             "../sample_alternativesource/distributed-gradient-descent.md"
#         ]
#     }
# ]
# """
# loaded_obj = yaml.load(test_yaml_str,Loader=yaml.Loader)

with open("sample/build.yaml", "r", encoding="utf-8") as f:
    data = yaml.load(f, Loader=yaml.Loader)
    print(data)

print("TEST DONE")