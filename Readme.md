# HRE4D: Hard Rock E4D
HRE4D is a fork of [E4D by PNNL](https://github.com/pnnl/E4D) made specifically for geophyscists dealing with hard-rock geology, rather than hydrogeology. Certain terminology and conventions are hence different. As a brief example, instead of conductivity we output resistivity, and we accept observed phase input as positive rather than negative. This program may be at any stage of completion.

There are also a few additional goals:
 * Making use of the program as streamlined as possible
 * Adding OpenMP support per node (to work in conjunction with MPI across nodes)
 * Increasing the speedup due to paralelism by moving away from the Master/Minion paradigm
 * Increasing the numerical stability of algorithms used within, such as the current Gauss-Newton and conjugate gradient methods, which can exhibit strange behavior for very large datasets on small machines/clusters.

