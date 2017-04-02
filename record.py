#!/usr/bin/env python

from PIL import Image

import gym
import gym_mupen64plus

import os
import shutil
from datetime import datetime

from utils import XboxController

# Record a sample once every SAMPLE_RATE steps
SAMPLE_RATE = 5

class Recorder(object):

    def __init__(self, env):
        self.env = env
        self.controller = XboxController()


    def run_episode(self):

        self.prep_env()

        print('beginning episode loop')
        step = 0
        total_reward = 0
        end_episode = False
        while not end_episode:
            action = self.controller.read()

            if step % SAMPLE_RATE == 0:
                recorder.save_data(self.obs, action)

            ### calibration
            action = [
                int(action[0] * 80),
                int(action[1] * -80),
                int(round(action[2])),
                int(round(action[3])),
                int(round(action[4])),
            ]

            self.obs, reward, end_episode, info = self.env.step(action)
            self.env.render()
            step += 1
            total_reward += reward


    def prep_env(self):
        self.obs = self.env.reset()
        self.env.render()
        print('env ready!')

        uid = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        self.outputDir = "samples/" + uid

        customDir = raw_input("Default directory: '" + self.outputDir + "'; press <Enter> to accept or choose your own path:")
        if customDir != "":
            self.outputDir = customDir

        if os.path.exists(self.outputDir):
            res = raw_input("Output Directory Exists - Overwrite Data? ('Yes or No')")
            if res == "Yes":
                # delete the dir
                shutil.rmtree(self.outputDir)

                # re-make dir
                os.mkdir(self.outputDir)
            else:
                raise Exception("Output Directory Exists!")
        else:
            os.mkdir(self.outputDir)

        self.t = 0


    def save_data(self, obs, action):
        image_file = self.outputDir+'/'+'img_'+str(self.t)+'.png'

        im = Image.fromarray(obs)
        im.save(image_file, "PNG")

        # make / open outfile
        outfile = open(self.outputDir+'/'+'data.csv', 'a')

        # write line
        outfile.write( image_file + ',' + ','.join(map(str, action)) + '\n' )
        outfile.close()

        self.t += 1



if __name__ == '__main__':
    
    env = gym.make('Mario-Kart-Luigi-Raceway-v0')

    recorder = Recorder(env)
    
    msg = "Press <Enter> to begin recording or press 'q' followed by <Enter> to quit..."
    user_input = raw_input(msg)
    while user_input != "q":
        recorder.run_episode()
        user_input = raw_input(msg)
        
    print "Exiting..."
