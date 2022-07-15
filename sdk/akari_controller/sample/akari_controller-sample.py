#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from akari_controller.akari_controller import AkariController

with AkariController() as controller:
    print(controller.get_joint_names())

    controller.enable_all_servo()

    controller.set_joint_velocities(pan=0, tilt=0)
    controller.set_joint_accelerations(pan=0, tilt=0)
    controller.move_joint_positions(pan=-0.6, tilt=-0.3)
    time.sleep(3)
    print(controller.get_joint_positions())

    controller.set_joint_velocities(pan=1)
    controller.move_joint_positions(pan=0, tilt=0.6)
    time.sleep(3)
    print(controller.get_joint_positions())

    controller.set_joint_velocities(tilt=1)
    controller.set_joint_accelerations(pan=1)
    controller.move_joint_positions(pan=0.6, tilt=-0.3)
    time.sleep(3)
    print(controller.get_joint_positions())

    controller.set_joint_accelerations(tilt=1)
    controller.move_joint_positions(pan=0, tilt=0)
    time.sleep(3)
    print(controller.get_joint_positions())

    controller.disable_all_servo()
