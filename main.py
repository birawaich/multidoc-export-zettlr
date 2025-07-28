
from src.documentcollection import DocumentColllection
from src.documentcollection import SingleDocument

#DEBUG Settings
DocumentColllection.verbose = True
SingleDocument.VERBOSE = True

# Settings
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/ATIC__advanced-topics-in-control/build.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/ATIC__advanced-topics-in-control/build_lectures.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/NSC__nonlinear-systems-and-control/build_lectures.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/NSC__nonlinear-systems-and-control/build.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/NSC__nonlinear-systems-and-control/build_lyapunov-theory.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/MPC__model-predictive-control/build_lectures.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/MPC__model-predictive-control/build.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/PSDC__power-systems-dynamics-and-control/build_lectures.yaml'
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/REE__recursive-estimation/build_lectures.yaml' 
# builddescriptor_path = '/home/bstadler/polybox/ZETTLR_STUDIES/REE__recursive-estimation/build.yaml' 
builddescriptor_path = 'sample/build.yaml'

# SETUP

collection = DocumentColllection(builddescriptor_path)

# RUN
collection.export_collection()