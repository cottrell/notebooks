# neural autoregressive flows

https://github.com/CW-Huang/NAF.git

paste these into chrome to restart:

https://github.com/CW-Huang/NAF
https://github.com/CW-Huang/naf_examples
https://github.com/gpapamak/maf
https://arxiv.org/pdf/1804.00779.pdf#page=10


You want to be looking at the IAF-DSF (deep) and IAF-DDSF (deep dense) sigmoidal flows stuff.

What is confusing is that it looks like these are using something called cMADE in the code ... but I think that is just the part mentioned in the paper about computing the autoregressive conditioner "c" via a single forward pass of a MADE model.
