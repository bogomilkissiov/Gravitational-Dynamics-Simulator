# Gravitational-Dynamics-Simulator
This program uses 4th-order Runge-Kutta (RK4) integration to solve the coupled system describing multi-body gravitational interactions.

HOW TO USE (if you don't know python):
1. As is, the program will generate a random solar system with a set number of planets. All you would have to do is find an online python editor, paste or upload the program, and then just run it.
2. If you want to create a specific solar system or change the number of randomly generated planets, find the comment within the program itself that looks like this: #____GRAPHICS____#  and then read the comment that starts with READ ME. Beneath the READ ME portion you should see a section that is blocked off by three lines of hashes like this:

#####
#####
#####
# 1. Initialize the system
...code...
#####
#####
#####

If you want to change the number of bodies, go to this line of code: num_orbiting = 100 #choose number of planets here
And tweak the number to your liking. If you don't want 100 bodies, make it 4, or 20, or 4000. Whatever your computer can handle.
If you want to set up your own specific system, just copy and paste this prompt into an LLM along with a copy of the code for the program: "I don't know much about python. I would like to create my own custom solar system for the program I have attached. [add a description for what you want your system to look like]. Write the code to initialize this system so I can copy and paste it into the "# 1. Initialize the system" section and get the code running right away. Note that the list of planet objects you generate must be called system in order for it to work."

THE LOGIC FOR THIS PROGRAM: 
1. The simplest component of the multi-body system is a custom datatype I have called Planet. Planet has an index, a mass, and a state matrix consisting of a position and velocity vector. Ex. Titan = Planet(23, 3, [[1,1], [5,-3]])
2. The whole system is simply a list of planets. Thus system = [planet_1, planet_2, ...]
3. Because this program allows for a system of many bodies, it is easier to "glue" the state matrices of all the planets together into one large matrix that represents the state of the whole system. Provided you have a function that takes the derivative of the columns of this matrix, this makes the RK4 integration function extremely straightforward and efficient.
4. The integration is performed by the RK4_step function. Once the new general state matrix has been calculated, the exact opposite process of gluing the state matrices together is applied and all of the planet objects receive their corresponding new_state matrix. Thus all of the backend computation is done through matrices.
5. The graphics exculsively rely on the state matrices within each planet object.
6. As is, the program is designed to generate a random list of planets with varying masses and initial conditions. The range for the random parameters is finite and actually quite limited. You can tweak the program to produce any system you like or just input a system of planets manually.

MY PROCESS FOR MAKING THIS:
When I set out to write this program I only intended to make it work for the classic three body problem. The 
