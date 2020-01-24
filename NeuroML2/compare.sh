set -e
ncpl -b *v.dat ../NEURON/v.dat &                                                                                                                                                                                
ncpl -b pop1_0.synapses:*:0_u_bar.dat ../NEURON/u_bar.dat    &                                                                                                                                                 
ncpl -b pop1_0.synapses:*:0_g.dat ../NEURON/g.dat    &                                                                                                                                    
ncpl -b pop1_0.synapses:*:0_T.dat ../NEURON/T.dat  &                                                                                                                           
ncpl -b pop1_0.synapses:*:0_N*.dat ../NEURON/N*.dat  &                                                                                                                  
ncpl -b pop1_0.synapses:*:0_w*.dat ../NEURON/w*.dat  &                                                                                                           
ncpl -b pop1_0.synapses:*:0_G*.dat ../NEURON/G.dat  pop1_0.synapses:*:0_P*.dat ../NEURON/P.dat &                                                                                                       
ncpl -b pop1_0.synapses:*:0_C*.dat ../NEURON/C.dat  &
