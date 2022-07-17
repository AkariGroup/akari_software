#!/usr/bin/env python
# -*- coding: utf-8 -*-

from akari_client import AkariClient

with AkariClient() as akari:
    akari.joints.enable_all_servo()
    akari.joints.set_joint_velocities(pan=8, tilt=8)
    akari.joints.set_joint_accelerations(pan=8, tilt=8)
    akari.joints.move_joint_positions(pan=0, tilt=0)
