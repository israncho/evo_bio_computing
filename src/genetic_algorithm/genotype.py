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
    def mutation(self, mutation_rate) -> None:
        ''' Perform the mutation operation on the current genotype.

        Args:
            mutation_rate (float): The mutation rate that controls
                the probability of mutation. It should be a value in
                the range [0, 1], where 0 means no mutation, and 1
                means all genes should mutate.

        Returns:
            None:

        Raises:
            ValueError: If the mutation rate is not in the
                valid range [0, 1]. '''
        pass


    @classmethod
    @abstractmethod
    def generate_population(cls, size: int, problem_instance) -> Iterable:
        '''
        Generate an initial population of genotypes tailored to a
        specific problem.

        Args:
            cls (class): The class itself.
            size (int): The desired size of the population.
            problem_instance: An instance of the specific problem,
                providing necessary information
                for generating suitable initial populations.

        Returns:
            Iterable: An iterable containing the initial
                population of genotypes. '''
        pass


    @abstractmethod
    def remaining_lifetime(self):
        ''' Calculate and return the remaining lifetime of
        the genotype

            Returns:
                Any: The remaining lifetime of the genotype. '''
        pass


    @abstractmethod
    def set_lifetime(self, new_lifetime_value) -> None:
        '''
         Set the remaining lifetime of a genotype.

        Args:
            new_lifetime_value: The new remaining lifetime value to be
            assigned to the genotype.

        Returns:
            None '''
        pass
