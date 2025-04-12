import functools
import random
from copy import copy
import csv

import numpy as np
from gymnasium.spaces import Box
from pettingzoo import ParallelEnv

from ns3gym import ns3_multiagent_env as ns3env


class CustomEnvironment(ParallelEnv):

    metadata = {
        "name": "custom_environment_v0",
    }

    def __init__(self):
        
        port=9999
        simTime= 45
        stepTime=0.2
        startSim=0
        seed=3
        simArgs = {"--duration": simTime,}
        debug=True
        max_env_steps = 250
        self.env = ns3env.MultiEnv(port=port, stepTime=stepTime, startSim=startSim, simSeed=seed, simArgs=simArgs, debug=debug)
        self.env._max_episode_steps = max_env_steps
        self.Cell_num=6
        self.max_throu=30
        self.Users=40
        self.state_dim = self.Cell_num*4
        self.action_dim =  self.env.action_space.shape[0]
        self.action_bound =  self.env.action_space.high

        self.possible_agents = ["eNodeB_1", "eNodeB_2", "eNodeB_3", "eNodeB_4", "eNodeB_5", "eNodeB_6"]

    def reset(self, seed=None, options=None):

        state = self.env.reset()
        for i in range(len(state)):
            state1 = np.reshape(state[i]['rbUtil'], [self.Cell_num, 1])#Reshape the matrix
            state2 = np.reshape(state[i]['dlThroughput'],[self.Cell_num,1])
            state2_norm=state2/self.max_throu
            state3 = np.reshape(state[i]['UserCount'], [self.Cell_num, 1])#Reshape the matrix
            state3_norm=state3/self.Users
            MCS_t=np.array(state[i]['MCSPen'])
            state4=np.sum(MCS_t[:,:10], axis=1)
            state4=np.reshape(state4,[self.Cell_num,1])
            # To report other reward functions
            # R_rewards = np.reshape(state['rewards'], [3, 1])#Reshape the matrix
            # R_rewards =[j for sub in R_rewards for j in sub]

            state[i]  = np.concatenate((state1,state2_norm,state3_norm,state4),axis=None)
            state[i] = np.reshape(state[i], [self.state_dim,])###



        self.agents = copy(self.possible_agents)
        self.timestep = 0

        observations = { a: state[i] for i, a in enumerate(self.agents) }

        # Get dummy infos. Necessary for proper parallel_to_aec conversion
        infos = {a: {'env_defined_actions':  None,} for a in self.agents}

        return observations, infos

    def step(self, actions):
        
        # Execute actions
        for i in range(len(actions)):
            actions[i] = actions[i] * self.action_bound
        next_state, reward, done, info = self.env.step(actions)

        for i in range(len(next_state)):
            state1 = np.reshape(next_state[i]['rbUtil'], [self.Cell_num, 1])#Reshape the matrix
            state2 = np.reshape(next_state[i]['dlThroughput'],[self.Cell_num,1])
            state2_norm=state2/self.max_throu
            state3 = np.reshape(next_state[i]['UserCount'], [self.Cell_num, 1])#Reshape the matrix
            state3_norm=state3/self.Users
            MCS_t=np.array(next_state[i]['MCSPen'])
            state4=np.sum(MCS_t[:,:10], axis=1)
            state4=np.reshape(state4,[self.Cell_num,1])

            print("action:{}".format((actions[self.agents[i]])))
            # print("Reward functions:{}".format((R_rewards)))

            print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
            next_state[i]  = np.concatenate((state1,state2_norm,state3_norm,state4),axis=None)
            next_state[i] = np.reshape(next_state[i], [self.state_dim,])

        # Check termination conditions
        terminations = {a: False for a in self.agents}
        rewards = {a: 0 for a in self.agents}

        # Check truncation conditions (overwrites termination conditions)
        truncations = {a: False for a in self.agents}
        if self.timestep > 100:
            truncations = {a: True for a in self.agents}
        self.timestep += 1

        # Get observations
        observations = {
            a: (
                next_state[i]
            )
            for i, a in enumerate(self.agents)
        }

        infos = {a: {'env_defined_actions':  None,} for a in self.agents}

        if any(terminations.values()) or all(truncations.values()):
            self.agents = []

        return observations, rewards, terminations, truncations, infos

    def render(self):
        """Renders the environment."""
        print("")

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        return Box(low=0, high=self.Users, shape=(self.state_dim,), dtype=np.float32)

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return Box(low=-1, high=1, shape=(self.Cell_num,), dtype=np.float32)