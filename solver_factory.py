class SolverFactory:
    def __init__(self):
        self.Default = "breadthfirst"
        self.Choices = ["breadthfirst", "depthfirst", "dijkstra", "astar"]

    def create_solver(self, type):
        if type == "depthfirst":
            import depthfirst
            return ["Depth first search", depthfirst.solve]
        elif type == "dijkstra":
            import dijkstra
            return ["Dijkstra's Algorithm", dijkstra.solve]
        elif type == "astar":
            import astar
            return ["A-star Search", astar.solve]
        else:
            import breadthfirst
            return ["Breadth first search", breadthfirst.solve]
