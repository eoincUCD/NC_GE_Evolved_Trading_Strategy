from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from stats.stats import stats, get_stats

import numpy as np

"""Hill-climbing is just about the simplest metaheuristic there
is. It's of interest in GP/GE because of the lingering suspicion among
many researchers that crossover just doesn't work. This goes back to
90s work by Chellapilla and by O'Reilly. Today, many papers are
published which use mutation only.

Even a simple hill-climber may work well in GP/GE. However, the main
purpose of this module is to provide two modern hill-climbing methods
proposed by Bykov: late-acceptance hill-climbing (LAHC) and
step-counting hill-climbing (SCHC). Both reduce to simple
hill-climbing (HC) with a particular parameter choice, so this module
provides HC as a by-product.

Both LAHC and SCHC are implemented as search_loop-type functions. They
don't provide/require a step-style function. Hence, to use these, just
pass the appropriate dotted function name:

--search_loop algorithm.hill_climbing.LAHC_loop
--search_loop algorithm.hill_climbing.SCHC_loop


LAHC is a hill-climbing algorithm with a history mechanism. The
history mechanism is very simple (one extra parameter: the length of
the history) but in some domains it seems to provide a remarkable
performance improvement compared to hill-climbing itself and other
heuristics. It hasn't previously been used in GP/GE.

LAHC was proposed by Bykov [http://www.cs.nott.ac.uk/~yxb/LAHC/LAHC-TR.pdf].

In standard hill-climbing, where we accept a move to a new proposed
point (created by mutation) if that point is as good as or better than
the current point.

In LAHC, we accept the move if the new point is as good as or better
than that we encountered L steps ago (L for history length).

LAHC is not to be confused with an acceptance to the GECCO
late-breaking papers track.

Step-counting hill-climbing
[http://link.springer.com/article/10.1007/s10951-016-0469-x] is a
variant, proposed by Bykov as an improvement on LAHC. Although less
"natural" it may be slightly simpler to tune again. In SCHC, we
maintain a threshold cost value. We accept moves which are better than
that. We update it every L steps to the current cost value.

There are also two variants: instead of counting all steps, we can
count only accepted, or only improving moves.
"""


def LAHC_search_loop():
    """
    Search loop for Late Acceptance Hill Climbing.
    
    This is the LAHC pseudo-code from Bykov and Burke.

        Produce an initial solution s
        Calculate initial cost function C(s)
        Specify Lfa
        For all k in {0...Lfa-1} f_k := C(s)
        First iteration I=0;
        Do until a chosen stopping condition
            Construct a candidate solution s*
            Calculate its cost function C(s*)
            v := I mod Lfa
            If C(s*)<=fv or C(s*)<=C(s)
            Then accept the candidate (s:=s*)
            Else reject the candidate (s:=s)
            Insert the current cost into the fitness array fv:=C(s)
            Increment the iteration number I:=I+1
    
    :return: The final population.
    """

    maximise = params['FITNESS_FUNCTION'].maximise
    max_its = params['POPULATION_SIZE'] * params['GENERATIONS']

    # Initialise population
    individuals = params['INITIALISATION'](params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    Lfa = params['HILL_CLIMBING_HISTORY']
    s = stats['best_ever']
    Cs = s.fitness
    f = Cs * np.ones(Lfa)  # history

    I = len(individuals)
    for generation in range(1, (params['GENERATIONS']+1)):

        this_gen = []

        # even though there is no population, we will take account of
        # the pop size parameter: ie we'll save stats after every
        # "generation"
        for j in range(params['POPULATION_SIZE']):

            this_gen.append(s)  # collect this "generation"

            s_ = params['MUTATION'](s)  # mutate s to get candidate s*
            if not s_.invalid:
                s_.evaluate()
            Cs_ = s.fitness

            v = I % Lfa
            # ugly
            if ((maximise and (Cs_ >= f[v] or Cs_ >= Cs)) or
                    (not maximise and (Cs_ <= f[v] or Cs_ <= Cs))):
                # accept the candidate
                s = s_
                Cs = Cs_
            else:
                pass  # reject the candidate

            f[v] = Cs
            I += 1

            # break from inner and outer if needed
            if I >= max_its:
                break

        # but get this get stats first
        stats['gen'] = generation
        get_stats(this_gen)

        if I >= max_its:
            break

    return individuals


def SCHC_search_loop():
    """
    Search Loop for Step-Counting Hill-Climbing.
    
    This is the SCHC pseudo-code from Bykov and Petrovic.

        Produce an initial solution s
        Calculate an initial cost function C(s)
        Initial cost bound Bc := C(s)
        Initial counter nc := 0
        Specify Lc
        Do until a chosen stopping condition
            Construct a candidate solution s*
            Calculate the candidate cost function C(s*)
            If C(s*) < Bc or C(s*) <= C(s)
                Then accept the candidate s := s*
                Else reject the candidate s := s
            Increment the counter nc := nc + 1
            If nc >= Lc
                Then update the bound Bc := C(s)
                reset the counter nc := 0
        
        Two alternative counting methods (start at the first If):
        
        SCHC-acp counts only accepted moves:
        
            If C(s*) < Bc or C(s*) <= C(s)
                Then accept the candidate s := s*
                     increment the counter nc := nc + 1
                Else reject the candidate s := s
            If nc >= Lc
                Then update the bound Bc := C(s)
                     reset the counter nc := 0
        
        SCHC-imp counts only improving moves:
        
            If C(s*) < C(s)
                Then increment the counter nc := nc + 1
            If C(s*) < Bc or C(s*) <= C(s)
                Then accept the candidate s := s*
                Else reject the candidate s := s
            If nc >= Lc
                Then update the bound Bc := C(s)
                     reset the counter nc := 0
    
    :return: The final population.
    """
    
    maximise = params['FITNESS_FUNCTION'].maximise
    max_its = params['POPULATION_SIZE'] * params['GENERATIONS']
    count_method = "all"  # TODO
    accept_method = "bykov"  # TODO

    # Initialise population
    individuals = params['INITIALISATION'](params['POPULATION_SIZE'])

    # Evaluate initial population
    individuals = evaluate_fitness(individuals)

    # Generate statistics for run so far
    get_stats(individuals)

    Lc = params['HILL_CLIMBING_HISTORY']
    s = stats['best_ever']
    Cs = s.fitness
    Bc = Cs  # initial cost bound
    nc = 0

    I = len(individuals)
    for generation in range(1, (params['GENERATIONS']+1)):

        this_gen = []

        # even though there is no population, we will take account of
        # the pop size parameter: ie we'll save stats after every
        # "generation"
        for j in range(params['POPULATION_SIZE']):

            this_gen.append(s)  # collect this "generation"

            s_ = params['MUTATION'](s)  # mutate s to get candidate s*
            if not s_.invalid:
                s_.evaluate()
            Cs_ = s.fitness

            # count
            if count_method == "all":  # we count all iterations (moves)
                nc += 1  # increment the counter
            
            elif count_method == "acp":  # we count accepted moves only
                if ((maximise and (Cs_ > Bc or Cs_ >= Cs)) or
                        ((not maximise) and (Cs_ < Bc or Cs_ <= Cs))):
                    nc += 1  # increment the counter
            
            elif count_method == "imp":  # we count improving moves only
                if ((maximise and Cs_ > Cs) or
                        ((not maximise) and Cs_ < Cs)):
                    nc += 1  # increment the counter
            
            else:
                raise ValueError("Unknown count method " + count_method)

            # accept
            if accept_method == "bykov":
                # standard accept method
                if ((maximise and (Cs_ > Bc or Cs_ >= Cs)) or
                        ((not maximise) and (Cs_ < Bc or Cs_ <= Cs))):
                    s = s_  # accept the candidate
                    Cs = Cs_
                
                else:
                    pass  # reject the candidate

            elif accept_method == "nicolau":
                # simpler alternative suggested by Nicolau, unpublished
                if ((maximise and Cs_ >= Bc) or
                        ((not maximise) and (Cs_ <= Bc))):
                    s = s_  # accept the candidate
                    Cs = Cs_
                
                else:
                    pass  # reject the candidate

            else:
                raise ValueError("Unknown accept method " + accept_method)

            if nc >= Lc:
                Bc = Cs  # update the bound
                nc = 0  # reset the counter
            I += 1

            # break from inner and outer if needed
            if I >= max_its:
                break

        # but get this gen stats first
        stats['gen'] = generation
        get_stats(this_gen)

        if I >= max_its:
            break

    return individuals
