class SolverFactory:
    def __init__(self):
        self.Default = "breadthfirst"
        self.Choices = ["breadthfirst", "depthfirst", "dijkstra", "astar", "all_methods"]

    def breadthfirst_solver(self):
        import breadthfirst
        return ["Breadth first search", breadthfirst.solve]

    def depthfirst_solver(self):
        import depthfirst
        return ["Depth first search", depthfirst.solve]

    def dijkstra_solver(self):
        import dijkstra
        return ["Dijkstra's Algorithm", dijkstra.solve]

    def astar_solver(self):
        import astar
        return ["A-star Search", astar.solve]

    def create_solver(self, method):
        solvers = {
            "breadthfirst": self.breadthfirst_solver(),
            "depthfirst": self.depthfirst_solver(),
            "dijkstra": self.dijkstra_solver(),
            "astar": self.astar_solver()
        }
        if method == "all_methods":
            return self.breadthfirst_solver(), self.depthfirst_solver(), self.dijkstra_solver(), self.astar_solver()
        elif method in solvers:
            return [solvers[method]]
        else:
            return solvers[self.Default]()
