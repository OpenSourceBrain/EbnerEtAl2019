# Based on https://www.neuron.yale.edu/phpBB/viewtopic.php?f=2&t=2750

from neuron import *
import numpy as np
import sys
import matplotlib.pyplot as plt

duration = 500
dt = 0.01

def get_random_stim(rate):
    
    stimNc = h.NetStim()
    stimNc.noise = 1      
    stimNc.start = 0     
    stimNc.number = 1e9
    stimNc.interval = 1000./rate
    return stimNc

def get_timed_stim():
    
    stimNc = h.NetStim()
    stimNc.noise = 0    
    stimNc.start = 100 
    stimNc.number = 3
    stimNc.interval = 20
    return stimNc

soma = h.Section()
soma.L =17.841242
soma.diam=17.841242
soma.push() 
soma.insert("pas")
soma.g_pas = 0.0003
syn = h.ExpSyn (0.5, sec = soma)  

stim = h.IClamp(0.5, sec = soma)
stim.delay = 200.0
stim.dur = 5.0
stim.amp = 0.4

def get_base_syn():
    syn = h.Syn4P (0.5, sec = soma)
    syn.A_LTD_pre = 0
    syn.A_LTP_pre = 0
    syn.A_LTD_post = 0
    syn.A_LTP_post = 0
    
    return syn



def get_ampa_syn():
    syn = get_base_syn()
    syn.s_ampa = 1
    syn.s_nmda = 0
    return syn

def get_nmda_syn():
    syn = get_base_syn()
    syn.s_ampa = 0
    syn.s_nmda = 1
    return syn

syn = get_base_syn()
syn = get_ampa_syn()
#syn = get_nmda_syn()

def run_sim(rate=10):

    print('Running simulation of %s with %s Hz input'%(duration, rate))

    stimNc = get_random_stim(rate)
    stimNc = get_timed_stim()
    
    vec_nc = h.Vector()

    nc = h.NetCon(stimNc, syn)
    nc.weight[0] = 0.001
    nc.delay = 0

    nc.record(vec_nc)

    vec = {}
    states = ['G', 'Z', 'E','C','P','X']
    states = ['u_bar', 'E','T', 'flag_D']
    #A_vals = ['A_LTD_pre', 'A_LTP_pre', 'A_LTD_post', 'A_LTP_post']
    
    for var in ['v','t','g','g_ampa','g_nmda','w_pre','w_post', 'w'] + states:
        vec[var] = h.Vector()
        if var!='v' and var!='t':
            exec("print('Recording:  %s')"%var)
            exec("vec ['%s'].record(syn._ref_%s)"%(var,var))

    # record the membrane potentials and
    # synaptic currents
    vec['v'].record(soma(0.5)._ref_v)
    vec ['t'].record(h._ref_t)

    # run the simulation
    h.load_file("stdrun.hoc")
    h.init()
    h.tstop = duration
    h.dt = dt
    h.run()

    spikes = []
    isis = []
    lastSpike =None
    for t in vec_nc:
        spikes.append(t)
        #print(t)
        if lastSpike:
            isis.append(t-lastSpike)
        lastSpike = t

    hz = 1000/(h.tstop/len(spikes))
    print("Spike times: %s"%['%.3f'%t for t in vec_nc])
    print("Num spikes: %s; avg rate: %s Hz; avg isi: %s ms; std isi: %s ms"%(len(spikes),hz,np.average(isis),np.std(isis)))
    #assert abs((hz-rate)/rate)<0.01

    scales = {'v':0.001, 'g':1e-6, 'u_bar':1}
    for var in scales:
        var_file = open('%s.dat'%var, 'w')
        for i in range(len(vec['t'])):
            var_file.write('%s\t%s\n'%(vec['t'][i]/1000,vec[var][i]*scales[var]))
        var_file.close()


    if not '-nogui' in sys.argv:
        # plot the results
        plt.figure()
        plt.title('Membrane potential')
        plt.plot(vec['t'],vec['v'])
        
        plt.figure()
        plt.title('Conductance')
        plt.plot(vec['t'],vec['g'],label='g')
        plt.plot(vec['t'],vec['g_ampa'],label='g_ampa')
        plt.plot(vec['t'],vec['g_nmda'],label='g_nmda')
        plt.legend()
        
        plt.figure()
        plt.title('Weights')
        plt.plot(vec['t'],vec['w'],label='w')
        plt.plot(vec['t'],vec['w_pre'],label='w_pre')
        plt.plot(vec['t'],vec['w_post'],label='w_post')
        plt.legend()
        
        plt.figure()
        plt.title('States')
        for s in states: 
            plt.plot(vec['t'],vec[s],label=s)
        plt.legend()
        
run_sim()

if not '-nogui' in sys.argv:
    plt.show()

