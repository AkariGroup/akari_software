#!/usr/bin/env python
# -*- coding: utf-8 -*-

from akari_controller import AkariClient

with AkariClient() as akari:
    akari.joints.disable_all_servo()
