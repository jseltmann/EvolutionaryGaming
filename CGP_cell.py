import function_set
import numpy as np


class CGP_cell:
    """
    Class representing a cell in a cartesian genetic program.

    Attributes
    ----------
    inputs : (int, int)
        Positions of the cells from which this cell takes its inputs.
    parameter : float
        Extra parameter used by some functions from the function set.
    function : function
        Function from function set used to calculate the output value.
    program : CGP_Program
        CGP program of which the cell is a part.
    active : boolean
        Marks cell as active.
    last_value : float or numpy.ndarray
        Value obtained in last function evaluation.
        Initialized as 0.
    is_output_cell : bool
        says if the current cell is an output cell or not

    Parameters
    ----------
    genome : [float]
        List of four floating point values between 0 and 1 representing the genome of the cell.
    program : CGP_Program
        CGP program of which the cell is a part.
    """

    def __init__(self, genome, program):
        # get inputs
        inp1 = round(genome[0] * (program.num_cells-1))
        inp2 = round(genome[1] * (program.num_cells-1))
        self.inputs = (inp1, inp2)

        # get function
        num_functions = len(function_set.functions)
        func_pos = round(genome[2] * (num_functions - 1))
        func_name = function_set.functions[func_pos]
        self.function = getattr(function_set, func_name)

        # parameter should be scaled to [-1, 1]
        self.parameter = 2 * genome[3] - 1

        self.program = program

        self.last_value = 0

        self.active = False

    def evaluate(self):
        """
        Evaluates the function of the cell using the inputs and the parameter.
        """

        inp1 = self.program.get_cell(self.inputs[0]).last_value
        inp2 = self.program.get_cell(self.inputs[1]).last_value

        self.last_value = np.nan_to_num(
            self.function(inp1, inp2, self.parameter))


class Output_cell(CGP_cell):
    """
    Class representing an output cell

    Attributes
    ----------
    inputs : (int, int)
        Positions of the cells from which this cell takes its inputs.
    parameter : float
        Extra parameter used by some functions from the function set.
    function : function
        Function from function set used to calculate the output value.
    program : CGP_Program
        CGP program of which the cell is a part.
    active : boolean
        Marks cell as active.
    last_value : float or numpy.ndarray
        Value obtained in last function evaluation.
        Initialized as 0.

    Parameters
    ----------
    genome : [float]
        List of four floating point values between 0 and 1 representing the genome of the cell.
    program : CGP_Program
        CGP program of which the cell is a part.
    """

    def evaluate(self):
        """
        Evaluates the function of the cell using the inputs and the parameter.
        """

        inp1 = self.program.get_cell(self.inputs[0]).last_value
        inp2 = self.program.get_cell(self.inputs[1]).last_value

        input_values = [inp1, inp2]

        # convert each input to list if isn't one already
        for i, fo in enumerate(input_values):
            if not isinstance(fo, list):
                input_values[i] = [fo]

        # get the average value of the lists, this will be the final value of the inputs
        input_values = [np.average(ip) for ip in input_values]

        self.last_value = sum(input_values)
