#!/usr/bin/env python
# coding:utf-8

"""
m5 init
Created on 2020/06/04
@author: Kazuya Yamamoto
"""

from akari_controller import AkariClient


def main() -> None:
    with AkariClient() as akari:
        akari.m5stack.get()


if __name__ == "__main__":
    main()
