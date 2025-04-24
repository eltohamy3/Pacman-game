import heapq  # class search
from collections import deque
from configuration import GRID_WIDTH

direction_array = [ (0 , 1), (0 , -1), (1 , 0), (-1 , 0)]

def euclidean_heuristic ( a , b ) :
    return ((a[0]  - b[0]) ** 2 + (a[1] - b[1]) ** 2 ) ** 0.5

def manhattan_heuristic (self, a , b ) :
    return abs(a  - b ) + abs(a [1] - b [1])

def dfs ( maze , start) :
        stack = [start]
        visited = set()
        parent = { }
        visited.add ( start )
        while stack :
            current = stack.pop ( )

            if current in maze.get_uneaten_dots():
                return reconstruct_path ( start , current , parent ) , visited

            x , y = current
            for dx , dy in direction_array :
                nx , ny = x + dx , y + dy

                isGate = maze.is_gate(x, y)
                if not maze.is_valid(nx, ny) and isGate:
                    nx = 0 if x != 0 else GRID_WIDTH - 1
                if maze.is_valid(nx, ny) and (nx , ny) not in visited :
                    stack.append ( (nx , ny) )
                    visited.add ( (nx , ny) )
                    parent [(nx , ny)] = current

        return [], visited

def bfs ( maze , start) :
    queue = deque ( [start] )
    visited = set (  )
    parent = { }
    visited.add ( start )

    while queue :
        current = queue.popleft ( )

        if current in maze.get_uneaten_dots() :
            return reconstruct_path ( start , current , parent ) , visited

        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy

            isGate = maze.is_gate(x, y)
            if not maze.is_valid(nx, ny) and isGate:
                nx = 0 if x != 0 else GRID_WIDTH - 1

            if maze.is_valid(nx, ny) and (nx , ny) not in visited :
                queue.append ( (nx , ny) )
                visited.add ( (nx , ny) )
                parent [(nx , ny)] = current
    return [], visited

def ucs ( maze , start) :
    heap = [(0 , start)]
    visited = set ( )
    parent = { }
    # The cost at each position
    cost_so_far = { start : 0 }
    while heap :
        cost , current = heapq.heappop ( heap )
        if current in visited :
            continue

        visited.add ( current )

        if current in maze.goals :
            return reconstruct_path ( start , current , parent ) , visited

        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy

            isGate = maze.is_gate(x, y)
            if not maze.is_valid(nx, ny) and isGate:
                nx = 0 if x != 0 else GRID_WIDTH - 1

            new_cost = cost + 1
            if maze.is_valid(nx, ny) and ((nx , ny) not in cost_so_far or new_cost < cost_so_far [(nx , ny)]) :
                cost_so_far [(nx , ny)] = new_cost
                heapq.heappush ( heap , (new_cost , (nx , ny)) )
                parent [(nx , ny)] = current
    return [], visited

def a_star ( maze , start) :
    goal = next(iter(maze.goals))
    heap = [(0 , start)]
    parent = { }
    cost_to_node = { start : 0 }
    visited = set ( )
    while heap :
        _ , current = heapq.heappop ( heap )

        if current == goal :
            return reconstruct_path ( start , current , parent ) , visited

        visited.add ( current )
        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy
            isGate = maze.is_gate(x, y)
            if not maze.is_valid(nx, ny) and isGate:
                nx = 0 if x != 0 else GRID_WIDTH - 1

            new_g = cost_to_node [current] + 1
            if maze.is_valid(nx, ny) and ((nx , ny) not in cost_to_node or new_g < cost_to_node [(nx , ny)]) :
                cost_to_node [(nx , ny)] = new_g
                estimated_cheapest_cost = new_g + euclidean_heuristic((nx, ny), goal)
                heapq.heappush ( heap , (estimated_cheapest_cost , (nx , ny)) )
                parent [(nx , ny)] = current
    return [], visited

def greedy ( maze , start) :
    goal = next(iter(maze.goals))
    heap = [(euclidean_heuristic(start, goal), start)]
    parent = { }
    visited = set ( )
    while heap :
        _ , current = heapq.heappop ( heap )
        if current == goal :
            return reconstruct_path ( start , current , parent ) , visited

        if current in visited :
            continue


        visited.add ( current )
        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy

            isGate = maze.is_gate(x, y)
            if not maze.is_valid(nx, ny) and isGate:
                nx = 0 if x != 0 else GRID_WIDTH - 1

            if maze.is_valid(nx, ny) and (nx , ny) not in visited :
                heapq.heappush (heap, (euclidean_heuristic((nx, ny), goal), (nx , ny)))
                parent [(nx , ny)] = current
    return [], visited

def reconstruct_path ( start , goal , parent ) :
    path = []
    node = goal
    while node != start :
        path.append ( node )
        node = parent.get ( node )
        if node is None :
            return []
    path.reverse ( )
    return path