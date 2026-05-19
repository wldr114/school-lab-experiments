import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
import os

from topology import Topology
from router import NetworkSimulator


def compute_node_positions(nodes, canvas_w, canvas_h):
    positions = {}
    n = len(nodes)
    if n == 0:
        return positions
    cx, cy = canvas_w / 2, canvas_h / 2
    radius = min(canvas_w, canvas_h) / 2 - 50
    for i, node in enumerate(sorted(nodes)):
        angle = 2 * math.pi * i / n - math.pi / 2
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions[node] = (x, y)
    return positions


class RoutingSimulationGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("链路状态路由协议仿真")
        self.root.geometry("1100x700")

        self.topology = None
        self.simulator = None
        self.topology_file = None

        self.node_positions = {}
        self.node_items = {}
        self.edge_items = {}
        self.selected_edge = None

        self._build_ui()

    def _build_ui(self):
        left_frame = ttk.Frame(self.root, width=550)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)

        ttk.Label(left_frame, text="网络拓扑图").pack(pady=(5, 0))

        self.canvas = tk.Canvas(left_frame, bg="white", relief=tk.SUNKEN, bd=1)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._build_control_panel()

        self.edge_menu = tk.Menu(self.root, tearoff=0)
        self.edge_menu.add_command(label="修改链路代价", command=self._modify_edge_cost)
        self.edge_menu.add_command(label="删除链路", command=self._delete_edge)

        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)

        right_frame = ttk.Frame(self.root, width=520)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)
        right_frame.pack_propagate(False)

        ttk.Label(right_frame, text="路由表").pack()

        self.route_notebook = ttk.Notebook(right_frame)
        self.route_notebook.pack(fill=tk.BOTH, expand=True)

    def _build_control_panel(self):
        ctrl_frame = ttk.Frame(self.root)
        ctrl_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        ttk.Button(ctrl_frame, text="加载拓扑", command=self._load_topology).pack(
            side=tk.LEFT, padx=3)

        ttk.Button(ctrl_frame, text="添加链路", command=self._add_edge).pack(
            side=tk.LEFT, padx=3)

        ttk.Button(ctrl_frame, text="添加节点", command=self._add_node).pack(
            side=tk.LEFT, padx=3)

        ttk.Button(ctrl_frame, text="删除节点", command=self._delete_node).pack(
            side=tk.LEFT, padx=3)

        ttk.Button(ctrl_frame, text="刷新路由表", command=self._refresh_routing_tables).pack(
            side=tk.LEFT, padx=3)

        ttk.Button(ctrl_frame, text="保存拓扑", command=self._save_topology).pack(
            side=tk.LEFT, padx=3)

        ttk.Separator(ctrl_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Label(ctrl_frame, text="日志:").pack(side=tk.LEFT)
        self.log_var = tk.StringVar(value="就绪")
        ttk.Label(ctrl_frame, textvariable=self.log_var, foreground="gray").pack(
            side=tk.LEFT, padx=5)

    def _load_topology(self):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="选择拓扑文件",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        if not filepath:
            return
        self.topology_file = filepath
        try:
            self.topology = Topology.from_file(filepath)
        except Exception as e:
            messagebox.showerror("加载失败", str(e))
            return

        self._restart_simulator()
        self._draw_topology()
        self._build_routing_tabs()
        self._refresh_routing_tables()
        self.log_var.set(f"已加载拓扑: {os.path.basename(filepath)}  ({len(self.topology.nodes)} 个节点)")

    def _restart_simulator(self):
        if self.simulator:
            self.simulator.stop()
        self.simulator = NetworkSimulator(self.topology)
        self.simulator.start()

    def _draw_topology(self):
        self.canvas.delete("all")
        self.node_items.clear()
        self.edge_items.clear()
        self.selected_edge = None

        if not self.topology:
            return

        cw = self.canvas.winfo_width() or 540
        ch = self.canvas.winfo_height() or 400
        self.node_positions = compute_node_positions(self.topology.nodes, cw, ch)

        self._draw_edges()
        self._draw_nodes()

    def _draw_nodes(self):
        r = 22
        for node, (x, y) in self.node_positions.items():
            oid = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#4A90D9", outline="#1A3A5C", width=2, tags="node"
            )
            self.canvas.create_text(x, y, text=node, fill="white",
                                     font=("Arial", 11, "bold"), tags="node")
            self.node_items[node] = oid

    def _draw_edges(self):
        for u in self.topology.graph:
            for v, cost in self.topology.graph[u].items():
                key = tuple(sorted([u, v]))
                if key in self.edge_items:
                    continue
                x1, y1 = self.node_positions[u]
                x2, y2 = self.node_positions[v]

                dx, dy = x2 - x1, y2 - y1
                dist = math.hypot(dx, dy)
                if dist == 0:
                    continue
                r = 22
                ox1, oy1 = x1 + dx / dist * r, y1 + dy / dist * r
                ox2, oy2 = x2 - dx / dist * r, y2 - dy / dist * r

                lid = self.canvas.create_line(ox1, oy1, ox2, oy2,
                                               fill="#555", width=2, tags="edge")
                mx, my = (ox1 + ox2) / 2, (oy1 + oy2) / 2
                tid_bg = self.canvas.create_rectangle(
                    mx - 18, my - 12, mx + 18, my + 12,
                    fill="#FFF9C4", outline="#E6C300", tags="edge"
                )
                tid = self.canvas.create_text(mx, my, text=str(cost),
                                               fill="#333", font=("Arial", 10, "bold"),
                                               tags="edge")
                self.edge_items[key] = (lid, tid_bg, tid)

    def _on_canvas_click(self, event):
        self._clear_edge_highlight()

        items = self.canvas.find_overlapping(event.x - 5, event.y - 5,
                                              event.x + 5, event.y + 5)
        for item in items:
            tags = self.canvas.gettags(item)
            if "edge" in tags:
                for key, (lid, tid_bg, tid) in self.edge_items.items():
                    if item == lid or item == tid_bg or item == tid:
                        self.selected_edge = key
                        self.canvas.itemconfig(lid, fill="red", width=3)
                        return

    def _on_canvas_right_click(self, event):
        items = self.canvas.find_overlapping(event.x - 5, event.y - 5,
                                              event.x + 5, event.y + 5)
        for item in items:
            tags = self.canvas.gettags(item)
            if "edge" in tags:
                for key, (lid, tid_bg, tid) in self.edge_items.items():
                    if item == lid or item == tid_bg or item == tid:
                        self.selected_edge = key
                        self._clear_edge_highlight()
                        self.canvas.itemconfig(lid, fill="red", width=3)
                        self.edge_menu.post(event.x_root, event.y_root)
                        return

    def _clear_edge_highlight(self):
        if self.selected_edge and self.selected_edge in self.edge_items:
            lid, _, _ = self.edge_items[self.selected_edge]
            self.canvas.itemconfig(lid, fill="#555", width=2)
        self.selected_edge = None

    def _modify_edge_cost(self):
        if not self.selected_edge or not self.topology:
            return
        u, v = self.selected_edge
        old_cost = self.topology.graph[u][v]
        new_cost = simpledialog.askinteger(
            "修改链路代价",
            f"链路 {u}—{v} 的当前代价: {old_cost}\n请输入新代价 (>=1):",
            minvalue=1, initialvalue=old_cost
        )
        if new_cost is None or new_cost == old_cost:
            return

        self.topology.update_edge(u, v, new_cost)
        self.simulator.trigger_update()
        self._draw_topology()
        self._refresh_routing_tables()
        self.log_var.set(f"已修改链路 {u}—{v} 代价: {old_cost} → {new_cost}")

    def _delete_edge(self):
        if not self.selected_edge or not self.topology:
            return
        u, v = self.selected_edge
        if not messagebox.askyesno("确认删除", f"确定要删除链路 {u}—{v} 吗？"):
            return

        self.topology.remove_edge(u, v)
        self.simulator.trigger_update()
        self._draw_topology()
        self._refresh_routing_tables()
        self.log_var.set(f"已删除链路 {u}—{v}")
        self.selected_edge = None

    def _add_edge(self):
        if not self.topology:
            messagebox.showinfo("提示", "请先加载拓扑文件")
            return

        nodes = sorted(self.topology.nodes)
        dialog = AddEdgeDialog(self.root, nodes)
        self.root.wait_window(dialog.top)
        if dialog.result:
            u, v, cost = dialog.result
            self.topology.add_edge(u, v, cost)
            self.simulator = NetworkSimulator(self.topology)
            self.simulator.start()
            self._draw_topology()
            self._build_routing_tabs()
            self._refresh_routing_tables()
            self.log_var.set(f"已添加链路 {u}—{v}，代价 {cost}")

    def _add_node(self):
        if not self.topology:
            messagebox.showinfo("提示", "请先加载拓扑文件")
            return

        node_id = simpledialog.askstring("添加节点", "请输入新节点 ID:", parent=self.root)
        if not node_id:
            return
        if node_id in self.topology.nodes:
            messagebox.showwarning("警告", f"节点 {node_id} 已存在")
            return

        self.topology.add_node(node_id)
        self._restart_simulator()
        self._draw_topology()
        self._build_routing_tabs()
        self._refresh_routing_tables()
        self.log_var.set(f"已添加节点 {node_id}")

    def _delete_node(self):
        if not self.topology or len(self.topology.nodes) <= 1:
            messagebox.showinfo("提示", "至少要保留一个节点")
            return

        dialog = SelectNodeDialog(self.root, self.topology.nodes, "选择要删除的节点")
        self.root.wait_window(dialog.top)
        if dialog.result:
            node_id = dialog.result
            self.topology.remove_node(node_id)
            self._restart_simulator()
            self._draw_topology()
            self._build_routing_tabs()
            self._refresh_routing_tables()
            self.log_var.set(f"已删除节点 {node_id}")

    def _save_topology(self):
        if not self.topology or not self.topology_file:
            messagebox.showinfo("提示", "没有可保存的拓扑")
            return
        self.topology.to_file(self.topology_file)
        self.log_var.set(f"拓扑已保存到 {os.path.basename(self.topology_file)}")

    def _build_routing_tabs(self):
        for tab_id in self.route_notebook.tabs():
            self.route_notebook.forget(tab_id)

        if not self.topology:
            return

        self._route_frames = {}
        for node in sorted(self.topology.nodes):
            frame = ttk.Frame(self.route_notebook)
            self.route_notebook.add(frame, text=f"节点 {node}")

            columns = ("dest", "next_hop", "cost")
            tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
            tree.heading("dest", text="目的网络")
            tree.heading("next_hop", text="下一跳")
            tree.heading("cost", text="代价")
            tree.column("dest", width=100, anchor=tk.CENTER)
            tree.column("next_hop", width=100, anchor=tk.CENTER)
            tree.column("cost", width=100, anchor=tk.CENTER)

            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self._route_frames[node] = tree

    def _refresh_routing_tables(self):
        if not self.simulator or not self.topology:
            return

        tables = self.simulator.get_routing_tables()
        for node in sorted(self.topology.nodes):
            if node not in self._route_frames:
                continue
            tree = self._route_frames[node]
            for row in tree.get_children():
                tree.delete(row)

            rt = tables.get(node, {})
            if not rt:
                continue

            for dest, (next_hop, cost) in sorted(rt.items()):
                cost_str = str(cost) if cost != float('inf') else "∞"
                tree.insert("", tk.END, values=(dest, next_hop, cost_str))


class AddEdgeDialog:
    def __init__(self, parent, nodes):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title("添加链路")
        self.top.geometry("280x200")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        ttk.Label(self.top, text="起点:").grid(row=0, column=0, padx=10, pady=10)
        self.from_var = tk.StringVar()
        self.from_cb = ttk.Combobox(self.top, textvariable=self.from_var,
                                     values=nodes, state="readonly", width=15)
        self.from_cb.grid(row=0, column=1, padx=10)

        ttk.Label(self.top, text="终点:").grid(row=1, column=0, padx=10, pady=10)
        self.to_var = tk.StringVar()
        self.to_cb = ttk.Combobox(self.top, textvariable=self.to_var,
                                   values=nodes, state="readonly", width=15)
        self.to_cb.grid(row=1, column=1, padx=10)

        ttk.Label(self.top, text="代价:").grid(row=2, column=0, padx=10, pady=10)
        self.cost_var = tk.IntVar(value=1)
        ttk.Entry(self.top, textvariable=self.cost_var, width=17).grid(
            row=2, column=1, padx=10)

        btn_frame = ttk.Frame(self.top)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="确定", command=self._ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.top.destroy).pack(
            side=tk.LEFT, padx=5)

    def _ok(self):
        u = self.from_var.get()
        v = self.to_var.get()
        cost = self.cost_var.get()
        if u and v and cost >= 1:
            if u != v:
                self.result = (u, v, cost)
                self.top.destroy()
            else:
                messagebox.showwarning("警告", "起点和终点不能相同", parent=self.top)


class SelectNodeDialog:
    def __init__(self, parent, nodes, title):
        self.result = None
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("280x140")
        self.top.resizable(False, False)
        self.top.transient(parent)
        self.top.grab_set()

        ttk.Label(self.top, text="选择节点:").pack(pady=15)
        self.node_var = tk.StringVar()
        cb = ttk.Combobox(self.top, textvariable=self.node_var,
                           values=sorted(nodes), state="readonly", width=20)
        cb.pack()

        btn_frame = ttk.Frame(self.top)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="确定", command=self._ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.top.destroy).pack(
            side=tk.LEFT, padx=5)

    def _ok(self):
        node = self.node_var.get()
        if node:
            self.result = node
            self.top.destroy()
