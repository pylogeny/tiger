# Compute TIGER Rates for Phylogenetic Data

This is a pure Python implementation of the TIGER rates ([Cummins and McInerney 2011](https://doi.org/10.1093/sysbio/syr064)), which can be computed for all kinds of phylogenetic data. The creation of the package was inspired by a study of [Syrjänenen et al. (2021)](https://doi.org/10.1093/jole/lzab004) in which the authors present a new implementation of TIGER rate computation for linguistic purposes. Since the implementation by Syrjänen et al. does not come along as a package, but rather as a commandline tool, whose application from within Python scripts is not straightforward, I decided to reimplement the rate computation based on the description in both publications in the form of a small Python package without further dependencies.  

