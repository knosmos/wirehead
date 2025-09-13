import math
from typing import Any, NamedTuple

from ortools.sat.python import cp_model

_LAMBDA_SIZE = 2
_LAMBDA_WIRE = 4
_SCALE = 100.0


class WireInfo(NamedTuple):
    source: int
    dest: int
    location_source: tuple[float, float]
    location_dest: tuple[float, float]


def pack_components_general(
    rects: list[tuple[float, float]], wires: list[WireInfo]
) -> list[tuple[float, float]]:
    """
    Packs rectangles that minimizes some combination of:
    1) sum of wire lengths
    2) perimeter (has to be linear)

    Assumes that (0, 0) is the bottom left.

    Args:
        rects: list of (width, height) of each rectangle
        wires: list of (source, dest, location_source, location_dest) indicating that
               1) wire from rects[source] to recs[dest] (0-indexed)
               2) location_source is the point of the wire in source with respect to its bottom left
               3) location_dest is the point of the wire in dest with respect to its bottom left

    Returns:
        Coordinates of the bottom left of each rectangle with the i-th coordinate corresponding
        to the i-th rectangle in the input.
    """
    model = cp_model.CpModel()
    n = len(rects)

    # Maximum size
    x_sum = max(1, sum(math.ceil(w * _SCALE) for w, _ in rects))
    y_sum = max(1, sum(math.ceil(h * _SCALE) for h, _ in rects))

    # Basic coordinate variables
    x = [model.NewIntVar(0, x_sum, f"x[{i}]") for i in range(n)]
    y = [model.NewIntVar(0, y_sum, f"y[{i}]") for i in range(n)]

    # Overlap constrains
    x_intervals = []
    y_intervals = []

    for i, (w_true, h_true) in enumerate(rects):
        w_scaled = math.ceil(w_true * _SCALE)
        h_scaled = math.ceil(h_true * _SCALE)

        x_intervals.append(
            model.NewFixedSizeIntervalVar(x[i], w_scaled, f"x_intervals[{i}]")
        )
        y_intervals.append(
            model.NewFixedSizeIntervalVar(y[i], h_scaled, f"y_intervals[{i}]")
        )

    model.AddNoOverlap2D(x_intervals, y_intervals)

    # Size of grid determined from locations
    w_used = model.NewIntVar(0, x_sum, "w_used")
    h_used = model.NewIntVar(0, y_sum, "h_used")

    model.AddMaxEquality(
        w_used, [x[i] + math.ceil(rects[i][0] * _SCALE) for i in range(n)]
    )
    model.AddMaxEquality(
        h_used, [y[i] + math.ceil(rects[i][1] * _SCALE) for i in range(n)]
    )

    def endpoint_expr(i: int, px: float, py: float) -> Any:
        px_scaled = round(px * _SCALE)
        py_scaled = round(py * _SCALE)
        sx = x[i] + px_scaled
        sy = y[i] + py_scaled
        return sx, sy

    wire_abs_terms = []
    for i, w in enumerate(wires):
        sx, sy = endpoint_expr(w.source, *w.location_source)
        dx, dy = endpoint_expr(w.dest, *w.location_dest)

        # Set variables to equal the wire length manhatten distance componenents
        dx_diff = model.NewIntVar(-x_sum, x_sum, f"dx_diff[{i}]")
        dy_diff = model.NewIntVar(-y_sum, y_sum, f"dy_diff[{i}]")
        model.Add(dx_diff == sx - dx)
        model.Add(dy_diff == sy - dy)

        dx_abs = model.NewIntVar(0, x_sum, f"dx_abs[{i}]")
        dy_abs = model.NewIntVar(0, y_sum, f"dy_abs[{i}]")
        model.AddAbsEquality(dx_abs, dx_diff)
        model.AddAbsEquality(dy_abs, dy_diff)

        wire_abs_terms.append(dx_abs)
        wire_abs_terms.append(dy_abs)

    # Minimize
    size_expr = w_used + h_used
    wire_expr = cp_model.LinearExpr.Sum(wire_abs_terms) if wire_abs_terms else 0
    model.Minimize(_LAMBDA_SIZE * size_expr + _LAMBDA_WIRE * wire_expr)

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0

    status = solver.Solve(model)

    # Get answer
    if status == cp_model.OPTIMAL:
        print("Found optimal solution")
    elif status == cp_model.FEASIBLE:
        print("Found feasible solution")
    elif status == cp_model.INFEASIBLE:
        raise RuntimeError("Problem is infeasible - no valid packing exists")
    elif status == cp_model.MODEL_INVALID:
        raise RuntimeError("Model is invalid - check constraints")
    else:
        raise RuntimeError(f"Solver failed with status: {status}")

    sol = []

    for i in range(len(rects)):
        xi = solver.Value(x[i]) / _SCALE
        yi = solver.Value(y[i]) / _SCALE
        sol.append((xi, yi))

    return sol


# Testing
if __name__ == "__main__":
    import random

    import matplotlib.patches as patches
    import matplotlib.pyplot as plt
    import numpy as np

    # Set random seed for reproducible results
    random.seed(42)
    np.random.seed(42)

    print("Creating visualization test with 8 rectangles and 20 wire connections...")

    # Start with complex test case
    simple_test = False

    if simple_test:
        print("🧪 Testing simple case: 3 rectangles, few wires")
        rects = [
            (2.0, 1.0),  # Rectangle 0
            (1.5, 1.5),  # Rectangle 1
            (1.0, 2.0),  # Rectangle 2
        ]
        rot = [False, False, False]  # No rotation for simplicity
        wire_connections = [
            (0, 1),  # Just a few connections
            (1, 2),
        ]
    else:
        print("🧪 Testing complex case: 8 rectangles, 20 wires")
        # Create 8 rectangles of varying sizes (simulating different electronic components)
        rects = [
            (3.0, 2.0),  # Rectangle 0 - Large component (e.g., microcontroller)
            (2.5, 1.5),  # Rectangle 1 - Medium component (e.g., voltage regulator)
            (2.0, 2.5),  # Rectangle 2 - Tall component (e.g., capacitor bank)
            (1.5, 1.8),  # Rectangle 3 - Small component (e.g., crystal oscillator)
            (2.2, 1.2),  # Rectangle 4 - Wide component (e.g., connector)
            (1.8, 2.2),  # Rectangle 5 - Square-ish component (e.g., IC)
            (2.8, 1.4),  # Rectangle 6 - Medium-large component (e.g., power module)
            (1.2, 2.0),  # Rectangle 7 - Narrow component (e.g., sensor)
        ]

        # Allow rotation for some rectangles (mix of rotatable and fixed)
        rot = [True, False, True, False, True, False, True, False]

        # Create 20 wire connections between rectangles
        wire_connections = [
            # Main hub connections (Rectangle 0 as central hub)
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),  # Hub to 4 components
            # Secondary hub connections (Rectangle 1 as secondary hub)
            (1, 2),
            (1, 5),
            (1, 6),  # Secondary hub connections
            # Power distribution connections
            (2, 3),
            (2, 4),
            (2, 7),  # Power rail connections
            # Signal chain connections
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),  # Sequential signal chain
            # Cross connections for complex routing
            (0, 5),
            (0, 7),  # Hub to distant components
            (1, 7),
            (3, 6),  # Cross connections
            (2, 6),
            (4, 7),  # Additional cross connections
        ]

    # Create wire connections between rectangles
    # Each wire connects the center of one rectangle to the center of another
    wires = []

    # Create WireInfo objects
    for src, dest in wire_connections:
        src_w, src_h = rects[src]
        dest_w, dest_h = rects[dest]

        # Connect centers of rectangles
        wires.append(
            WireInfo(
                source=src,
                dest=dest,
                location_source=(src_w / 2, src_h / 2),  # center of source
                location_dest=(dest_w / 2, dest_h / 2),  # center of dest
            )
        )

    print(f"Generated {len(rects)} rectangles and {len(wires)} wires")

    # Pack the rectangles
    try:
        positions = pack_components_general(rects, wires)
        print("✅ Packing successful!")
        print(f"Rectangle positions: {positions}")

        # Create visualization
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))

        # Colors for rectangles (8 different colors for 8 rectangles)
        colors = [
            "lightblue",  # Rectangle 0 - Microcontroller
            "lightgreen",  # Rectangle 1 - Voltage regulator
            "lightcoral",  # Rectangle 2 - Capacitor bank
            "lightyellow",  # Rectangle 3 - Crystal oscillator
            "lightpink",  # Rectangle 4 - Connector
            "lightgray",  # Rectangle 5 - IC
            "lightcyan",  # Rectangle 6 - Power module
            "lavender",  # Rectangle 7 - Sensor
        ]

        # Draw rectangles
        for i, ((x, y), (w, h)) in enumerate(zip(positions, rects)):
            rect = patches.Rectangle(
                (x, y),
                w,
                h,
                linewidth=2,
                edgecolor="black",
                facecolor=colors[i % len(colors)],
                alpha=0.7,
            )
            ax.add_patch(rect)

            # Add rectangle label at center
            ax.text(
                x + w / 2,
                y + h / 2,
                f"R{i}",
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
            )

        # Draw wires
        for i, wire in enumerate(wires):
            src_pos = positions[wire.source]
            dest_pos = positions[wire.dest]

            # Calculate actual wire endpoints
            src_x = src_pos[0] + wire.location_source[0]
            src_y = src_pos[1] + wire.location_source[1]
            dest_x = dest_pos[0] + wire.location_dest[0]
            dest_y = dest_pos[1] + wire.location_dest[1]

            # Draw wire as line
            if wire.source == wire.dest:
                # Self-connection - draw as small circle
                circle = patches.Circle(
                    (src_x, src_y), 0.1, facecolor="red", edgecolor="darkred", alpha=0.8
                )
                ax.add_patch(circle)
            else:
                # Regular wire connection
                ax.plot([src_x, dest_x], [src_y, dest_y], "r-", linewidth=1, alpha=0.6)

                # Add small circles at endpoints
                ax.plot(src_x, src_y, "ro", markersize=3)
                ax.plot(dest_x, dest_y, "ro", markersize=3)

        # Set equal aspect ratio and adjust limits
        ax.set_aspect("equal")

        # Calculate bounds with some padding
        all_x = [pos[0] for pos in positions] + [
            pos[0] + rect[0] for pos, rect in zip(positions, rects)
        ]
        all_y = [pos[1] for pos in positions] + [
            pos[1] + rect[1] for pos, rect in zip(positions, rects)
        ]

        padding = 0.5
        ax.set_xlim(min(all_x) - padding, max(all_x) + padding)
        ax.set_ylim(min(all_y) - padding, max(all_y) + padding)

        # Add grid and labels
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_title(
            "Rectangle Packing Visualization\n"
            f"{len(rects)} rectangles, {len(wires)} wire connections"
        )

        # Add legend
        legend_elements = [
            patches.Patch(color="lightblue", label="Rectangles"),
            plt.Line2D(
                [0], [0], color="red", linewidth=2, alpha=0.6, label="Wire connections"
            ),
            plt.Line2D(
                [0],
                [0],
                marker="o",
                color="red",
                linewidth=0,
                markersize=5,
                label="Wire endpoints",
            ),
        ]
        ax.legend(handles=legend_elements, loc="upper right")

        plt.tight_layout()
        plt.show()

        # Print some statistics
        total_area = sum(w * h for w, h in rects)
        bounding_box_w = max(pos[0] + rect[0] for pos, rect in zip(positions, rects))
        bounding_box_h = max(pos[1] + rect[1] for pos, rect in zip(positions, rects))
        bounding_area = bounding_box_w * bounding_box_h
        efficiency = (total_area / bounding_area) * 100 if bounding_area > 0 else 0

        print(f"\n📊 Packing Statistics:")
        print(f"Total rectangle area: {total_area:.2f}")
        print(f"Bounding box: {bounding_box_w:.2f} × {bounding_box_h:.2f}")
        print(f"Bounding box area: {bounding_area:.2f}")
        print(f"Packing efficiency: {efficiency:.1f}%")

        # Calculate total wire length
        total_wire_length = 0
        for wire in wires:
            if wire.source != wire.dest:  # Skip self-connections
                src_pos = positions[wire.source]
                dest_pos = positions[wire.dest]
                src_x = src_pos[0] + wire.location_source[0]
                src_y = src_pos[1] + wire.location_source[1]
                dest_x = dest_pos[0] + wire.location_dest[0]
                dest_y = dest_pos[1] + wire.location_dest[1]

                wire_length = abs(src_x - dest_x) + abs(
                    src_y - dest_y
                )  # Manhattan distance
                total_wire_length += wire_length

        print(f"Total wire length (Manhattan): {total_wire_length:.2f}")

    except Exception as e:
        print(f"❌ Packing failed: {e}")
        import traceback

        traceback.print_exc()
