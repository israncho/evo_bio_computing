from abc import ABC, abstractmethod
from typing import Iterable

class Genotype(ABC):
    ''' Abstract base class representing a genotype in a genetic algorithm.
    Genotypes are used to represent potential solutions to a problem. This
    class defines the interface for genotypes.

    Args:
        ABC (class): Abstract base class from which Genotype inherits.

    Attributes:
        None '''

    @classmethod
    @abstractmethod
    def crossover(cls, genotypes: Iterable) -> Iterable:
        ''' Perform crossover operation between genotypes.

        Args:
            cls (class): The class itself.
            genotypes (Iterable): An iterable of genotypes to be used
                in the crossover.

        Returns:
            Iterable: An iterable of genotypes resulting from the
            crossover operation. '''
        pass


    @abstractmethod
    def phenotype(self):
        ''' Calculate and return the phenotype of the genotype.

        Returns:
            Any: The phenotype representation of the genotype. '''
        pass


    @abstractmethod
    def fitness(self) -> float:
        ''' Calculate and return the fitness value of the genotype.

        Returns:
            float: The fitness value of the genotype. '''
        pass


    @abstractmethod
    def mutation(self, funct):
        ''' Mutate the genotype based on a mutation function.

        Args:
            funct (callable): The mutation function to apply to the genotype.

        Returns:
            None '''
        pass


    def remaining_lifetime(self):
        ''' Calculate and return the remaining lifetime of
        the genotype

            Returns:
                Any: The remaining lifetime of the genotype. '''
        pass
