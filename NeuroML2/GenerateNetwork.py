from neuromllite import Network, Cell, InputSource, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id='Syn4Net')
net.notes = 'Syn4Net: synaptic properties'
net.parameters = { 'input_amp':   0.23,
                   'weight':      0.001}
                   #'tau_syn':     2} 

cell = Cell(id='passiveCell', neuroml2_source_file='passiveCell.cell.nml')
net.cells.append(cell)

spkArr1 = Cell(id='spkArr1', neuroml2_source_file='inputs.nml')
net.cells.append(spkArr1)


input_source = InputSource(id='i_clamp', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':'input_amp', 'start':200., 'stop':800.})
net.input_sources.append(input_source)

input_source1 = InputSource(id='i_clamp1', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':0.4, 'start':200., 'stop':205.})
net.input_sources.append(input_source1)

r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)

p0 = Population(id='pop0', size=1, component=spkArr1.id, properties={'color':'1 0 0'},random_layout = RandomLayout(region=r1.id))
p1 = Population(id='pop1', size=1, component=cell.id, properties={'color':'0 1 0'},random_layout = RandomLayout(region=r1.id))

net.populations.append(p0)
net.populations.append(p1)

syn = Synapse(id='AMPA_noplast', neuroml2_source_file='fourPathwaySyn.synapse.nml')
net.synapses.append(syn)
                      

net.projections.append(Projection(id='proj0',
                                  presynaptic=p0.id, 
                                  postsynaptic=p1.id,
                                  synapse=syn.id,
                                  delay=0,
                                  weight='weight'))
net.projections[0].random_connectivity=RandomConnectivity(probability=1)


'''
net.inputs.append(Input(id='stim',
                        input_source=input_source.id,
                        population=p0.id,
                        percentage=100))'''

net.inputs.append(Input(id='stim1',
                        input_source=input_source1.id,
                        population=p1.id,
                        percentage=100))

print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='Sim%s'%net.id,
                 network=new_file,
                 duration='500',
                 dt='0.025',
                 recordTraces={'pop1':'*'},
                 recordVariables={'synapses:%s:0/g'%syn.id:{'pop1':'*'}},
                 recordSpikes={'pop0':'*'})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)

