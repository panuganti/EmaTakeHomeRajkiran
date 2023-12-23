from abc import ABC, abstractmethod

class MergeDevAgentInterface(abc.ABC):
    def __init__(self, config):
        self.config = config

    def display(self):
        print(f"MyClassInSubdirectory value: {self.value}")