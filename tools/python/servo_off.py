#!/usr/bin/env python
# -*- coding: utf-8 -*-

from akari_controller.akari_controller import AkariController

with AkariController() as controller:
    controller.disable_all_servo()
