#!/usr/bin/env python
# -*- coding: utf-8 -*-

from akari_controller.akari_controller import AkariController

with AkariController() as controller:
    controller.enable_all_servo()
    controller.set_joint_velocities(pan=8, tilt=8)
    controller.set_joint_accelerations(pan=8, tilt=8)
    controller.move_joint_positions(pan=0, tilt=0)
