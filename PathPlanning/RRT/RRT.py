# author: 0aqz0
# date: 2018/11/24
"""
RRT path planning implementation with python
"""

class Node:
    """
    RRT node
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

