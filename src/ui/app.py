from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Dict, List
from src.algorithms.backtracking import backtracking
from src.algorithms.dsatur import dsatur
from src.algorithms.greedy import greedy_first_fit
from src.algorithms.welsh_powell import welsh_powell
from src.graph.dataset import load_records
from src.graph.models import ConflictGraph, GraphColoringResult
from src.reporting.benchmark import run_benchmark, BenchmarkStats

DEFAULT_ORDER = ["B", "A", "H", "F", "I", "E", "D", "C", "G"]

class ColoringApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Coloreo de grafos - Admision maestria")
        self.geometry("1280x820")
        self.minsize(1100, 720)

        self.records = load_records()
        self.graph = ConflictGraph.from_records(self.records)
        self.results: Dict[str, GraphColoringResult] = {}
        self.benchmarks: Dict[str, BenchmarkStats] = {}

        self.algorithm_var = tk.StringVar(value="Greedy (First-Fit)")
        self.order_var = tk.StringVar(value=", ".join(DEFAULT_ORDER))
        self.iterations_var = tk.StringVar(value="10")
        self.status_var = tk.StringVar(value="Listo para ejecutar el algoritmo de coloreo.")
        self.detail_var = tk.StringVar(value="")

        self._build_ui()
        self._draw_current_graph()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self, padding=12)
        outer.pack(fill="both", expand=True)

        controls = ttk.LabelFrame(outer, text="Controles", padding=10)
        controls.pack(fill="x")

        ttk.Label(controls, text="Algoritmo:").grid(row=0, column=0, sticky="w")
        algorithm_box = ttk.Combobox(
            controls,
            textvariable=self.algorithm_var,
            values=["Greedy (First-Fit)", "DSATUR", "Backtracking", "Welsh-Powell"],
            state="readonly",
            width=24,
        )
        algorithm_box.grid(row=0, column=1, padx=(8, 20), sticky="w")

        ttk.Label(controls, text="Orden Greedy:").grid(row=0, column=2, sticky="w")
        ttk.Entry(controls, textvariable=self.order_var, width=30).grid(row=0, column=3, padx=(8, 12), sticky="w")

        ttk.Label(controls, text="Iteraciones:").grid(row=0, column=4, sticky="w")
        ttk.Spinbox(controls, from_=1, to=100, textvariable=self.iterations_var, width=10).grid(row=0, column=5, padx=(8, 12))

        ttk.Button(controls, text="Ejecutar seleccionado", command=self.run_selected).grid(row=0, column=6, padx=(0, 8))
        ttk.Button(controls, text="Ejecutar comparacion", command=self.run_comparison).grid(row=0, column=7)

        controls.columnconfigure(8, weight=1)

        body = ttk.Frame(outer)
        body.pack(fill="both", expand=True, pady=(12, 0))

        left_panel = ttk.Frame(body)
        left_panel.pack(side="left", fill="both", expand=True)

        graph_frame = ttk.LabelFrame(left_panel, text="Grafo de conflictos", padding=8)
        graph_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(graph_frame, bg="#fbfbfb", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self._draw_current_graph())

        right_panel = ttk.Frame(body, width=360)
        right_panel.pack(side="right", fill="y", padx=(12, 0))

        summary_frame = ttk.LabelFrame(right_panel, text="Resultado", padding=8)
        summary_frame.pack(fill="x")
        ttk.Label(summary_frame, textvariable=self.status_var, wraplength=320, justify="left").pack(anchor="w")
        ttk.Label(summary_frame, textvariable=self.detail_var, wraplength=320, justify="left").pack(anchor="w", pady=(8, 0))

        comparison_frame = ttk.LabelFrame(right_panel, text="Comparacion", padding=8)
        comparison_frame.pack(fill="both", expand=True, pady=(12, 0))

        columns = ("algorithm", "bloques", "tiempo_ms", "stddev", "complejidad")
        self.table = ttk.Treeview(comparison_frame, columns=columns, show="headings", height=12)
        for column, title, width in [
            ("algorithm", "Algoritmo", 90),
            ("bloques", "Bloques (prom)", 70),
            ("tiempo_ms", "Tiempo (prom)", 70),
            ("stddev", "Desv. Est.", 60),
            ("complejidad", "Complejidad", 80),
        ]:
            self.table.heading(column, text=title)
            self.table.column(column, width=width, anchor="w")
        self.table.pack(fill="both", expand=True)

        info_frame = ttk.LabelFrame(right_panel, text="Clases", padding=8)
        info_frame.pack(fill="x", pady=(12, 0))
        classes_text = "\n".join(f"{record.id}: {record.materia} ({record.grupo}, {record.docente})" for record in self.records)
        ttk.Label(info_frame, text=classes_text, justify="left", wraplength=320).pack(anchor="w")

    def _run_algorithm(self, name: str) -> GraphColoringResult:
        if name == "Greedy (First-Fit)":
            order = [item.strip() for item in self.order_var.get().split(",") if item.strip()]
            if set(order) != set(self.graph.vertices()):
                order = DEFAULT_ORDER
            return greedy_first_fit(self.graph, order)
        if name == "DSATUR":
            return dsatur(self.graph)
        if name == "Backtracking":
            return backtracking(self.graph)
        return welsh_powell(self.graph)

    def run_selected(self) -> None:
        name = self.algorithm_var.get()
        result = self._run_algorithm(name)
        self.results = {name: result}
        self.benchmarks.clear()
        self._update_summary(result)
        self._refresh_comparison_table()
        self._draw_graph(result)

    def run_comparison(self) -> None:
        try:
            iterations = int(self.iterations_var.get())
            iterations = max(1, min(iterations, 100))
        except ValueError:
            iterations = 10

        greedy_order = [item.strip() for item in self.order_var.get().split(",") if item.strip()]
        if set(greedy_order) != set(self.graph.vertices()):
            greedy_order = DEFAULT_ORDER

        self.results.clear()
        self.benchmarks.clear()

        self.benchmarks["Greedy (First-Fit)"] = run_benchmark(
            self.graph, "Greedy (First-Fit)", greedy_first_fit, iterations, greedy_order
        )
        self.benchmarks["DSATUR"] = run_benchmark(self.graph, "DSATUR", dsatur, iterations)
        self.benchmarks["Backtracking"] = run_benchmark(self.graph, "Backtracking", backtracking, iterations)
        self.benchmarks["Welsh-Powell"] = run_benchmark(self.graph, "Welsh-Powell", welsh_powell, iterations)

        selected_name = self.algorithm_var.get()
        selected_bench = self.benchmarks.get(selected_name)
        if selected_bench:
            self.status_var.set(f"{selected_bench.algorithm}: {selected_bench.blocks_avg:.1f} bloques (prom), {selected_bench.time_avg_ms:.2f} ms")
            self.detail_var.set(f"Iteraciones: {selected_bench.iterations}\nComplejidad: {selected_bench.complexity}\nExacto: {'si' if selected_bench.exact else 'no'}")

        self._refresh_comparison_table()
        self._draw_graph_from_benchmark(selected_name)

    def _update_summary(self, result: GraphColoringResult) -> None:
        self.status_var.set(f"{result.algorithm}: {result.blocks} bloques, {result.elapsed_ms:.2f} ms")
        self.detail_var.set(f"Complejidad: {result.complexity}\nOrden: {', '.join(result.order)}\nExacto: {'si' if result.exact else 'no'}")

    def _refresh_comparison_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        for name in ["Greedy (First-Fit)", "DSATUR", "Backtracking", "Welsh-Powell"]:
            result = self.results.get(name)
            if result:
                self.table.insert("", "end", values=(
                    result.algorithm,
                    result.blocks,
                    f"{result.elapsed_ms:.2f}",
                    "N/A",
                    result.complexity,
                ))

        for name in ["Greedy (First-Fit)", "DSATUR", "Backtracking", "Welsh-Powell"]:
            bench = self.benchmarks.get(name)
            if bench:
                self.table.insert("", "end", values=(
                    bench.algorithm,
                    f"{bench.blocks_avg:.1f}",
                    f"{bench.time_avg_ms:.2f}",
                    f"{bench.time_stddev_ms:.3f}",
                    bench.complexity,
                ))

    def _draw_current_graph(self) -> None:
        selected = self.algorithm_var.get()
        if self.results:
            self._draw_graph(self.results.get(selected))
        else:
            self._draw_graph(None)

    def _draw_graph_from_benchmark(self, algorithm_name: str) -> None:
        """Dibuja el grafo sin color (solo la estructura) con las estadísticas del benchmark."""
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 900)
        height = max(self.canvas.winfo_height(), 560)
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.33

        vertices = self.graph.vertices()
        if not vertices:
            return

        positions = self._circular_positions(vertices, center_x, center_y, radius)
        palette = self._color_palette()

        for vertex in vertices:
            for neighbor in self.graph.neighbors(vertex):
                if vertex < neighbor:
                    self.canvas.create_line(*positions[vertex], *positions[neighbor], fill="#b8b8b8", width=2)

        for vertex in vertices:
            x, y = positions[vertex]
            fill = palette.get(0, "#d9edf7")
            self.canvas.create_oval(x - 24, y - 24, x + 24, y + 24, fill=fill, outline="#303030", width=2)
            self.canvas.create_text(x, y, text=vertex, font=("Segoe UI", 10, "bold"))

        bench = self.benchmarks.get(algorithm_name)
        if bench:
            title = f"{bench.algorithm} | Bloques (prom): {bench.blocks_avg:.1f} | Complejidad: {bench.complexity}"
        else:
            title = algorithm_name
        self.canvas.create_text(16, 16, text=title, anchor="nw", font=("Segoe UI", 12, "bold"), fill="#1f1f1f")

    def _draw_graph(self, result: GraphColoringResult | None) -> None:
        self.canvas.delete("all")
        width = max(self.canvas.winfo_width(), 900)
        height = max(self.canvas.winfo_height(), 560)
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) * 0.33

        vertices = self.graph.vertices()
        if not vertices:
            return

        positions = self._circular_positions(vertices, center_x, center_y, radius)
        palette = self._color_palette()

        for vertex in vertices:
            for neighbor in self.graph.neighbors(vertex):
                if vertex < neighbor:
                    self.canvas.create_line(*positions[vertex], *positions[neighbor], fill="#b8b8b8", width=2)

        for vertex in vertices:
            x, y = positions[vertex]
            color_number = result.colors.get(vertex, 0) if result else 0
            fill = palette.get(color_number, "#d9edf7")
            self.canvas.create_oval(x - 24, y - 24, x + 24, y + 24, fill=fill, outline="#303030", width=2)
            label = f"{vertex}\n{color_number}"
            self.canvas.create_text(x, y, text=label, font=("Segoe UI", 10, "bold"))

        title = self.algorithm_var.get()
        if result:
            title = f"{result.algorithm} | Bloques: {result.blocks} | Complejidad: {result.complexity}"
        self.canvas.create_text(16, 16, text=title, anchor="nw", font=("Segoe UI", 12, "bold"), fill="#1f1f1f")

    def _circular_positions(self, vertices: List[str], center_x: float, center_y: float, radius: float) -> Dict[str, tuple[float, float]]:
        import math

        positions: Dict[str, tuple[float, float]] = {}
        total = len(vertices)
        for index, vertex in enumerate(vertices):
            angle = (2 * math.pi * index / total) - math.pi / 2
            positions[vertex] = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))
        return positions

    def _color_palette(self) -> Dict[int, str]:
        return {
            0: "#d9edf7",
            1: "#f7d6d0",
            2: "#d8e8d2",
            3: "#f8e1ac",
            4: "#d7d2f2",
            5: "#cde8e8",
            6: "#f4d8ec",
        }


def launch_app() -> None:
    app = ColoringApp()
    app.mainloop()
