from src.singledocument import SingleDocument
import subprocess
import os

def compile_latex(latex_content: str
                , output_directory: str='out'
                , tex_filename: str='document.tex'
                , pdf_filename: str='document.pdf') -> str:
    """
    Compile a LaTeX file to a PDF using some engine (so far: lualatex).

    Args:
        tex_filepath (str): The path to the LaTeX (.tex) file to be compiled.
        output_directory (str): The directory where the compiled PDF should be saved. Default is 'output'.
        pdf_filename (str): The name of the generated PDF file. Default is 'document.pdf'.

    Returns:
        str: The path to the generated PDF file if compilation is successful, None otherwise.

    Note: Written with ChatGPT; and modified
    """

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Write the LaTeX content to a .tex file
    tex_filepath = os.path.join(output_directory, tex_filename)
    with open(tex_filepath, 'w') as tex_file:
        tex_file.write(latex_content)

    # get the current working direction and switch to output directory (as images are relative to it)
    old_working_directory = os.getcwd()
    os.chdir(output_directory)

    # Compile the .tex file to a PDF using lualatex
    try:
        process = subprocess.run(['lualatex', #run luatex
                                  '--shell-escape', #to be able to run minted or other stop
                                  '-synctex=1', #to synch positions in the source to the PDF
                                  '-halt-on-error', #replace with `-interaction=nonstopmode` to not halt on error
                                  '-output-directory',
                                  output_directory,
                                  tex_filepath],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        
        # Check for errors
        if process.returncode != 0:
            print("Error during LaTeX compilation:")
            print(process.stdout)
            print(process.stderr)
            return None
        else:
            print("Compilation successful")
        
        # Return the path to the generated PDF
        os.chdir(old_working_directory)
        return os.path.join(output_directory, pdf_filename)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        os.chdir(old_working_directory)
        return None


def merge_documents(documents: list[SingleDocument]) -> str:
    """Merges a bunch of documents into a single latex stirng"""

    concat = ''

    for document in documents:
        latex = document.get_latex_text()

        # wrap it into a minipage
        # latex = "\\begin{minipage}{\columnwidth}\n"\
        #     + latex +"\n"\
        #     + "\end{minipage}\n"
        
        # concatenate it
        concat += latex

    # put it into the tempalte
    with open('template/template_outputfile.tex','r') as templatefile:
        template_latex = templatefile.read()

    merged = template_latex.replace('%%<content_placeholder>%%',concat)

    return merged

def set_metadata_merged(text: str, author:str, title: str) -> str:
    """set the author and the title metadat in the results"""

    text = text.replace('%%<TITLE>%%',title)
    text = text.replace('%%<AUTHOR>%%',author)

    if SingleDocument.SHOW_TAGS:
        text = text.replace('%%<LISTOFTODOS>%%','\listoftodos')

    return text