# Tests
Every tests should check the following:

- Number of variables
- Number of constraints
- Objective sense
- The solution for some simple instances
- Different seeds should create different instances

# Generators

### Generating MIPS
There should be (at least) two functions that are used to generate a specific MIP. 
One which takes problem specific parameters as input and returns the MIP.
One which takes generator specific arguments as input and returns problem the specific parameters.  
 