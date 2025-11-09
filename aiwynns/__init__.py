"""
Aiwynn's Idea Factory
A sophisticated system for managing AI-generated fiction novel ideas
"""

__version__ = "1.0.0"
__author__ = "Aiwynn"

from .database import ConceptDatabase
from .search import SearchEngine
from .stats import StatsGenerator
from .creator import Creator

__all__ = [
    'ConceptDatabase',
    'SearchEngine',
    'StatsGenerator',
    'Creator',
]
