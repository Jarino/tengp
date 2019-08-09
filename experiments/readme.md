# Experiments

Collection of scripts for executing the experiments and evaluating the results.

## Scripts

`baseline.py` runs the baseline experiment of CGP with single mutation. Example usage (from root of project)
```
python -m experiments.baseline nguyen7 -d train -t 10 -o baseline.logs
```



## Notes

**Idea:** use nodes with fixed function. Create a graph, which will have all functions from function set in a column, with one additional identity node.
This way, the mapping is much simpler, since we do not have to do a linear combination of the two functions, just linear combination for each input.

_Possible issue:_ one needs to arrange fixed functions in such way, that the space contains all combinations, that would be possible without fixed. This might not even be entirely possible, without introduction ridiculously large phenotypes. Although, one can effectively tackle this in case of one row CGP, which is frequently used - number of columns will be equal to number of functions + identity function.

**Idea (greedy approach):** all connections could be set to identity. Also max_back parameter will be set to one, so only connections to previous column are possible. Then, one can start greedy optimization from leftmost column, to rightmost column. First, find best solution only using first column (without changing the genotype tied with the other columns). When convergence for that column is reached, fix the genes representing that column and move to the next. Optimize connections to the second column and repeat, until all columns are reached, or until pure identity is chosen as an optimal solution.

_Possible benefits:_ This could really speed up the convergence for easy functions.

_Possible issue:_ Large chance of stucking in local optima due to greedy approach. Specialy in decieving functions, it can even choose a term, which is not in the function at all.

**Issue with using local optimization:** CGP exhibits large dependency on order of genes. The gene which 
