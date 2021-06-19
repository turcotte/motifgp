"""
Objective functions that require a number of positive successes (p), negative success (n), and the total in each class (P and N)

Each function should support p, P, n, N as parameter signature.
"""
from hypergeometric import getLogFETPvalue
from scipy.stats import fisher_exact
from math import log

class Objective(object):
    def __init__(self):
        self.f = None
        self.w = None
        self.tag = "NoName"

    def get(self):
        return [self.tag, self.f, self.w]

class Discrimination(Objective):
    def __init__(self):
        self.tag = "Discrimination"
        self.w = 1.0

        def fit_discrimination(p, _, n, __):
            if p + n == 0:
                return 0
            else:
                return p/(1.0 * (p+n))
        self.f = fit_discrimination

class Support(Objective):
    def __init__(self):
        self.tag = "Support"
        self.w = 1.0

        def fit_support(p, P, _, __):
            return p/(1.0*P)

        self.f = fit_support

class AbstractFisher(Objective):
    pvalue = None
    OR = None        

    def __init__(self):
        super(AbstractFisher, self).__init__()
        
    def refresh_stats(self, p, P, n, N):
        if p == 0:
            AbstractFisher.OR, AbstractFisher.pvalue = 0.0, 1.0
            return
        else:
            fp = P - p
            fn = N - n
        try:
            AbstractFisher.OR, AbstractFisher.pvalue = fisher_exact([[p,fp],[n,fn]], "greater")
        except Exception as e:
            print "Error!"
            print "p, fp, n, fn"
            print p, fp, n ,fn
            print P, p
            raise e
        
        #Handle ORs
        if AbstractFisher.OR == float('inf'):
            AbstractFisher.OR = float(P + p)
            #AbstractFisher.OR = float(P)
            

class ScipyFisher(AbstractFisher):
    def __init__(self):
        super(ScipyFisher, self).__init__()
        self.tag = "Fisher"
        self.w = -1.0
                
        def fit_fisher(p, P, n, N):
            self.refresh_stats(p,P,n,N)
            return AbstractFisher.pvalue
            
        self.f = fit_fisher

class ScipyOddsRatio(AbstractFisher):
    """
    Currently, this assumes Fisher is also used and precomputed before 
    """
    def __init__(self):
        super(ScipyOddsRatio, self).__init__()
        self.tag = "OR"
        self.w = 1.0
                
        def fit_OR(p, P, n, N):
            # Assuming we don't need to compute Fisher before
            return self.OR
            
        self.f = fit_OR


class Fisher(Objective):
    def __init__(self):
        self.tag = "Fisher"
        self.w = -1.0
        
        def fit_fisher(p, P, n, N):
            pvalue_threshold = 0.5
            return getLogFETPvalue(p, P, n, N, pvalue_threshold)
        
        self.f = fit_fisher
                                                                    
