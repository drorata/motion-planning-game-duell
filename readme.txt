Title: On Sampling Based Algorithms for Solving the Motion Planning Problem

Abstract:

Given a robot and a workspace scattered with obstacles, a natural problem to consider is the motion planning problem (a.k.a. the "piano movers problem"). That is, given the source and target placements of the robot in the workspace, determine whether the robot can move from one placement to the other. Additionally, if such movement is possible, a feasible description is also desired. This problem was first posed over four decades ago.

A sample based algorithm for solving the motion planning problem functions in two phases. First, it studies the connectivity of the corresponding configuration space. Second, based on the study phase, it answers queries determining whether and how the robot can be moved from one placement to the other.

In this talk we present in detail one of the most celebrated sample based algorithms: the Probabilistic Roadmap Method. We elaborate on some implementation details of the method and prove that it is probabilistically complete. Furthermore, we briefly present a more recent sampling based algorithm known as the Motion Planning via Manifold Samples.
