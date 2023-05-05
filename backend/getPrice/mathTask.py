from time import sleep

"""
    Temporary solution for calculating the arithmetic average cost of a car
"""

class ArithmeticMean:
    # I do not like the implementation of this class and its method, 
    # it will undergo changes in the near future
    def __init__(self) -> None:
        pass

    def mild(self, sin: list):
        if type(sin) is list:
            return

        bestInt = len(sin)
        for prom in range(1, bestInt):
            sin[0] += sin[prom]
        return sin[0], bestInt