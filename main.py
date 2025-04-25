# from src.singledocument import SingleDocument
# from src.functions import *

# ### Settings

# author = "Ford Prefect"

# filenames = ['sample1.md','sample2.md','sample3.md', 'sample4.md']
# # filenames = ['sample3.md']
# filepath_source = 'sample/'
# filepath_output = 'out/'
# title = "Test Samples"


# SingleDocument.verbose = True

# ### Run

# documents = []
# SingleDocument.filepath_source = filepath_source
# SingleDocument.filepath_output = filepath_output
# for filename in filenames:
#     documents.append(SingleDocument(filename))
    
# # for document in documents:
# #     print(document.get_markdown_text())
# #     print(document.get_latex_text())

# latex_total = merge_documents(documents=documents)
# latex_total = set_metadata_merged(latex_total,author=author,title=title)

# # print(latex_total)

# # Compile (2 times for correct references)
# for i in range(2):
#     compile_latex(latex_total
#                 ,output_directory=filepath_output)
    
### TEMPORARYT TESTING
from src.documentcollection import DocumentColllection
print("START TESTING")

path = 'sample/build.yaml'

collection = DocumentColllection(path)


print("END TESTING")