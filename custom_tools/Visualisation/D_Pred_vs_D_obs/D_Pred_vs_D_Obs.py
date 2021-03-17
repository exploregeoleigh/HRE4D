#!/usr/bin/env python
# coding: utf-8

# ## Data Pred vs D_Obs plotter.
# A quick script to generate a plot of data observered vs data predicted a given survey.
# Reads in a data predicted and survey file, otuputs plots

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib 
import sys

if(len(sys.argv)<2):
    print("ERROR! Not enough arguments. Please use [filename] [optional, 0 to not show plots, 1 to show] as command line arguments")
    quit()
filename_dpd=sys.argv[1]
if(len(sys.argv)>2):
    show_plts=int(sys.argv[2])
else:
    show_plts=0

# Functions used

# In[71]:




#Misc file processing
file_dpd=open(filename_dpd)

text_dpd=file_dpd.readlines()


# In[72]:


def readint(textline,num2read):
    """
    Read an element from a line of text of format ' a b c d' in the num2read'th position
    returns it as an int
    """
    nums=0
    prev_char=' '
    zone=''
    for char in textline:
        if prev_char==' ' and char != ' ':
            nums+=1
        prev_char=char
        if nums==num2read and (char!=' ' ):
            zone=zone+char #concatenate
    return int(zone)

def readreal(textline,num2read):
    """
    Read an element from a line of text of format ' a b c d' in the num2read'th position
    returns it as a real
    """
    nums=0
    prev_char=' '
    zone=''
    for char in textline:
        if prev_char==' ' and char != ' ':
            nums+=1
        prev_char=char
        if nums==num2read and (char!=' '):
            zone=zone+char #concatenate
    return float(zone)


# In[73]:


def data_type(str_in):
    """
    Returns what the data type of the input looks like
    Input:
       str_in (string) - string to be read
    Output:
       d_type (int) - 0 for int, 1 for float, 2 for str
    """
    str_in=str_in.strip() # Equivalent to trim in fortran
    # E4D does not take in comment lines, so we dont need to check for them
    # If the string is a pure number with no periods, return it
    n_periods=0
    if(str_in.isnumeric() ):
        return 0
    for char in str_in:
        if ((not char.isnumeric) and (char!='.') ):
            d_type=2
            return 2
        if(char=='.'):
            n_periods+=1
    if(n_periods==1):
        return 1
    else:
        return 2

        
def read_dpd(text_in):
    """
    Reads in a survey file (electrodes first, then measurments). 
    Fortran should skip the blank lines with read, so if translating 
    this code to fortran you may just be able to use for loops.
    Input: 
        text_in (string) - survey file text as  file.readlines (list of strings)
    Output: 
        d_obs
        d_pred (numpy array size: N_obs x 2) - measurement data from the file
    """
    iline=0
    # read number of measurements
    nm=-1
    while nm==-1:
        line=text_in[iline][:-1]
        iline+=1
        if(line.strip()==''):
            continue # Fortran cycle
        else:
            nm=readint(line,1)
            
    # Create data objects
    d_obs=np.zeros((nm,2)) # Create a numpy array filled with zeros
    d_pred=np.zeros((nm,2)) 
    
    #Read in next lines
    nm_read=0
    while nm_read<nm:
        line=text_in[iline][:-1].strip()
        iline+=1
        if(line==''):
            continue # Fortran cycle
        else:
            d_obs[nm_read,0]=readreal(line,6)
            d_pred[nm_read,0]=readreal(line,7)
            d_obs[nm_read,1]=readreal(line,8)
            d_pred[nm_read,1]=readreal(line,9)
            nm_read+=1
    return d_obs, d_pred
        
    
        
        
        
        
            


# In[247]:


def plot_pred_v_obs(pred1,obs1,dtype, fname):
    """
    Plots the pred vs obs. Saves plot to a file.
    Assumes input for phase is positive and in mRad
    Input: 
        pred1 (numpy array of size (nm)) - predicted data
        obs1 (numpy array of size (nm)) - observered data
        dtype (int) - type of data, 0 for Conductivity, 1 for phase
        fname (str) - local filename to save plot to
    Output:
        none
    """
    n_obs_neg=np.sum(obs1<0)
    n_pred_neg=np.sum(pred1<0)
    t_data_culled=np.size(pred1)-np.sum((pred1>0)*(obs1>0))
    pred=pred1[(pred1>0)*(obs1>0)]
    obs=obs1[(pred1>0)*(obs1>0)]
                          
    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    o_min=np.min(obs)
    o_max=np.max(obs)
    p_min=np.min(pred)
    p_max=np.max(pred)
    d_min=min(o_min,p_min)
    d_max=max(o_max,p_max)
    d_dif=d_max-d_min
    o_dif=o_max-o_min
    x=np.linspace(o_min-o_dif/20,o_max+o_dif/20,2)
    m, c = np.polyfit(obs, pred,1)
    y1=m*x+c
    y2=x
    if(dtype==0):
        ax.plot(x,y2, 'g--')
        ax.plot(x,y1, 'r-')
        ax.loglog(obs,pred,'bo')    
        ax.set_title("Predicted vs Observed for Voltage Ratio (Ohms)")
        ax.set_xlim(d_min/4,d_max*4)    
        if(t_data_culled>0):
            ax.text(d_min/2, d_max/2, str(t_data_culled)+ ' data points culled.'
                    +str(n_obs_neg)+' obs culled and '+str(n_pred_neg)+' pred culled',
                    bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    elif(dtype==1):
        ax.plot(x,y2, 'g--')
        ax.plot(x,y1, 'r-')
        ax.plot(obs,pred,'bo')
        ax.set_title("Predicted vs Observed for Apparent Phase (mRad)")
        ax.set_xlim(d_min-d_dif/10,d_max+d_dif/10) 
        if(t_data_culled>0):
            ax.text(d_min, d_max-d_dif/10, str(t_data_culled)+ ' data points culled. '
                    +str(n_obs_neg)+' obs culled and '+str(n_pred_neg)+' pred culled',
                    bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    ax.set_ylabel('Predicted value')
    ax.set_xlabel('Observed value')
    ax.set_aspect(aspect=1,adjustable='box')
    ax.grid(which='both')
    ax.legend(["d_obs = d_pred", "Data fit"])
    #ax.text(d_min,1, 'boxed italics text in data coords', style='italic',
    # bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    plt.savefig(fname, format='jpg')


# Actually read the data

# In[178]:


d_obs, d_pred = read_dpd(text_dpd)
d_obs[:,1]=-d_obs[:,1]*1000
d_pred[:,1]=-d_pred[:,1]*1000


# Produce some plots

# In[228]:


filename_dpd[:-4]


# In[248]:


plot_pred_v_obs(d_pred[:,0],d_obs[:,0], 0,'Plot_of_'+filename_dpd[:-4]+'_V_Ratio.jpg')
if show_plts==1:
    plt.show()


# In[249]:


plot_pred_v_obs(d_pred[:,1],d_obs[:,1],1,'Plot_of_'+filename_dpd[:-4]+'_Phase.jpg')
if show_plts==1:
    plt.show()
