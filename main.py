
from src.documentcollection import DocumentColllection
from src.documentcollection import SingleDocument

#DEBUG Settings
DocumentColllection.verbose = True
SingleDocument.verbose = True

# Settings
builddescriptor_path = 'sample/build.yaml'

# SETUP
collection = DocumentColllection(builddescriptor_path)

# RUN
collection.export_collection()