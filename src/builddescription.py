import yaml

class BuildDescription(yaml.YAMLObject):
    """
    YAML Object to represent a build description.

    Allows for easy parsing of the build description files.
    """

    yaml_tag = u'!BuildDescription'

    def __init__(self,
                 title, author_name, author_email):
        self.title = title #Title of the Build
        self.author_name = author_name #Name of the Author
        self.author_email = author_email #E-Mail of the Author

    def __repr__(self):
        """Official Way to print this object as a string."""
        return f"BuildDescrition(title={self.title},...)"
    
### TEMPORARY TESTING
print("TEST START")

test_yaml_str = """
--- !BuildDescription
title: "Sample Export"
author_name: "Arthur Dent"
author_email: "myemail@mydomain.org"
"""

loaded_obj = yaml.load(test_yaml_str,Loader=yaml.Loader)

print("TEST DONE")