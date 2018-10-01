from .individual import NPIndividual, TFIndividual

class Parameters():
    """Contains construction parameters for CGP individual."""

    def __init__(self,
                 n_inputs,
                 n_outputs,
                 n_rows,
                 n_columns,
                 function_set,
                 fitness_of_invalid=float('inf'),
                 use_tensors=False,
                 max_back=None):
        """Creates Parameters object.


        Args:
            n_inputs (int): Number of input nodes (i.e. attributes)
            n_outputs (int): Number of output nodes
            n_rows (int): Number of rows
            n_columns (int): Number of columns
            function_set (FunctionSet): instance of FunctionSet class
            fitness_of_invalid (number): penalty fitness assigned to individual producing error
            use_tensors (bool): if true, CGP works with tensors instead of numpy arrays
            max_back (bool): number of previous nodes (including inputs) to which node can connect. When set to None, not limit is imposed.
            use_tensorflow (bool): not used

        Returns:
            Parameters class instance.
        """

        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_nodes = n_rows * n_columns
        self.n_columns = n_columns
        self.n_rows = n_rows
        self.function_set = function_set
        self.fitness_of_invalid = fitness_of_invalid
        self.use_tensors = True
        self.individual_class = NPIndividual
        # self.individual_class = TFIndividual there is probably no reason for that

        if max_back is None:
            self.max_back = self.n_nodes + self.n_inputs + self.n_outputs
        else:
            self.max_back = max_back

class FunctionSet():
    """Class containing functions which CGP system can use."""

    def __init__(self):
        """Initialize empty function set."""
        self.functions = []
        self.max_arity = 0

    def add(self, function, arity):
        """Add given function to function set.

        Args:
            function (callable): function to add (must have a workings __name__)
            arity (int): arity (number of arguments) of given function
        """
        self.functions.append((function, arity))
        self.max_arity = max(self.functions, key=lambda x: x[1])[1]

    def __getitem__(self, index):
        """Returns a function at given index."""
        return self.functions[index]

    def __len__(self):
        """Returns a number of functions in function set."""
        return len(self.functions)

