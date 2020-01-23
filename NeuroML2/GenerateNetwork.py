from neuromllite import Network, Cell, InputSource, Population, Synapse, RectangularRegion, RandomLayout 
from neuromllite import Projection, RandomConnectivity, Input, Simulation
import sys

################################################################################
###   Build new network

net = Network(id='Syn4Net')
net.notes = 'Syn4Net: synaptic properties'
net.parameters = { 'weight': 0.001,
                   'stim1_delay':      50,
                   'stim2_delay':      200}


cell = Cell(id='passiveCell', neuroml2_source_file='passiveCell.cell.nml')
net.cells.append(cell)

spkArr1 = Cell(id='spkArr1', neuroml2_source_file='inputs.nml')
net.cells.append(spkArr1)


stim1 = InputSource(id='stim1', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':0.4, 'start':'stim1_delay', 'stop':'stim1_delay+5'})
net.input_sources.append(stim1)

stim2 = InputSource(id='stim2', 
                           pynn_input='DCSource', 
                           parameters={'amplitude':0.4, 'start':'stim2_delay', 'stop':'stim2_delay+5'})
net.input_sources.append(stim2)

r1 = RectangularRegion(id='region1', x=0,y=0,z=0,width=1000,height=100,depth=1000)
net.regions.append(r1)

p0 = Population(id='pop0', size=1, component=spkArr1.id, properties={'color':'1 0 0', 'radius':10},random_layout = RandomLayout(region=r1.id))
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

net.inputs.append(Input(id='i_stim1',
                        input_source=stim1.id,
                        population=p1.id,
                        percentage=100))
net.inputs.append(Input(id='i_stim2',
                        input_source=stim2.id,
                        population=p1.id,
                        percentage=100))

print(net.to_json())
new_file = net.to_json_file('%s.json'%net.id)


################################################################################
###   Build Simulation object & save as JSON

sim = Simulation(id='Sim%s'%net.id,
                 network=new_file,
                 duration='500',
                 dt='0.01',
                 recordTraces={'pop1':'*'},
                 recordVariables={'synapses:%s:0/g'%syn.id:{'pop1':'*'},
                                  'synapses:%s:0/u_bar'%syn.id:{'pop1':'*'},
                                  'synapses:%s:0/T'%syn.id:{'pop1':'*'}},
                 recordSpikes={'pop0':'*'})
                 
sim.to_json_file()



################################################################################
###   Run in some simulators

from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

check_to_generate_or_run(sys.argv, sim)

