import numpy as np
# READ THIS: GO TO ____GRAPHICS____ SECTION
# BELOW ON INSTRUCTIONS TO GENERATE YOUR OWN
# SOLAR SYSTEM

# define planet datatype
class Planet:
    def __init__(self, index : int, mass : float, state : np.ndarray):
        self.index = index
        self.mass = mass
        self.state = np.asanyarray(state)
    
    def update_state(self, new_state):
        self.state = np.asanyarray(new_state)
    
    @property
    def r(self):
        return self.state[0] # First row is position

    @property
    def v(self):
        return self.state[1] # Second row is velocity


#____INTEGRATION____#
def state_matrix(system : list[Planet]) -> np.ndarray:
    #produces position/velocity matrix from planet list
    return np.stack([p.state for p in system])

def mass_list(system : list[Planet]) -> np.ndarray:
    #produces a list of planet masses from the system list
    return np.array([p.mass for p in system])

def acc_matrix(positions : np.ndarray, masses : np.ndarray) -> np.ndarray:
    #takes in a matrix of position vectors and outputs a matrix of acceleration vectors
    # 1. Get relative displacement vectors (N, N, 2)
    # This is the "broadcasting" trick: (1, N, 2) - (N, 1, 2)
    diff = positions[np.newaxis, :, :] - positions[:, np.newaxis, :]
    
    # 2. Distances squared (N, N)
    r2 = np.sum(diff**2, axis=-1)
    
    # 3. Softening to avoid 1/0 
    eps = 1e-2
    inv_r3 = (r2 + eps)**(-1.5)
    
    # 4. Net acceleration (N, 2)
    # We multiply by masses and sum across the 'other' planets
    a = np.einsum('nj,njd,j->nd', inv_r3, diff, masses)
    return a

def derivative(state : np.ndarray, masses : np.ndarray) -> np.ndarray:
    #produces velocity/acceleration matrix from state matrix

    derivative_matrix = np.zeros_like(state)

    derivative_matrix[:, 0] = state[:, 1]

    derivative_matrix[:, 1] = acc_matrix(state[:, 0], masses)

    return derivative_matrix

def update_planets(system: list[Planet], new_state: np.ndarray):
    #Updates the state attribute of each Planet object in the system 
    #using the output of RK4_step.
    for i, planet in enumerate(system):
        # new_state[i] is the (2, 2) matrix for the i-th planet
        # containing [[pos_x, pos_y], [vel_x, vel_y]]
        planet.state = new_state[i]

#RK4 step function
def RK4_step(t : float, dt : float, system : list[Planet]):
    state = state_matrix(system)
    masses = mass_list(system)

    k1 = derivative(state, masses)

    k2 = derivative(state + (dt/2) * k1, masses)

    k3 = derivative(state + (dt/2) * k2, masses)

    k4 = derivative(state + dt * k3, masses)

    new_state = state + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

    update_planets(system, new_state)


#____GRAPHICS____#
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#####   READ THIS: YOU NEED A LIST OF PLANET OBJECTS CALLED system
#####   FOR THIS TO WORK. BELOW IS A SET OF COMMANDS TO GENERATE A
#####   RANDOM LIST OF PLANETS WITH A SPECIFIED NUMBER OF THEM. YOU
#####   CAN USE THE "1. Initialize the system" SECTION TO SET UP YOUR OWN
#####   COMMANDS OR JUST MANUALLY GENERATE YOUR OWN SYSTEM. REMEMBER
#####   THAT EACH PLANET IS Planet(index, mass, state) WHERE state
#####   IS A MATRIX WITH A POSITION AND VELOCITY VECTOR. SYSTEM LIST
#####   JUST NEEDS TO LOOK LIKE: system = [planet_1, planet_2, etc.]
#####   FOR LARGE LISTS IT IS EASIER TO SHOW AN LLM THE PLANET TYPE
#####   (OR THE WHOLE PROGRAM) AND ASK IT TO GENERATE A LIST TO YOUR
#####   LIKING. IF YOU CHANGE THE NAME FOR YOUR SYSTEM LIST MAKE
#####   SURE YOU SWAP IT OUT IN EVERY INSTANCE IN SECTIONS 2,3, AND 4
#####   BELOW.

#####
#####
#####
# 1. Initialize the system
# State matrix format: [[x, y], [vx, vy]]
#Generate planets system
states = []
num_orbiting = 100 #choose number of planets here
for i in range(num_orbiting):
    # Random distance from the center (between 5 and 25 units)
    r = np.random.uniform(5, 25)
    
    # Random angle in radians
    theta = np.random.uniform(0, 2 * np.pi)
    
    # Calculate position (x, y)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    # Calculate velocity (vx, vy)
    # To make them "orbit," velocity is perpendicular to the position vector
    # Magnitude is kept low as requested (between 0.1 and 0.4)
    v_mag = np.random.uniform(0.1, 0.4)
    vx = -v_mag * np.sin(theta) 
    vy = v_mag * np.cos(theta)
    
    # Assemble the state matrix
    new_state = np.array([[x, y], [vx, vy]])
    states.append(new_state)

system = []
for i, s in enumerate(states):
    m = np.random.uniform(1, 1.1)
    planet = Planet(index=i, mass=m, state=s)
    system.append(planet)
#####
#####
#####

# Time step for RK4
dt = 0.005

# 2. Setup the Matplotlib Figure
# facecolor='black' handles the outer window border
fig, ax = plt.subplots(figsize=(8, 8), facecolor='black') 

# Set the actual graph area to black
ax.set_facecolor('black') 

# Kill the axes, ticks, and labels in one command
ax.axis('off')

# Remove the white margins so the black goes edge-to-edge
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

ax.set_aspect('equal')
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)

colors = plt.get_cmap('tab10').colors
markers = []
trails = []

# Initialize graphical objects for each planet
for i in range(len(system)):
    # The moving dot
    marker, = ax.plot([], [], 'o', color=colors[i % 10], markersize=2)
    markers.append(marker)
    
    # The fading trail behind it
    trail, = ax.plot([], [], '-', color=colors[i % 10], alpha=0.2, linewidth=1.5)
    trails.append(trail)

# Storage for the trails
history_x = [[] for _ in range(len(system))]
history_y = [[] for _ in range(len(system))]
trail_length = 50 # Number of past positions to keep drawn

# 3. The Animation Engine
def update(frame):
    # Run multiple physics steps per graphics frame to speed up the visual motion
    steps_per_frame = 5
    for _ in range(steps_per_frame):
        RK4_step(0, dt, system) # t=0 because RK4_step doesn't utilize time
    
    # Update graphics coordinates
    for i, p in enumerate(system):
        x, y = p.r[0], p.r[1]
        
        # Move the planet marker
        markers[i].set_data([x], [y])
        
        # Extend the trail
        history_x[i].append(x)
        history_y[i].append(y)
        
        # Chop the tail of the trail if it gets too long
        if len(history_x[i]) > trail_length:
            history_x[i].pop(0)
            history_y[i].pop(0)
            
        trails[i].set_data(history_x[i], history_y[i])
        
    # FuncAnimation needs to know exactly which objects were updated
    return markers + trails

# 4. Trigger the Animation
# blit=True is a performance boost that only redraws the moving parts
anim = FuncAnimation(fig, update, frames=None, interval=20, blit=True)

plt.show()
