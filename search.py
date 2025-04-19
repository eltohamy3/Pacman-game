import heapq  # class search
import math
from collections import deque


def dfs ( maze , start , goal ) :
        stack = [start]
        visited = set ( )
        # A map to track the parent of each node
        parent = { }
        visited.add ( start )
        while stack :
            current = stack.pop ( )
            if current == goal :
                break
            x , y = current
            for dx , dy in [(-1 , 0) , (1 , 0) , (0 , -1) , (0 , 1)] :
                nx , ny = x + dx , y + dy
                if maze.can_move ( nx , ny ) and (nx , ny) not in visited :
                    stack.append ( (nx , ny) )
                    visited.add ( (nx , ny) )
                    parent [(nx , ny)] = current
        return reconstruct_path ( start , goal , parent ) , visited

def bfs ( maze , start , goal ) :
    queue = deque ( [start] )
    visited = set ( )
    parent = { }
    visited.add ( start )
    while queue :
        current = queue.popleft ( )
        if current == goal :
            break
        x , y = current
        for dx , dy in [(-1 , 0) , (1 , 0) , (0 , -1) , (0 , 1)] :
            nx , ny = x + dx , y + dy
            if maze.can_move ( nx , ny ) and (nx , ny) not in visited :
                queue.append ( (nx , ny) )
                visited.add ( (nx , ny) )
                parent [(nx , ny)] = current
    return reconstruct_path ( start , goal , parent ) , visited

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
        if current == goal :
            break
        x , y = current
        for dx , dy in [(-1 , 0) , (1 , 0) , (0 , -1) , (0 , 1)] :
            nx , ny = x + dx , y + dy
            next_node = (nx , ny)
            new_cost = cost + 1
            if maze.can_move ( nx , ny ) and (next_node not in cost_so_far or new_cost < cost_so_far [next_node]) :
                cost_so_far [next_node] = new_cost
                heapq.heappush ( heap , (new_cost , next_node) )
                parent [next_node] = current
    return reconstruct_path ( start , goal , parent ) , visited

def heuristic ( a , b ) :
    return max ( abs ( a [0] - b [0] ) + abs ( a [1] - b [1] ) ,
                 math.sqrt ( pow ( a [0] - b [0] , 2 ) + pow ( a [1] - b [1] , 2 ) ) )

def a_star ( maze , start , goal ) :
    heap = [(0 , start)]
    parent = { }
    g = { start : 0 }
    visited = set ( )
    while heap :
        _ , current = heapq.heappop ( heap )
        if current == goal :
            break
        visited.add ( current )
        x , y = current
        for dx , dy in [(-1 , 0) , (1 , 0) , (0 , -1) , (0 , 1)] :
            nx , ny = x + dx , y + dy
            next_node = (nx , ny)
            new_g = g [current] + 1
            if maze.can_move ( nx , ny ) and (next_node not in g or new_g < g [next_node]) :
                g [next_node] = new_g
                f = new_g + heuristic ( next_node , goal )
                heapq.heappush ( heap , (f , next_node) )
                parent [next_node] = current
    return reconstruct_path ( start , goal , parent ) , visited

def greedy ( maze , start , goal ) :
    heap = [(heuristic ( start , goal ) , start)]
    parent = { }
    visited = set ( )
    while heap :
        _ , current = heapq.heappop ( heap )
        if current == goal :
            break
        if current in visited :
            continue
        visited.add ( current )
        x , y = current
        for dx , dy in [(-1 , 0) , (1 , 0) , (0 , -1) , (0 , 1)] :
            nx , ny = x + dx , y + dy
            next_node = (nx , ny)
            if maze.can_move ( nx , ny ) and next_node not in visited :
                heapq.heappush ( heap , (heuristic ( next_node , goal ) , next_node) )
                parent [next_node] = current
    return reconstruct_path ( start , goal , parent ) , visited

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