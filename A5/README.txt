README.txt

This is Version 5 (released Feb. 18, 2018) of the starter code
for Assignment 5 in CSE 415, University of Washington, Winter 2018.

This is intended to be the final version, except for possible bug
fix releases or minor enhancements. The feature set here can be considered
complete for purposes of Assignment 5.

Written by S. Tanimoto, with feedback from R. Thompson.

To start the GUI, type the following, in the same folder
as the code.

python3 TOH_MDP.py

All files here except YourUWNetID_VI.py are different from those in
the first release.

TOH_MDP.py and Vis_TOH_MDP.py have been updated in this version since
the previous version (version 2 on Feb. 14).

The sample script has also been updated to suggest how to automate
setup for doing Q-Learning experiments.

Main changes from the previous release:
  You can only show a policy when it is safe (a policy can be extracted),
assuming your extract_policy methods work.

  Policy display is persistent with automatic updating whenever Q values
change.

  Independent policies are stored and displayed... one for VI and one for
QL.  This also means you can view both at the same time, in different
colors.

  Misc. improvements, related to the manual user driving, etc.

