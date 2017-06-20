from os import getcwd, listdir, path
import sys
sys.path.append("../src")

from utilities.algorithm.general import check_python_version

check_python_version()

from scripts import GE_LR_parser
from ponyge import mane
from algorithm.parameters import params, set_params
from representation.individual import Individual


def load_population(target):
    """
    Given a target folder, read all files in the folder and load/parse
    solutions found in each file.
    
    :param target: A target folder stored in the "seeds" folder.
    :return: A list of all parsed individuals stored in the target folder.
    """

    # Set path for seeds folder
    path_1 = path.join(getcwd(), "..", "seeds")

    if not path.isdir(path_1):
        # Seeds folder does not exist.
    
        s = "scripts.seed_PonyGE2.load_population\n" \
            "Error: `seeds` folder does not exist in root directory."
        raise Exception(s)
    
    path_2 = path.join(path_1, target)

    if not path.isdir(path_2):
        # Target folder does not exist.
    
        s = "scripts.seed_PonyGE2.load_population\n" \
            "Error: target folder " + target + \
            " does not exist in seeds directory."
        raise Exception(s)
    
    # Get list of all target individuals in the target folder.
    target_inds = [i for i in listdir(path_2) if i.endswith(".txt")]
       
    # Initialize empty list for seed individuals.
    seed_inds = []

    for ind in target_inds:
        # Loop over all target individuals.

        # Get full file path.
        file_name = path.join(path_2, ind)

        # Initialise None data for ind info.
        genotype, phenotype = None, None

        # Open file.
        with open(file_name, "r") as f:
            
            # Read file.
            raw_content = f.read()
            
            # Read file.
            content = raw_content.split("\n")
            
            # Check if genotype is already saved in file.
            if "Genotype:" in content:
                
                # Get index location of genotype.
                gen_idx = content.index("Genotype:") + 1
                
                # Get the genotype.
                try:
                    genotype = eval(content[gen_idx])
                except:
                    s = "scripts.seed_PonyGE2.load_population\n" \
                        "Error: Genotype from file " + file_name + \
                        " not recognized: " + content[gen_idx]
                    raise Exception(s)
            
            # Check if phenotype (target string) is already saved in file.
            if "Phenotype:" in content:
    
                # Get index location of genotype.
                phen_idx = content.index("Phenotype:") + 1
    
                # Get the phenotype.
                phenotype = content[phen_idx]
                
                # TODO: Current phenotype is read in as single-line only. Split is performed on "\n", meaning phenotypes that span multiple lines will not be parsed correctly. This must be fixed in later editions.
            
            elif "Genotype:" not in content:
                # There is no explicit genotype or phenotype in the target
                # file, read in entire file as phenotype.
                phenotype = raw_content

        if genotype:
            # Generate individual from genome.
            ind = Individual(genotype, None)
            
            if phenotype and ind.phenotype != phenotype:
                s = "scripts.seed_PonyGE2.load_population\n" \
                    "Error: Specified genotype from file " + file_name + \
                    " doesn't map to same phenotype. Check the specified " \
                    "grammar to ensure all is correct: " + \
                    params['GRAMMAR_FILE']
                raise Exception(s)
        
        else:
            # Set target for GE LR Parser.
            params['REVERSE_MAPPING_TARGET'] = phenotype
            
            # Parse target phenotype.
            ind = GE_LR_parser.main()
            
        # Add new ind to the list of seed individuals.
        seed_inds.append(ind)

    return seed_inds


if __name__ == '__main__':
    # Set parameters
    set_params(sys.argv[1:])
    
    if params['TARGET_SEED_FOLDER']:
        # A target folder containing seed individuals has been given.
        params['SEED_INDIVIDUALS'] = load_population(
            params['TARGET_SEED_FOLDER'])
    
    elif params['REVERSE_MAPPING_TARGET']:
        # A single seed phenotype has been given. Parse and run.
        
        # Parse seed individual and store in params.
        params['SEED_INDIVIDUALS'] = [GE_LR_parser.main()]
        
    # Launch PonyGE2.
    mane()
