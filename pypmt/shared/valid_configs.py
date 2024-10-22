from unified_planning.shortcuts import CompilationKind
from pypmt.encoders.R2E import EncoderRelaxed2Exists
from pypmt.encoders.basic import EncoderForall, EncoderSequential, EncoderExists, EncoderExistsNoProp, \
    EncoderForallNoProp, EncoderForallLazy, EncoderForallLazyStepShare, EncoderExistsLazy, EncoderExistsLazyStepShare, \
    EncoderExistsLazyPath, EncoderForallLazyEdgeCache, EncoderForallLazyNoGraph, EncoderForallLazyNeighbours, \
    EncoderForallLazyOptimal
from pypmt.encoders.SequentialLifted import EncoderSequentialLifted
from pypmt.encoders.SequentialQFUF import EncoderSequentialQFUF
from pypmt.encoders.OMT import EncoderSequentialOMT

from pypmt.planner.SMT import SMTSearch
from pypmt.planner.lifted import LiftedSearch
from pypmt.planner.QFUF import QFUFSearch
from pypmt.planner.OMT import OMTSearch

# valid configs that the library is able to operate with

grounded_encoders_default_compilation_list = [
    ('up_quantifiers_remover', CompilationKind.QUANTIFIERS_REMOVING), 
    ('up_disjunctive_conditions_remover', CompilationKind.DISJUNCTIVE_CONDITIONS_REMOVING), 
    ('up_grounder', CompilationKind.GROUNDING)
]

lifted_encoders_default_compilation_list = []

valid_configs = {
    "seq":     (EncoderSequential, SMTSearch, grounded_encoders_default_compilation_list),
    "forall":  (EncoderForall, SMTSearch, grounded_encoders_default_compilation_list),
    "exists":  (EncoderExists, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-noprop":  (EncoderForallNoProp, SMTSearch, grounded_encoders_default_compilation_list),
    "exists-noprop":  (EncoderExistsNoProp, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-lazy":  (EncoderForallLazy, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-lazy-stepshare":  (EncoderForallLazyStepShare, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-lazy-edgecache":  (EncoderForallLazyEdgeCache, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-lazy-nograph": (EncoderForallLazyNoGraph, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-lazy-neighbours": (EncoderForallLazyNeighbours, SMTSearch, grounded_encoders_default_compilation_list),
    "forall-lazy-optimal": (EncoderForallLazyOptimal, SMTSearch, grounded_encoders_default_compilation_list),
    "exists-lazy":  (EncoderExistsLazy, SMTSearch, grounded_encoders_default_compilation_list),
    "exists-lazy-stepshare":  (EncoderExistsLazyStepShare, SMTSearch, grounded_encoders_default_compilation_list),
    "exists-lazy-path":  (EncoderExistsLazyPath, SMTSearch, grounded_encoders_default_compilation_list),
    "r2e":     (EncoderRelaxed2Exists, SMTSearch,  grounded_encoders_default_compilation_list),
    "uf":      (EncoderSequentialLifted, LiftedSearch, lifted_encoders_default_compilation_list), # TODO: has to be tested and too slow
    "qfuf":    (EncoderSequentialQFUF, QFUFSearch, lifted_encoders_default_compilation_list),
    "omtseq":  (EncoderSequentialOMT, OMTSearch, grounded_encoders_default_compilation_list),
}