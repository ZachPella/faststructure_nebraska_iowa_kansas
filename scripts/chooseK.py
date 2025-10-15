import numpy as np
import getopt
import glob
import sys
import re

def parse_logs(files):
    """
    parses through log files to extract marginal
    likelihood estimates from executing the
    variational inference algorithm on a dataset.
    Arguments:
        files : list
            list of .log file names
    """
    marginal_likelihood = []
    for file in files:
        handle = open(file,'r')
        for line in handle:
            if 'Marginal Likelihood' in line:
                m = float(line.strip().split('=')[1])
                marginal_likelihood.append(m)
                break
        handle.close()
    return marginal_likelihood

def parse_varQs(files):
    """
    parses through multiple .meanQ files to extract the mean
    admixture proportions estimated by executing the
    variational inference algorithm on a dataset. This is then used
    to identify the number of model components used to explain
    structure in the data, for each .meanQ file.
    Arguments:
        files : list
            list of .meanQ file names
    """
    bestKs = []
    for file in files:
        handle = open(file,'r')
        Q = np.array([map(float,line.strip().split()) for line in handle])
        # Normalize rows to sum to 1 (replacing vars.utils.insum)
        Q = Q / Q.sum(axis=1, keepdims=True)
        handle.close()
        N = Q.shape[0]
        C = np.cumsum(np.sort(Q.sum(0))[::-1])
        bestKs.append(np.sum(C<N-1)+1)
    return bestKs

def parseopts(opts):
    """
    parses the command-line flags and options passed to the script
    """
    for opt, arg in opts:
        if opt in ["--input"]:
            filetag = arg
    return filetag

def usage():
    """
    brief description of various flags and options for this script
    """
    print "\nHere is how you can use this script\n"
    print "Usage: python %s"%sys.argv[0]
    print "\t --input=<file>"

if __name__=="__main__":
    # parse command-line options
    argv = sys.argv[1:]
    smallflags = ""
    bigflags = ["input="]
    try:
        opts, args = getopt.getopt(argv, smallflags, bigflags)
        if not opts:
            usage()
            sys.exit(2)
    except getopt.GetoptError:
        print "Incorrect options passed"
        usage()
        sys.exit(2)

    filetag = parseopts(opts)

    # Find log files with pattern like faststructure_K1.1.log
    log_files = sorted(glob.glob('%s*.log'%filetag))

    if not log_files:
        print "Error: No log files found matching pattern %s*.log" % filetag
        sys.exit(1)

    # Extract K values from filenames like faststructure_K1.1.log -> K=1
    Ks = []
    for file in log_files:
        match = re.search(r'K(\d+)\.\d+\.log', file)
        if match:
            Ks.append(int(match.group(1)))
    Ks = np.array(Ks)

    if len(Ks) == 0:
        print "Error: Could not extract K values from log files"
        sys.exit(1)

    marginal_likelihoods = parse_logs(log_files)

    # Find meanQ files
    meanq_files = sorted(glob.glob('%s*.meanQ'%filetag))

    if not meanq_files:
        print "Error: No meanQ files found matching pattern %s*.meanQ" % filetag
        sys.exit(1)

    bestKs = parse_varQs(meanq_files)

    print "Model complexity that maximizes marginal likelihood = %d"%Ks[np.argmax(marginal_likelihoods)]
    print "Model components used to explain structure in data = %d"%np.argmax(np.bincount(bestKs))
