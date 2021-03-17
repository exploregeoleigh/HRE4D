This script will generate plots from a .dpd file output form e4d (ensure the option is turned on in the E4D output file before running your inversion).

It takes input from at least 1 command line argument:
 > ./D_pred_vs_D_Obs [filename] [show_plts]
 filename is the filename of the .dpd file
 show_plts is an optional integer deafulting to 0. 0 does not display the plots, 1 does. Both write to an aptly named file.
 
 The input file is structured in the following way:
 
 
 n           # a line indicating the number of measurements
 1 a1 b1 m1 n1 V_obs1 V_pred1 Phase_obs1 Phase_pred1    # The following lines have an indx, the indexes of the current and potential
 2 a2 b2 m2 n2 V_obs2 V_pred2 Phase_obs2 Phase_pred2    # electrodes, then the obsereved and predicted values for voltage and phase
 ...
 n an bn mn nn V_obsn V_predn Phase_obsn Phase_predn
 
 
 The script will automatically cull voltage ratio data points that are negative and phase pred points that are positive.

