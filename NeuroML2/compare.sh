set -e
ncpl -b *v.dat ../NEURON/v.dat &                                                                                                                                                                                
ncpl -b pop1_0.synapses:AMPA_noplast:0_u_bar.dat ../NEURON/u_bar.dat    &                                                                                                                                    
ncpl -b pop1_0.synapses:AMPA_noplast:0_T.dat ../NEURON/T.dat  &                                                                                                                           
ncpl -b pop1_0.synapses:AMPA_noplast:0_N*.dat ../NEURON/N*.dat  &                                                                                                                  
ncpl -b pop1_0.synapses:AMPA_noplast:0_w*.dat ../NEURON/w*.dat  &
