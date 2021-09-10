import numpy as np
import gym
import pybullet_envs

from pybullet_envs.gym_locomotion_envs import WalkerBaseBulletEnv
from pybullet_envs.env_bases import MJCFBaseBulletEnv
from pybullet_envs.robot_locomotors import Ant, WalkerBase
from pybullet_envs.robot_bases import MJCFBasedRobot

class MyWalkerBase(WalkerBase):
    
  def __init__(self, fn, robot_name, action_dim, obs_dim, power):
    MJCFBasedRobot.__init__(self, fn, robot_name, action_dim, obs_dim)
    self.power = power
    self.camera_x = 0
    self.start_pos_x, self.start_pos_y, self.start_pos_z = 0, 0, 0
    self.walk_target_x = 20  # originally 1 kilometer away, now 20,20m
    self.walk_target_y = 20
    self.body_xyz = [0, 0, 0]
    self.angle_to_target = None
    
  electricity_cost = -2.0  # cost for using motors -- this parameter should be carefully tuned against reward for making progress, other values less improtant
  stall_torque_cost = -0.1  # cost for running electric current through a motor even at zero rotational speed, small
  foot_collision_cost = -1.0  # touches another leg, or other objects, that cost makes robot avoid smashing feet into itself
  foot_ground_object_names = set(["floor"])  # to distinguish ground and other objects
  joints_at_limit_cost = -0.1  # discourage stuck joints
    
  
  def calc_potential(self):
    # progress in potential field is speed*dt, typical speed is about 2-3 meter per second, this potential will change 2-3 per frame (not per second),
    # all rewards have rew/frame units and close to 1.0
    debugmode = 0
    if (debugmode):
      print("calc_potential: self.walk_target_dist")
      print(self.walk_target_dist)
      print("self.scene.dt")
      print(self.scene.dt)
      print("self.scene.frame_skip")
      print(self.scene.frame_skip)
      print("self.scene.timestep")
      print(self.scene.timestep)
        
    reward = -self.walk_target_dist / self.scene.dt
    
    return reward
    
  def step(self, a):
    if not self.scene.multiplayer:  # if multiplayer, action first applied to all robots, then global step() called, then _step() for all robots with the same actions
      self.robot.apply_action(a)
      self.scene.global_step()

    state = self.robot.calc_state()  # also calculates self.joints_at_limit

    self._alive = float(
        self.robot.alive_bonus(
            state[0] + self.robot.initial_z,
            self.robot.body_rpy[1]))  # state[0] is body height above ground, body_rpy[1] is pitch
    done = self._isDone()
    if not np.isfinite(state).all():
      print("~INF~", state)
      done = True

    if self.angle_to_target == None:
        self.angle_to_target = np.arctan2(self.walk_target_y, self.walk_target_x)
    
    angle_old = self.angle_to_target
    self.angle_to_target = self.walk_target_theta - self.body_rpy[2]
    angle_progress = float( (np.cos(self.angle_to_target) - np.cos(angle_old))/self.scene.dt )
    
    potential_old = self.potential
    self.potential = self.robot.calc_potential()
    progress = float(self.potential - potential_old)

    feet_collision_cost = 0.0
    for i, f in enumerate(
        self.robot.feet
    ):  # TODO: Maybe calculating feet contacts could be done within the robot code
      contact_ids = set((x[2], x[4]) for x in f.contact_list())
      #print("CONTACT OF '%d' WITH %d" % (contact_ids, ",".join(contact_names)) )
      if (self.ground_ids & contact_ids):
        #see Issue 63: https://github.com/openai/roboschool/issues/63
        #feet_collision_cost += self.foot_collision_cost
        self.robot.feet_contact[i] = 1.0
      else:
        self.robot.feet_contact[i] = 0.0

    electricity_cost = self.electricity_cost * float(np.abs(a * self.robot.joint_speeds).mean(
    ))  # let's assume we have DC motor with controller, and reverse current braking
    electricity_cost += self.stall_torque_cost * float(np.square(a).mean())

    joints_at_limit_cost = float(self.joints_at_limit_cost * self.robot.joints_at_limit)
    debugmode = 0
    if (debugmode):
      print("alive=")
      print(self._alive)
      print("progress")
      print(progress)
      print("electricity_cost")
      print(electricity_cost)
      print("joints_at_limit_cost")
      print(joints_at_limit_cost)
      print("feet_collision_cost")
      print(feet_collision_cost)

    self.rewards = [
        self._alive, progress, angle_progress, electricity_cost, joints_at_limit_cost, feet_collision_cost
    ]
    if (debugmode):
      print("rewards=")
      print(self.rewards)
      print("sum rewards")
      print(sum(self.rewards))
    self.HUD(state, a, done)
    self.reward += sum(self.rewards)

    return state, sum(self.rewards), bool(done), {}
    
class MyAnt(MyWalkerBase):
  foot_list = ['front_left_foot', 'front_right_foot', 'left_back_foot', 'right_back_foot']

  def __init__(self):
    MyWalkerBase.__init__(self, "ant.xml", "torso", action_dim=8, obs_dim=28, power=2.5)

  def alive_bonus(self, z, pitch):
    return +1 if z > 0.26 else -1  # 0.25 is central sphere rad, die if it scrapes the ground

class MyAntBulletEnv(WalkerBaseBulletEnv):

  def __init__(self, render=False):
    self.robot = MyAnt()
    
    self.camera_x = 0
    self.walk_target_x = 20  # originally 1 kilometer away, now 20,20m
    self.walk_target_y = 20
    self.stateId = -1
    MJCFBaseBulletEnv.__init__(self, self.robot, render)