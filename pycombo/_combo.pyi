# SPDX-License-Identifier: GPL-3.0-or-later
from typing import List, Optional, Tuple

def execute_from_file(
    graph_path: str,
    modularity_resolution: float = 1.0,
    max_communities: Optional[int] = None,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    random_seed: Optional[int] = None,
) -> Tuple[List[int], float]: ...

def execute_from_matrix(
    matrix: List[List[float]],
    modularity_resolution: float = 1.0,
    max_communities: Optional[int] = None,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    random_seed: Optional[int] = None,
) -> Tuple[List[int], float]: ...

def execute(
    size: int,
    edges: List[Tuple[int, int, float]],
    directed: bool = False,
    modularity_resolution: float = 1.0,
    max_communities: Optional[int] = None,
    num_split_attempts: int = 0,
    fixed_split_step: int = 0,
    start_separate: bool = False,
    treat_as_modularity: bool = False,
    verbose: int = 0,
    intermediate_results_path: Optional[str] = None,
    random_seed: Optional[int] = None,
) -> Tuple[List[int], float]: ...
