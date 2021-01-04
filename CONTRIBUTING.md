# Contribution Guide
To contribute: fork this repo, clone the forked repo make the changes in a branch then create a pull request to this repo. 

## Development Environment
Install dependencies and activate conda development environment
```bash
conda env create -n GeCO --file conda-dev-env.yml
```
Then activate the created conda environment.
```bash
conda activate GeCO
```

## Adding a Generator
1. First, look through the list of generator types already implemented in the readme, and add your code to the corresponding module/package if the same type 
is implemented, if not create a new module.
2. Your module should ideally contain two public functions:
    * one that generates the parameters required for the instance with the signature `FIRSTAUTHOR_params`. 
    * another one that takes these params as an input and returns an instance with the signature `FIRSTAUTHOR_instance`.
3. Your code should be documented, prefereably following NumPy's [standards](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard).

## Creating an Issue
Adding an issue is still a contribution! if you find something wrong or that can be added and you don't have the time to do it 
create an issue and we will try our best to solve it. 
