from nose.tools import assert_equals
from nose.tools import assert_is_none
from nose.tools import assert_is_not_none

import deap.creator
import deap.base

from stgpfitness import STGPFitness
from hypergeometric import *

class Object(object):
    pass

def test_matchers():
    objectives = "FDSI"
    stgp = STGPFitness(objectives)

    regex = "AAAACGTAAAA"
    regex = "A"
    p_strings = ["TTTTTTTAAAACGTAAAATTTTTTT"]
    n_strings = ["TTTTTTTTTTTTTTTTTTTTTTTTT"]

    stgp.re_positive_dataset = p_strings
    stgp.re_negative_dataset = n_strings

    options = Object()
    options.training_path = "tests/resources/test_positive"
    options.background_path = "tests/resources/test_negative"

    stgp.options = options
    
    python_score = stgp.memoize_or_python_match(regex)
    python_score = [float(sprint_logx(python_score[0], 3, "%6.3fe%-5.0f"))] + [x for x in python_score[1:]]
    
    grep_score = stgp.memoize_or_grep(regex)
    grep_score = [float(sprint_logx(grep_score[0], 3, "%6.3fe%-5.0f"))] + [x for x in grep_score[1:]]
    assert_equals(python_score, [0.5, 1.0, 1.0, 0.5] )
    assert_equals(grep_score, [0.5, 1.0, 1.0, 0.5] )
    assert_equals(python_score, grep_score)
    
