from roundabout.utils import test_plot
from roundabout.utils import test_ani, delta_plot
from roundabout.env import Env
import numpy as np
from roundabout.utils import test_ani
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 18})
np.seterr(all='raise')


envParams = {
    "a": 3, 
    "v": 8,
    "C": 3,
    "veh_length": 5,
    "headway": 3,
    "Q": None,
    "step_size": 0.05,
    "boundary": 250,
    "eta": np.array([[0.0, 0.0, 5/7, 2/7],
                     [2/7, 0.0, 0.0, 5/7],
                     [5/7, 2/7, 0.0, 0.0],
                     [0.0, 5/7, 2/7, 0.0]]),
    "fifo": True
}

# Put together the initial Q (incoming flow). This will be a time-based function. To approximate this behavior, at each
# time step, we use a uniform distribution to get a baseline value and then add randomized noise based on a normal
# distribution. We use this as the mean to a Poisson distribution to get the Qi's. This way, our lambda isn't static.
baselines = np.random.uniform(25, 41, 4)
incomingFlows = np.array([0.0, 0.0, 0.0, 0.0])
for x in range(len(baselines)):
    baselines[x] += np.random.normal(0, 3)

    # The flow should be first divided by 60 to get incoming flow per minute and then multiplied by the step_size to get
    # an approximate incoming number of vehicles this time step
    incomingFlows[x] = np.random.poisson(baselines[x]) / 60 * envParams['step_size']

# Set the envParams.Q equal to this array of incoming flows
envParams['Q'] = incomingFlows

initParams = {
    "l_0": np.array([0, 0, 0, 0]),  
    #"l_0": np.array([14, 15, 13, 14]),  
}

env = Env(envParams)
env.initialize(initParams)

test_ani(env, 2400, "compare-68")
env.save_records("compare_records-68")