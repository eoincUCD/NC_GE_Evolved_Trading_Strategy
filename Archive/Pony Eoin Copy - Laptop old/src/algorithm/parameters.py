from multiprocessing import cpu_count
from os import path
from socket import gethostname

hostname = gethostname().split('.')
machine_name = hostname[0]


"""Algorithm parameters"""
params = {
        # Set default step and search loop functions
        'SEARCH_LOOP': 'search_loop',
        'STEP': 'step',

        # Evolutionary Parameters
        'POPULATION_SIZE': 500,
        'GENERATIONS': 50,
        'HILL_CLIMBING_HISTORY': 1000,

        # Set optional experiment name
        'EXPERIMENT_NAME': None,
        # Set default number of runs to be done.
        # ONLY USED WITH EXPERIMENT MANAGER.
        'RUNS': 1,

        # Class of problem
        'FITNESS_FUNCTION': "supervised_learning.regression",

        # Select problem dataset
        'DATASET_TRAIN': "Vladislavleva4/Train.txt",
        'DATASET_TEST': "Vladislavleva4/Test.txt",
        'DATASET_DELIMITER': None,

        # Set grammar file
        'GRAMMAR_FILE': "supervised_learning/Vladislavleva4.bnf",

        # Select error metric
        'ERROR_METRIC': None,
        # "mse"
        # "mae"
        # "rmse"
        # "hinge"
        # "f1_score"

        'OPTIMIZE_CONSTANTS': False,

        # Specify target for target problems
        'TARGET': "ponyge_rocks",

        # Set max sizes of individuals
        'MAX_TREE_DEPTH': 90,  # SET TO 90 DUE TO PYTHON EVAL() STACK LIMIT.
                               # INCREASE AT YOUR OWN RISK.
        'MAX_TREE_NODES': None,
        'CODON_SIZE': 100000,
        'MAX_GENOME_LENGTH': None,
        'MAX_WRAPS': 0,

        # INITIALISATION
        'INITIALISATION': "operators.initialisation.PI_grow",
        # "operators.initialisation.uniform_genome"
        # "operators.initialisation.rhh"
        # "operators.initialisation.PI_grow"
        'INIT_GENOME_LENGTH': 200,
        # Set the maximum geneome length for initialisation.
        'MAX_INIT_TREE_DEPTH': 10,
        # Set the maximum tree depth for initialisation.
        'MIN_INIT_TREE_DEPTH': None,
        # Set the minimum tree depth for initialisation.

        # SELECTION
        'SELECTION': "operators.selection.tournament",
        # "operators.selection.tournament"
        # "operators.selection.truncation",
        'TOURNAMENT_SIZE': 2,
        # For tournament selection
        'SELECTION_PROPORTION': 0.5,
        # For truncation selection
        'INVALID_SELECTION': False,
        # Allow for selection of invalid individuals during selection process.

        # OPERATOR OPTIONS
        'WITHIN_USED': True,
        # Boolean flag for selecting whether or not mutation is confined to
        # within the used portion of the genome. Default set to True.

        # CROSSOVER
        'CROSSOVER': "operators.crossover.variable_onepoint",
        # "operators.crossover.fixed_onepoint",
        # "operators.crossover.subtree",
        'CROSSOVER_PROBABILITY': 0.75,
        'NO_CROSSOVER_INVALIDS': False,
        # Prevents crossover from generating invalids.

        # MUTATION
        'MUTATION': "operators.mutation.int_flip_per_codon",
        # "operators.mutation.subtree",
        # "operators.mutation.int_flip_per_codon",
        # "operators.mutation.int_flip_per_ind",
        'MUTATION_PROBABILITY': None,
        'MUTATION_EVENTS': 1,
        'NO_MUTATION_INVALIDS': False,
        # Prevents mutation from generating invalids.

        # REPLACEMENT
        'REPLACEMENT': "operators.replacement.generational",
        # "operators.replacement.generational",
        # "operators.replacement.steady_state",
        'ELITE_SIZE': None,

        # DEBUGGING
        # Use this to turn on debugging mode. This mode doesn't write any files
        # and should be used when you want to test new methods.
        'DEBUG': False,

        # PRINTING
        # Use this to print out basic statistics for each generation to the
        # command line.
        'VERBOSE': False,
        # Use this to prevent anything being printed to the command line.
        'SILENT': False,

        # SAVING
        'SAVE_ALL': False,
        # Use this to save the phenotype of the best individual from each
        # generation. Can generate a lot of files. DEBUG must be False.
        'SAVE_PLOTS': True,
        # Saves a plot of the evolution of the best fitness result for each
        # generation.

        # MULTIPROCESSING
        'MULTICORE': False,
        # Multiprocessing of phenotype evaluations.
        'CORES': cpu_count(),

        # STATE SAVING/LOADING
        'SAVE_STATE': False,
        # Saves the state of the evolutionary run every generation. You can
        # specify how often you want to save the state with SAVE_STATE_STEP.
        'SAVE_STATE_STEP': 1,
        # Specifies how often the state of the current evolutionary run is
        # saved (i.e. every n-th generation). Requires int value.
        'LOAD_STATE': None,
        # Loads an evolutionary run from a saved state. You must specify the
        # full file path to the desired state file. Note that state files have
        # no file type.

        # SEEDING
        'SEED_INDIVIDUALS': [],
        # Specify a list of PonyGE2 individuals with which to seed the initial
        # population.
        'TARGET_SEED_FOLDER': None,
        # Specify a target seed folder in the 'seeds' directory that contains a
        # population of individuals with which to seed a run.
    
        # CACHING
        'CACHE': False,
        # The cache tracks unique individuals across evolution by saving a
        # string of each phenotype in a big list of all phenotypes. Saves all
        # fitness information on each individual. Gives you an idea of how much
        # repetition is in standard GE/GP.
        'LOOKUP_FITNESS': False,
        # Uses the cache to look up the fitness of duplicate individuals. CACHE
        #  must be set to True if you want to use this.
        'LOOKUP_BAD_FITNESS': False,
        # Uses the cache to give a bad fitness to duplicate individuals. CACHE
        # must be True if you want to use this (obviously)"""
        'MUTATE_DUPLICATES': False,
        # Removes duplicate individuals from the population by replacing them
        # with mutated versions of the original individual. Hopefully this will
        # encourage diversity in the population.

        # Set machine name (useful for doing multiple runs)
        'MACHINE': machine_name,

        # Set Random Seed for all Random Number Generators to be used by
        # PonyGE2, including the standard Python RNG and the NumPy RNG.
        'RANDOM_SEED': None,

        # Reverse Mapping to GE individual:
        'REVERSE_MAPPING_TARGET': None
}


def load_params(file_name):
    """
    Load in a params text file and set the params dictionary directly.

    :param file_name: The name/location of a parameters file.
    :return: Nothing.
    """

    try:
        open(file_name, "r")
    except FileNotFoundError:
        s = "algorithm.paremeters.load_params\n" \
            "Error: Parameters file not found.\n" \
            "       Ensure file extension is specified, e.g. 'regression.txt'."
        raise Exception(s)

    with open(file_name, 'r') as parameters:
        # Read the whole parameters file.
        content = parameters.readlines()

        for line in content:
            
            # Parameters files are parsed by finding the first instance of a
            # colon.
            split = line.find(":")
            
            # Everything to the left of the colon is the parameter key,
            # everything to the right is the parameter value.
            key, value = line[:split], line[split+1:].strip()
            
            # Evaluate parameters.
            try:
                value = eval(value)
            
            except:
                # We can't evaluate, leave value as a string.
                pass

            # Set parameter
            params[key] = value


def set_params(command_line_args, create_files=True):
    """
    This function parses all command line arguments specified by the user.
    If certain parameters are not set then defaults are used (e.g. random
    seeds, elite size). Sets the correct imports given command line
    arguments. Sets correct grammar file and fitness function. Also
    initialises save folders and tracker lists in utilities.trackers.

    :param command_line_args: Command line arguments specified by the user.
    :return: Nothing.
    """

    from utilities.algorithm.initialise_run import initialise_run_params
    from utilities.algorithm.initialise_run import set_param_imports
    from utilities.fitness.math_functions import return_one_percent
    from representation import grammar
    import utilities.algorithm.command_line_parser as parser
    from utilities.stats import trackers, clean_stats

    cmd_args, unknown = parser.parse_cmd_args(command_line_args)
    
    if unknown:
        # We currently do not parse unknown parameters. Raise error.
        s = "algorithm.parameters.set_params\nError: " \
            "unknown parameters: %s\nYou may wish to check the spelling, " \
            "add code to recognise this parameter, or use " \
            "--extra_parameters" % str(unknown)
        raise Exception(s)

    # LOAD PARAMETERS FILE
    # NOTE that the parameters file overwrites all previously set parameters.
    if 'PARAMETERS' in cmd_args:
        load_params(path.join("..", "parameters", cmd_args['PARAMETERS']))

    # Join original params dictionary with command line specified arguments.
    # NOTE that command line arguments overwrite all previously set parameters.
    params.update(cmd_args)

    if params['LOAD_STATE']:
        # Load run from state.
        from utilities.algorithm.state import load_state

        # Load in state information.
        individuals = load_state(params['LOAD_STATE'])

        # Set correct search loop.
        from algorithm.search_loop import search_loop_from_state
        params['SEARCH_LOOP'] = search_loop_from_state

        # Set population.
        setattr(trackers, "state_individuals", individuals)

    else:
        if params['REPLACEMENT'].split(".")[-1] == "steady_state":
            # Set steady state step and replacement.
            params['STEP'] = "steady_state_step"
            params['GENERATION_SIZE'] = 2
        
        else:
            # Elite size is set to either 1 or 1% of the population size,
            # whichever is bigger if no elite size is previously set.
            if params['ELITE_SIZE'] is None:
                params['ELITE_SIZE'] = return_one_percent(1, params[
                    'POPULATION_SIZE'])
    
            # Set the size of a generation
            params['GENERATION_SIZE'] = params['POPULATION_SIZE'] - \
                                        params['ELITE_SIZE']

        # Set correct param imports for specified function options, including
        # error metrics and fitness functions.
        set_param_imports()

        # Clean the stats dict to remove unused stats.
        clean_stats.clean_stats()

        # Initialise run lists and folders
        initialise_run_params(create_files)

        # Set GENOME_OPERATIONS automatically for faster linear operations.
        if params['CROSSOVER'].representation == "linear" and \
                params['MUTATION'].representation == "linear":
            params['GENOME_OPERATIONS'] = True
        else:
            params['GENOME_OPERATIONS'] = False

        # Parse grammar file and set grammar class.
        params['BNF_GRAMMAR'] = grammar.Grammar(path.join("..", "grammars",
                                                params['GRAMMAR_FILE']))
