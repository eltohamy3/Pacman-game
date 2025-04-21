import heapq  # class search
from collections import deque

direction_array = [ (-1 , 0), (1 , 0), (0 , -1), (0 , 1)]

def dfs ( maze , start , goal ) :
        stack = [start]
        visited = set()
        parent = { }
        visited.add ( start )
        while stack :
            current = stack.pop ( )

            if current in goal :
                return reconstruct_path ( start , current , parent ) , visited

            x , y = current
            for dx , dy in direction_array :
                nx , ny = x + dx , y + dy
                if maze.valid(nx, ny) and (nx , ny) not in visited :
                    stack.append ( (nx , ny) )
                    visited.add ( (nx , ny) )
                    parent [(nx , ny)] = current
        return [], visited

def bfs ( maze , start , goal ) :
    queue = deque ( [start] )
    visited = set (  )
    parent = { }
    visited.add ( start )
    while queue :
        current = queue.popleft ( )

        if current in goal :
            return reconstruct_path ( start , current , parent ) , visited

        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy
            if maze.valid(nx, ny) and (nx , ny) not in visited :
                queue.append ( (nx , ny) )
                visited.add ( (nx , ny) )
                parent [(nx , ny)] = current
    return [], visited

def ucs ( maze , start , goal ) :
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
        if current in goal :
            return reconstruct_path ( start , current , parent ) , visited
        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy
            next_node = (nx , ny)
            new_cost = cost + 1
            if maze.valid(nx, ny) and (next_node not in cost_so_far or new_cost < cost_so_far [next_node]) :
                cost_so_far [next_node] = new_cost
                heapq.heappush ( heap , (new_cost , next_node) )
                parent [next_node] = current
    return [], visited

def heuristic ( a , b ) :
    return ((a [0] - b [0]) ** 2 + (a [1] - b [1]) ** 2 ) ** 0.5

def a_star ( maze , start , goal ) :
    goal_pos = goal.pop()
    heap = [(0 , start)]
    parent = { }
    cost_to_node = { start : 0 }
    visited = set ( )
    while heap :
        _ , current = heapq.heappop ( heap )
        if current == goal_pos :
            return reconstruct_path ( start , current , parent ) , visited
        visited.add ( current )
        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy
            next_node = (nx , ny)
            new_g = cost_to_node [current] + 1
            if maze.valid(nx, ny) and (next_node not in cost_to_node or new_g < cost_to_node [next_node]) :
                cost_to_node [next_node] = new_g
                estimated_cheapest_cost = new_g + heuristic ( next_node , goal_pos )
                heapq.heappush ( heap , (estimated_cheapest_cost , next_node) )
                parent [next_node] = current
    return [], visited

def greedy ( maze , start , goal ) :
    goal_pos = goal.pop()
    heap = [(heuristic ( start , goal_pos ) , start)]
    parent = { }
    visited = set ( )
    while heap :
        _ , current = heapq.heappop ( heap )
        if current == goal_pos :
            return reconstruct_path ( start , current , parent ) , visited
        if current in visited :
            continue
        visited.add ( current )
        x , y = current
        for dx , dy in direction_array :
            nx , ny = x + dx , y + dy
            next_node = (nx , ny)
            if maze.valid(nx, ny) and next_node not in visited :
                heapq.heappush ( heap , (heuristic ( next_node , goal_pos ) , next_node) )
                parent [next_node] = current
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