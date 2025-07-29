import pypandoc
import os
import yaml
import re
from pylatexenc.latexencode import unicode_to_latex


class SingleDocument:
    """
    Class holding information for a single document
    
    Attributes
    ----------
    _filename: str
        (private) Filename of the markdown document
    _filepath_source: str
        (private) Filepath of the source (directory)
    
    """


    FILEPATH_OUTPUT: str = ''
    """Filepath relative to CWD where output files will lie
    Used to correctly link resources for Latex generation"""

    FILEPATH_SOURCE: str = ''
    """Absolute Filepath from buildescriptor"""

    SHOW_TAGS: bool = True
    """Set to true to render tags like #todo"""

    VERBOSE: bool = False
    """Set to True for verbose info"""

    def __init__(self,
                 filepath: str):
        """
        Initialization

        Parameters
        ----------
        filepath: str,
            path to the file directly form the build descriptor file
        
        """
        # set instance variables
        self._filename: str = os.path.basename(filepath)
        self._filepath_source: str = os.path.dirname(
            os.path.abspath(
                os.path.join(SingleDocument.FILEPATH_SOURCE,filepath)
            )
        )    

        self._markdown_raw: str = None #markdown file content as text (raw = unmodified)
        self._markdown_mod: str = None #markdown file content as text (modified)
        self._latex_raw: str = None #latex representation of file (raw = unmodified)
        self._latex_mod: str = None #latex representation of file (modified)

        self._metadata: dict = None #dictionary holding metadata
        return
    
    ### PUBLIC
    
    def get_markdown_text(self) -> str:
        """return the (modified) markdown text of this document
        
        if it has not been loaded, it will do so"""

        if self._markdown_mod is not None:
            return self._markdown_mod
        
        if self._markdown_raw is not None:
            return self._modify_markdown()
        
        self._read_markdown_text()
        return self._modify_markdown()
    
    def get_latex_text(self,
                       level: int=0) -> str:
        """return the latex text of this document
        
        loads and converts it if needed
        
        Can convert it as if it is on a certain level, 0 by default"""

        if self._latex_mod is not None:
            return self._latex_mod
        
        if self._latex_raw is not None:
            return self._modify_latex(level)
        
        self.get_markdown_text() #get and modify markdown
        self._convert_to_latex()
        return self._modify_latex(level)

    
    ### PRIVATE

    def _read_markdown_text(self) -> str:
        """Reads the file specified by the filename, stores it, and returns it
        
        also loads the metadata"""
        if SingleDocument.VERBOSE:
            print("Reading content of file "+self._filename+"...")

        filepath = os.path.join(self._filepath_source,
                                self._filename)
        assert os.path.exists(filepath), \
            "Document "+filepath+" does not exist!"
        
        with open(filepath,'r',encoding='utf-8') as file:
            assert file.readable(), "File "+filepath+" is not readable!"
            content = file.read()

        ### Extract Metadata
        self._metadata = self._extract_yaml_header(content)

        self._markdown_raw = content
        return content
    
    def _modify_markdown(self) -> str:
        """Modifies the raw markdown string, stores it, and returns it"""
        if SingleDocument.VERBOSE:
            print("Mopdifying raw markdown of file "+self._filename+"...")

        assert self._markdown_raw is not None, "need to load raw markdown first!"

        ### CONVERTIONS
        converted = self._markdown_raw

        # add relative path to metadata
        relative_path = os.path.relpath(self._filepath_source, start=self.FILEPATH_OUTPUT)
        converted = self._extend_yaml_header(content=converted, new_key="resource_path_mod"
                                             ,new_value=relative_path)
        # add relative path from current directory
        relative_path_curdir = os.path.relpath(self._filepath_source)
        converted = self._extend_yaml_header(content=converted, new_key="resource_path_mod_curdir"
                                             ,new_value=relative_path_curdir)
        
        # take care of non-supported latex characters
        converted = converted.replace('\u219D', '$\leadsto$') #↝
        converted = converted.replace('\u21D2', '$\Rightarrow$') #⇒ (U+21D2)
        converted = converted.replace('\u21D0', '$\Leftarrow$') #⇐ (U+21D0)
        converted = converted.replace('\u2194', '$\leftrightarrow$') #↔ (U+2194)
        converted = converted.replace('\u21D4', '$\Leftrightarrow$')#⇔ (U+21D4)
        converted = converted.replace('\u2264', '$\leq$')#≤ (U+2264)
        converted = converted.replace('\u2265', '$\geq$')#≥ (U+2265)
        converted = converted.replace('\u2260', '$\\neq$')#≠ (U+2260)
        converted = converted.replace('\u2154', '$\sfrac{2}{3}$')#⅔ (U+2154)
        converted = converted.replace('\u2153', '$\sfrac{1}{3}$')#⅓ (U+2153)
        converted = converted.replace('\u2192', '$\\rightarrow$')#→
        converted = converted.replace('\u2190', '$\leftarrow$')#←
        converted = converted.replace('\u00B1', '$\pm$')#±

        ### STORING
        self._markdown_mod = converted
        return converted
    
    def _extend_yaml_header(self, content: str, new_key: str, new_value: str) -> str:
        """
        Add a new metadata field to the YAML front matter in a given string. Adds a YAML formatter in case none exists.

        Args:
            yaml_string (str): The string containing the YAML front matter and document content.
            new_key (str): The new metadata key to add.
            new_value (str): The new metadata value to add.

        Returns:
            str: The updated string with the new metadata field added.
        """
        # Define the regex pattern to match the YAML front matter block
        pattern = r'^(\-{3}\s*\n.*?\n)(\-{3}\s*)'
        replacement = f'\\1{new_key}: \"{new_value}\"\n\\2'
        
        # Check if YAML front matter exists
        if re.search(pattern, content, flags=re.DOTALL | re.MULTILINE):
            # If YAML front matter exists, update it
            updated_yaml_string = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)
        else:
            # If YAML front matter does not exist, add it at the beginning
            new_yaml_front_matter = f"---\n{new_key}: \"{new_value}\"\n---\n"
            updated_yaml_string = new_yaml_front_matter + content
        
        return updated_yaml_string
    
    def _extract_yaml_header(self, markdown_content: str):
        # Use a regular expression to find the YAML header at the beginning of the file
        yaml_header = re.match(r'^---\n(.*?)\n---', markdown_content, re.DOTALL)
        if yaml_header:
            yaml_content = yaml_header.group(1)
            # Parse the YAML content
            return yaml.safe_load(yaml_content)
        return None
    
    # LATEX RELATED STUFF
    
    def _convert_to_latex(self) -> str:
        """Converts the modified markdown to latex, stores it, and returns it"""
        if SingleDocument.VERBOSE:
            print("Converting modified markdown of file "+self._filename+" to Latex...")

        assert self._markdown_mod  is not None, "need to have a modified markdown text first!"

        converted = pypandoc.convert_text(source=self._markdown_mod, to='latex',format='md'
                                          ,filters=['pandocs_filters/curdir-reference-path-resources.lua'
                                                    ,'pandocs_filters/set_graphics_width.lua'
                                                    ,'pandocs_filters/mod-reference-path-resources.lua',
                                                    'pandocs_filters/custom_headers.lua']
                                        ,extra_args=[]) 
        #wirte '--standalone' to see full latex output

        self._latex_raw = converted

        return converted
    
    def _modify_latex(self,
                      level: int) -> str:
        """Modifies the raw latex string, stores it, and returns it
        
        Parameters
        ----------
        level: int
            level of this document (to be redered as such, doesn't make sense in the class, hence this is a parameter)
        """
        if SingleDocument.VERBOSE:
            print("Modifying raw latex of file "+self._filename+"...")

        assert self._latex_raw is not None, "need to convert to latex first!"

        ### CONVERTIONS

        # use metadata if available
        header = ''

        if self._metadata:
            metadata: dict = self._metadata
            if "title" in metadata:
                title_str = unicode_to_latex(metadata["title"]) #escape text to be LaTex safe
                header += "\\mezdoctitle{"+str(level)+"}{"+title_str+"}\n\n"
            if "id" in metadata:
                # add label for references from ID
                id = self._label_from_id(str(metadata["id"]))
                header += "\\label{"+id+"}\n\n"

        converted = header + self._latex_raw

        # scale images to \columnwidth in case there is no width yet
        converted = self._add_width_to_includegraphics(converted)

        # make floats floating due to issues in multicolumn
        # (https://tex.stackexchange.com/questions/12262/multicol-and-figures)
        converted = self._add_option_H_to_figures(converted)

        # convert all internal refererences to the latex command
        converted = self._replace_zettler_internal_link_with_command(converted)

        # handle the #tags
        if SingleDocument.SHOW_TAGS:
            converted = self._handle_tags(converted)

        ### STORING
        self._latex_mod = converted
        return converted
    
    def _add_width_to_includegraphics(self, content: str) -> str:
        """looks for all includegraphics and adds `\columnwidth` to the graphics in case there 
        is no defined with or height yet"""

        CM_IN_INCH = 2.54 #conversion from CM to INCH
        DPI_PICTURES = 400 #"true" DPI the pictures have
        DPI_INTERNAL = 96 #amount of DPI that pandocs uses to convert px --> inch
        MAX_SIZE_IMAGE_CM = 8.0 #maximal width of an image in CM


        # Regex pattern to find \includegraphics commands
        pattern = re.compile(r'(\\includegraphics)(\[[^\]]*\])?(\{[^}]*\})')

        def extract_numbers_from_match(match):
            #extract the inches values from a match that looks like '[width=2.66667in,height=2.66667in]'
            pattern = r'(\d+\.?\d*)'
            # Use re.findall() to extract all matching numbers
            numbers = re.findall(pattern, match)
            # Convert the extracted strings to floats
            numbers = [float(num) for num in numbers]
            return numbers

        def replace_match(match):
            prefix, options, filename = match.groups()
            if options is None:
                # No options provided, add width=\columnwidth
                return f'{prefix}[width=0.8\\columnwidth]{filename}'
            elif 'width=' not in options and 'height=' not in options:
                # Options provided but without width or height, add width=\columnwidth
                return f'{prefix}[width=0.8\\columnwidth{options[1:]}{filename}'
            else:
                # Options already contain width or height: scale it down and if too
                # large do scale
                width, height = extract_numbers_from_match(options)
                # convert to cm and scale down according to DPI
                width *= CM_IN_INCH * DPI_INTERNAL / DPI_PICTURES
                height *= CM_IN_INCH * DPI_INTERNAL / DPI_PICTURES

                # check if width is too wide --> then return the columnwidth
                if(width > MAX_SIZE_IMAGE_CM):
                    return f'{prefix}[width=0.8\\columnwidth]{filename}'
                
                return f'{prefix}[width={width}cm,height={height}cm]{filename}'

        # Replace all matches in the content
        new_content = pattern.sub(replace_match, content)
        
        return new_content
     
    def _add_option_H_to_figures(self, latex_text: str) -> str:
        # Regular expression to find figure environments without any options\n",
        pattern = r'(\\begin{figure})(?!\[\w*\])'
        # Replace those occurrences with the same string but with [H] appended
        replacement = r'\1[H]'

        modified_text = re.sub(pattern, replacement, latex_text)
        
        return modified_text
   
    def _replace_zettler_internal_link_with_command(self, latex_text: str) -> str:
        # replaces `[[20240719012226]]` with the latex command for it

        pattern = re.compile(r'\{\[\}\{\[\}(\d{14})\{\]\}\{\]\}') #note: the [[ ]] are compiled into {[}... for soem reason
        
        # replace function to use sub directly
        def local_replace_func(match):
            id = match.group(1)
            return "\hyperref["+self._label_from_id(id)+"]{\mezintreference}" #requires hyperref document

        # search for all matches
        result = pattern.sub(local_replace_func, latex_text)

        return result
    
    def _handle_tags(self, latex_text: str) -> str:
        """
        Handle all tags defined by #TAGNAME or #TAGNAME[CONTENT can be long] in markdown file

        Note: these are seen as \#TAGNAME or \#TAGNAME{[}CONTENT can be long{]} in converted latex file
        """

        pattern = re.compile(r'\\#(\w+)(?:\{\[\}(.*?)\{\]\})?',flags=re.DOTALL)

        # local replace function
        def local_replace_func(match):
            tag = match.group(1)
            content = match.group(2)
            # Example replacement — modify as you wish:
            return SingleDocument._latex_string_for_tag(tag,content)

        return pattern.sub(local_replace_func, latex_text)

    def _latex_string_for_tag(tag: str,
                              content: str) -> str:
        """returns a string for a certain tag, potentially with content
        
        Note: need to be inline as it is a multicol document"""
        if tag.lower() == 'todo':
            if content is None:
                content = "Do something!"
            return "\\todo[inline, color=tagtodo]{"+content.replace('\n',' ')+"}"
        if tag.lower() == 'question':
            if content is None:
                content = "Ask something!"
            return "\\todo[inline, color=tagquestion]{"+content.replace('\n',' ')+"}" 

        if content is not None:
            return "\\todo[inline, author="+tag+", color=tagunknown]{"+content.replace('\n',' ')+"}"
        return "\\todo[inline, color=tagunknown]{"+tag+"}"
    
    def _label_from_id(self, id: str) -> str:
        """Returns the label for a single document from the id"""
        return "singledocid:"+id