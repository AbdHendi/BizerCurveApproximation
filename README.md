# BizerCurveApproximation
An interactive GUI where users sketch curves on a whiteboard. The system approximates these using Bezier curves, optimizing for fewer control points while maintaining curve integrity

### Initial Solution Generation:

1. Based on user-provided sketch points, it generates an initial set of control points.
The control points are initialized randomly but are constrained to the range of input sequence points.
2. It ensures that the start and end control points match the start and end of the user's sketched points.
### Optimization:

1. Utilizes an iterative optimization algorithm to minimize the error between the approximated Bezier curve and the user's sketched curve.
2. Control points are adjusted based on a set of possible move options to enhance the curve approximation.
3. It visually tracks the optimization progress by plotting the approximated curve against the user's sketched curve.
4. Errors are computed and minimized for each segment until either the error is below a threshold or a maximum iteration count is reached.
### Modules:
1. fixed_length_connection_points: Determines the connection point indices based on a fixed length.
2. generate_initial_solution: Produces an initial set of control points.
3. optimization: Implements the optimization algorithm to refine the control points.

### Result Samples:

![spat](https://github.com/AbdHendi/BizerCurveApproximation/assets/87819598/ca64f813-b2a8-4ac6-9fc4-99b59927302f)


![5](https://github.com/AbdHendi/BizerCurveApproximation/assets/87819598/6481195f-5120-411e-8ec2-e71c95413654)
