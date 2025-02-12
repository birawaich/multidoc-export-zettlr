from src.singledocument import SingleDocument
import subprocess
import os

def compile_latex(latex_content: str
                , output_directory: str='out'
                , tex_filename: str='document.tex'
                , pdf_filename: str='document.pdf') -> str:
    """
    Compile a LaTeX file to a PDF using some engine (so far: pdflatex).

    Args:
        tex_filepath (str): The path to the LaTeX (.tex) file to be compiled.
        output_directory (str): The directory where the compiled PDF should be saved. Default is 'output'.
        pdf_filename (str): The name of the generated PDF file. Default is 'document.pdf'.

    Returns:
        str: The path to the generated PDF file if compilation is successful, None otherwise.

    Note: Written with ChatGPT
    """

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Write the LaTeX content to a .tex file
    tex_filepath = os.path.join(output_directory, tex_filename)
    with open(tex_filepath, 'w') as tex_file:
        tex_file.write(latex_content)
    
    # Compile the .tex file to a PDF using pdflatex
    try:
        process = subprocess.run(['pdflatex', '-halt-on-error'
                                  , '-output-directory', output_directory, tex_filepath],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check for errors
        if process.returncode != 0:
            print("Error during LaTeX compilation:")
            print(process.stdout)
            print(process.stderr)
            return None
        else:
            print("Compilation successful")
        
        # Return the path to the generated PDF
        return os.path.join(output_directory, pdf_filename)
    
    except Exception as e:
        print(f"An error occurred: {e}")
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

    return text