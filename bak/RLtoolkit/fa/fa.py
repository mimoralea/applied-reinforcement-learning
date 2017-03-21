### This file contains the base definitions for function approximators.


### Generic FA functions:
### 
###    functionapproximator.faApproximate (input)               # changes nothing
###    functionapproximator.faLearn (input, target)              # makes all changes
###    functionapproximator.faLearnLastApproximation (input, output, target)
###
### The last function is a computationally cheap version of learn which can be used
### if input and output are the input and output from the last call to faApproximate
### with this function approximator.
###
### All arguments are 1D ARRAYS, except that target may optionally be a scalar, and that
### input is also allowed to be a list of indices of active input lines (these 
### indices run from 0 to the dimensionality of the input).  The dimensionality of
### the input is called numinputs and the dimensionality of the output is called
### numoutputs
###
### The function (fainit functionapproximator) can be used to reinitialize the 
### data structures of a function approximator without reallocating memory for them.

### Mix in  CHECKINPUTRANGE and CHECKINPUTDIMENSIONALITY to get your inputs 
### checked automatically.

class CheckInputDimensionality:

    def __init__(self, numinputs=1):
        self.numinputs = numinputs

    def faApproximate(self, input):
        if self.numinputs != len(input):
            print("Input", str(input), "does not match dimentionality", fa.numinputs)
        return 0

    def faLearnLastApproximation(self, input, output, target):
        if self.numinputs != len(input):
            print("Input", str(input), "does not match dimentionality", fa.numinputs)


class FunctionApproximator (CheckInputDimensionality):
    "Foundation of all function approximators"

    def __init__(self, numinputs=1, numoutputs=1):
        self.numinputs = numinputs
        self.numoutputs = numoutputs
        self.learningrate = 1.0

    def faLearn(self, input, target):
        """The default faLearn just approximates and learns the approximation.
           Surprisingly, this suffices for almost all function approximators."""
        output = self.faApproximate(input)
        self.faLearnLastApproximation(input, output, target)

    def faApproximate(self, input):
        "The default"
        return CheckInputDimensionality.faApproximate(self, input)

    def faLearnLastApproximation(self, input, output, target):
        "The default"
        CheckInputDimensionality.faLearnLastApproximation(input, output, target)

    def normalizedlearningrate(self, input):
        "Default for a functionapproximator just returns its learningrate slot's value"
        return self.learningrate



