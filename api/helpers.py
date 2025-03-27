from typing import Dict, List, Set


def get_descendants(id: str, map: Dict[str, List[str]], visited: Set[str]):
    if id in map:
        for child in map[id]:
            if child not in visited:
                visited.add(child)
                get_descendants(child, map, visited)
