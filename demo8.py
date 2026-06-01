from manim import *
import numpy as np


class PythonCodeDemoGroverQRL(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 时间倍率
        # =========================
        # 目标时长大约 70s
        TIME_SCALE = 1.25

        def play_s(*animations, run_time=1.0, **kwargs):
            self.play(*animations, run_time=run_time * TIME_SCALE, **kwargs)

        def wait_s(duration=1.0):
            self.wait(duration * TIME_SCALE)

        # =========================
        # 字体
        # =========================
        font_cn = "SimSun"          # 宋体；如果不显示，可改为 "宋体"
        font_en = "Times New Roman"
        font_code = "Consolas"

        # =========================
        # 工具函数
        # =========================
        def bilingual_text(
            cn,
            en,
            font_size_cn=25,
            font_size_en=16,
            color_cn=WHITE,
            color_en=GRAY_B,
            buff=0.06,
            max_width=None
        ):
            cn_obj = Text(
                cn,
                font=font_cn,
                font_size=font_size_cn,
                color=color_cn
            )
            en_obj = Text(
                en,
                font=font_en,
                font_size=font_size_en,
                color=color_en
            ).next_to(cn_obj, DOWN, buff=buff)

            group = VGroup(cn_obj, en_obj)

            if max_width is not None and group.width > max_width:
                group.scale_to_fit_width(max_width)

            return group

        def bottom_caption(
            cn,
            en,
            color_cn=WHITE,
            color_en=GRAY_B,
            box_color="#181818",
            max_width=8.0
        ):
            text_group = bilingual_text(
                cn,
                en,
                font_size_cn=24,
                font_size_en=16,
                color_cn=color_cn,
                color_en=color_en,
                max_width=max_width
            )

            bg = RoundedRectangle(
                width=max(text_group.width + 0.62, 5.8),
                height=text_group.height + 0.42,
                corner_radius=0.14,
                stroke_color=GRAY_D,
                stroke_width=1,
                fill_color=box_color,
                fill_opacity=0.90
            )

            group = VGroup(bg, text_group)
            group.to_edge(DOWN, buff=0.18)
            text_group.move_to(bg.get_center())
            return group

        def code_block(lines, title_text, color=BLUE_B, width=6.1, height=4.55):
            panel = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.16,
                stroke_color=color,
                stroke_width=2,
                fill_color="#151515",
                fill_opacity=0.94
            )

            title = Text(
                title_text,
                font=font_en,
                font_size=22,
                color=color
            ).move_to(panel.get_top() + DOWN * 0.32)

            row_group = VGroup()
            rows = []

            for i, line in enumerate(lines, start=1):
                num = Text(
                    f"{i:>2}",
                    font=font_code,
                    font_size=14,
                    color=GRAY_B
                )

                txt = Text(
                    line,
                    font=font_code,
                    font_size=15,
                    color=GRAY_A
                )

                row = VGroup(num, txt).arrange(RIGHT, buff=0.18, aligned_edge=UP)
                rows.append(row)
                row_group.add(row)

            row_group.arrange(DOWN, aligned_edge=LEFT, buff=0.07)
            row_group.next_to(title, DOWN, buff=0.24)
            row_group.align_to(panel.get_left() + RIGHT * 0.20, LEFT)

            if row_group.width > width - 0.35:
                row_group.scale_to_fit_width(width - 0.35)
                row_group.next_to(title, DOWN, buff=0.24)
                row_group.align_to(panel.get_left() + RIGHT * 0.20, LEFT)

            if row_group.height > height - 0.85:
                row_group.scale_to_fit_height(height - 0.90)
                row_group.next_to(title, DOWN, buff=0.24)
                row_group.align_to(panel.get_left() + RIGHT * 0.20, LEFT)

            group = VGroup(panel, title, row_group)
            return group, rows, panel

        def highlight_row(row, color=YELLOW, buff=0.06):
            return SurroundingRectangle(
                row,
                color=color,
                buff=buff,
                stroke_width=3
            )

        def make_operator_box(label, color, center):
            box = RoundedRectangle(
                width=2.1,
                height=0.76,
                corner_radius=0.15,
                stroke_color=color,
                stroke_width=3,
                fill_color="#1A1A1A",
                fill_opacity=0.92
            ).move_to(center)

            text = Text(
                label,
                font=font_en,
                font_size=24,
                color=color
            ).move_to(box)

            return VGroup(box, text)

        # =========================
        # 1. 标题
        # =========================
        title = bilingual_text(
            "实战：Python 与 Grover 量子线路",
            "Implementation: Python and the Grover Quantum Circuit",
            font_size_cn=35,
            font_size_en=21,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.8
        ).to_edge(UP, buff=0.35)

        play_s(FadeIn(title, shift=DOWN), run_time=1.5)
        wait_s(0.7)

        # =========================
        # 2. 左侧 Gridworld 环境
        # =========================
        cell_size = 0.54
        grid_n = 5
        grid_center = LEFT * 3.75 + DOWN * 0.12

        def cell_pos(row, col):
            x = (col - 2) * cell_size
            y = (2 - row) * cell_size
            return grid_center + np.array([x, y, 0])

        grid = VGroup()
        for r in range(grid_n):
            for c in range(grid_n):
                square = Square(
                    side_length=cell_size,
                    stroke_color=GRAY_B,
                    stroke_width=2,
                    fill_color="#1E1E1E",
                    fill_opacity=0.66
                ).move_to(cell_pos(r, c))
                grid.add(square)

        start = cell_pos(0, 0)
        decision_point = cell_pos(2, 2)
        goal = cell_pos(4, 4)

        agent = Dot(start, radius=0.105, color=BLUE_B)

        agent_label = Text(
            "Agent",
            font=font_en,
            font_size=18,
            color=BLUE_B
        ).next_to(agent, UP, buff=0.08)

        goal_star = Star(
            n=5,
            outer_radius=0.17,
            inner_radius=0.075,
            color=YELLOW,
            fill_opacity=1
        ).move_to(goal)

        goal_glow = Circle(
            radius=0.28,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=YELLOW,
            fill_opacity=0.12
        ).move_to(goal)

        traps = VGroup(
            Text("×", font=font_en, font_size=34, color=RED_B).move_to(cell_pos(1, 1)),
            Text("×", font=font_en, font_size=34, color=RED_B).move_to(cell_pos(2, 4)),
            Text("×", font=font_en, font_size=34, color=RED_B).move_to(cell_pos(4, 1)),
        )

        grid_label = Text(
            "GridworldEnv",
            font=font_en,
            font_size=22,
            color=BLUE_B
        ).next_to(grid, UP, buff=0.28)

        play_s(
            LaggedStart(
                *[FadeIn(s, scale=0.85) for s in grid],
                lag_ratio=0.018
            ),
            FadeIn(grid_label),
            run_time=1.8
        )

        play_s(
            FadeIn(agent, scale=1.25),
            FadeIn(agent_label),
            FadeIn(goal_glow, scale=1.4),
            FadeIn(goal_star, scale=1.15),
            LaggedStart(
                *[FadeIn(t, scale=1.2) for t in traps],
                lag_ratio=0.12
            ),
            run_time=1.4
        )

        caption = bottom_caption(
            "左边是经典环境：它只负责接收 action，并返回 state、reward、done",
            "The classical environment receives an action and returns state, reward, and done.",
            color_cn=BLUE_B
        )

        play_s(FadeIn(caption, shift=UP), run_time=1.0)
        wait_s(1.0)

        # =========================
        # 3. 右侧展示 GridworldEnv 代码
        # =========================
        env_lines = [
            "class GridworldEnv:",
            "    def __init__(self):",
            "        self.grid = [[1, 2, 3, 4, 5],",
            "                     [6, 7, 8, 9, 10],",
            "                     [11,12,13,14,15],",
            "                     [16,17,18,19,20],",
            "                     [21,22,23,24,25]]",
            "        self.state = 1",
            "",
            "    def step(self, action):",
            "        next_state = move(action)",
            "        reward = get_reward(next_state)",
            "        done = (next_state == 25)",
            "        return next_state, reward, done",
        ]

        env_code, env_rows, env_panel = code_block(
            env_lines,
            "environment.py",
            color=BLUE_B,
            width=6.05,
            height=4.45
        )
        env_code.move_to(RIGHT * 2.55 + DOWN * 0.05)

        play_s(FadeIn(env_code, shift=LEFT), run_time=1.2)

        h_step = highlight_row(env_rows[9], color=YELLOW)
        h_return = highlight_row(env_rows[13], color=GREEN_B)

        play_s(Create(h_step), run_time=0.8)
        wait_s(0.5)
        play_s(Create(h_return), run_time=0.8)

        env_caption = bottom_caption(
            "环境部分没有量子魔法，本质还是经典强化学习的 step",
            "The environment is still classical: this is the normal RL step.",
            color_cn=GRAY_A
        )

        play_s(Transform(caption, env_caption), run_time=0.8)
        wait_s(1.3)

        # =========================
        # 4. Agent 移动到需要决策的位置
        # =========================
        path = [
            cell_pos(0, 1),
            cell_pos(1, 1),
            cell_pos(1, 2),
            cell_pos(2, 2),
        ]

        path_arrows = VGroup()
        current = start

        # 关键要求：Agent 一开始移动时就删除 Agent 标识
        first_move = True

        move_caption = bottom_caption(
            "当 Agent 走到交叉路口时，就需要调用量子线路来选择 action",
            "At a branching state, the agent calls the quantum circuit to select an action.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, move_caption), run_time=0.8)

        for p in path:
            arrow = Arrow(
                current,
                p,
                buff=0.16,
                stroke_width=5,
                color=BLUE_C,
                max_tip_length_to_length_ratio=0.25
            )
            path_arrows.add(arrow)

            if first_move:
                play_s(
                    FadeOut(agent_label),
                    GrowArrow(arrow),
                    agent.animate.move_to(p),
                    run_time=0.75
                )
                first_move = False
            else:
                play_s(
                    GrowArrow(arrow),
                    agent.animate.move_to(p),
                    run_time=0.75
                )

            current = p

        decision_ring = Circle(
            radius=0.28,
            stroke_color=YELLOW,
            stroke_width=4
        ).move_to(decision_point)

        play_s(Create(decision_ring), Flash(agent, color=YELLOW, flash_radius=0.42), run_time=0.9)
        wait_s(1.0)

        # =========================
        # 5. 切换到量子 action selection 代码
        # =========================
        play_s(
            FadeOut(env_code),
            FadeOut(h_step),
            FadeOut(h_return),
            run_time=0.8
        )

        quantum_lines = [
            "def quantum_action_selection():",
            "    qr = QuantumRegister(2)",
            "    cr = ClassicalRegister(2)",
            "    qc = QuantumCircuit(qr, cr)",
            "",
            "    qc.h(qr[0])",
            "    qc.h(qr[1])",
            "",
            "    qc, qr = gIteration11(qc, qr)",
            "    action = collapseActionSelectionMethod(qc, qr, cr)",
            "    return action",
        ]

        quantum_code, quantum_rows, quantum_panel = code_block(
            quantum_lines,
            "quantum_action.py",
            color=YELLOW,
            width=6.05,
            height=4.25
        )
        quantum_code.move_to(RIGHT * 2.55 + DOWN * 0.05)

        play_s(FadeIn(quantum_code, shift=LEFT), run_time=1.1)

        qr_highlight = highlight_row(quantum_rows[1], color=BLUE_B)
        cr_highlight = highlight_row(quantum_rows[2], color=BLUE_B)

        play_s(Create(qr_highlight), Create(cr_highlight), run_time=0.9)

        qubit_note = MathTex(
            r"2\ \text{qubits} \Rightarrow 4\ \text{actions}",
            font_size=30,
            color=YELLOW
        ).next_to(grid, DOWN, buff=0.45)

        play_s(Write(qubit_note), run_time=1.0)

        quantum_caption = bottom_caption(
            "两个 qubits 正好可以编码四个候选 action",
            "Two qubits are enough to encode four candidate actions.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, quantum_caption), run_time=0.8)
        wait_s(1.2)

        # =========================
        # 6. H gate 生成 superposition
        # =========================
        h0_highlight = highlight_row(quantum_rows[5], color=YELLOW)
        h1_highlight = highlight_row(quantum_rows[6], color=YELLOW)

        play_s(
            FadeOut(qr_highlight),
            FadeOut(cr_highlight),
            Create(h0_highlight),
            Create(h1_highlight),
            run_time=0.9
        )

        superposition_formula = MathTex(
            r"\lvert \psi\rangle",
            r"=",
            r"{1\over 2}",
            r"(",
            r"\lvert 00\rangle",
            r"+",
            r"\lvert 01\rangle",
            r"+",
            r"\lvert 10\rangle",
            r"+",
            r"\lvert 11\rangle",
            r")",
            font_size=29
        ).next_to(grid, DOWN, buff=0.44)

        for idx in [4, 6, 8, 10]:
            superposition_formula[idx].set_color(BLUE_B)

        play_s(FadeOut(qubit_note), Write(superposition_formula), run_time=1.6)

        h_caption = bottom_caption(
            "H gate 把确定的 action 状态变成均匀 superposition",
            "The H gates create a uniform superposition over all actions.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, h_caption), run_time=0.8)
        wait_s(1.4)

        # =========================
        # 7. gIteration11：Oracle + Diffusion
        # =========================
        play_s(
            FadeOut(quantum_code),
            FadeOut(h0_highlight),
            FadeOut(h1_highlight),
            FadeOut(superposition_formula),
            run_time=0.8
        )

        grover_lines = [
            "def gIteration11(qc, qr):",
            "    # Oracle: mark |11>",
            "    qc.h(qr[1])",
            "    qc.cx(qr[0], qr[1])",
            "    qc.h(qr[1])",
            "",
            "    # Diffusion",
            "    qc.h(qr)",
            "    qc.x(qr)",
            "    qc.h(qr[1])",
            "    qc.cx(qr[0], qr[1])",
            "    qc.h(qr[1])",
            "    qc.x(qr)",
            "    qc.h(qr)",
            "    return qc, qr",
        ]

        grover_code, grover_rows, grover_panel = code_block(
            grover_lines,
            "grover_iteration.py",
            color=GREEN_B,
            width=6.05,
            height=4.65
        )
        grover_code.move_to(RIGHT * 2.55 + DOWN * 0.05)

        play_s(FadeIn(grover_code, shift=LEFT), run_time=1.1)

        oracle_box = make_operator_box(
            "Oracle",
            RED_B,
            grid_center + RIGHT * 0.1 + UP * 0.75
        )

        diffusion_box = make_operator_box(
            "Diffusion",
            GREEN_B,
            grid_center + RIGHT * 0.1 + DOWN * 0.55
        )

        oracle_rows_group = VGroup(grover_rows[1], grover_rows[2], grover_rows[3], grover_rows[4])
        diffusion_rows_group = VGroup(
            grover_rows[6],
            grover_rows[7],
            grover_rows[8],
            grover_rows[9],
            grover_rows[10],
            grover_rows[11],
            grover_rows[12],
            grover_rows[13],
        )

        oracle_highlight = SurroundingRectangle(
            oracle_rows_group,
            color=RED_B,
            buff=0.07,
            stroke_width=3
        )

        diffusion_highlight = SurroundingRectangle(
            diffusion_rows_group,
            color=GREEN_B,
            buff=0.07,
            stroke_width=3
        )

        play_s(Create(oracle_highlight), FadeIn(oracle_box, shift=UP), run_time=1.0)

        oracle_caption = bottom_caption(
            "Oracle 的任务是标记目标 action，比如这里的 |11>",
            "The Oracle marks the target action, here the state |11>.",
            color_cn=RED_B
        )

        play_s(Transform(caption, oracle_caption), run_time=0.8)
        wait_s(1.4)

        play_s(Create(diffusion_highlight), FadeIn(diffusion_box, shift=DOWN), run_time=1.0)

        diffusion_caption = bottom_caption(
            "Diffusion 负责把被标记的 action 的 amplitude 放大",
            "Diffusion amplifies the amplitude of the marked action.",
            color_cn=GREEN_B
        )

        play_s(Transform(caption, diffusion_caption), run_time=0.8)
        wait_s(1.5)

        # =========================
        # 8. 用概率柱表示 gIteration 后的结果
        # =========================
        prob_axis = Line(
            grid_center + LEFT * 1.55 + DOWN * 1.35,
            grid_center + RIGHT * 1.55 + DOWN * 1.35,
            color=GRAY_B,
            stroke_width=2
        )

        bar_positions = [
            grid_center + LEFT * 1.08 + DOWN * 1.35,
            grid_center + LEFT * 0.36 + DOWN * 1.35,
            grid_center + RIGHT * 0.36 + DOWN * 1.35,
            grid_center + RIGHT * 1.08 + DOWN * 1.35,
        ]

        bars = VGroup()
        labels = VGroup()
        probs = [0.03, 0.03, 0.04, 0.90]
        ket_labels = [
            r"\lvert 00\rangle",
            r"\lvert 01\rangle",
            r"\lvert 10\rangle",
            r"\lvert 11\rangle"
        ]

        for i, p in enumerate(probs):
            height = p * 1.35
            color = YELLOW if i == 3 else BLUE_B

            bar = Rectangle(
                width=0.26,
                height=max(height, 0.04),
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.70
            ).move_to(bar_positions[i] + UP * max(height, 0.04) / 2)

            prob_text = MathTex(
                rf"{int(p * 100)}\%",
                font_size=19,
                color=color
            ).next_to(bar, UP, buff=0.07)

            ket = MathTex(
                ket_labels[i],
                font_size=18,
                color=color
            ).next_to(bar, DOWN, buff=0.10)

            bars.add(bar)
            labels.add(VGroup(prob_text, ket))

        play_s(
            FadeOut(oracle_box),
            FadeOut(diffusion_box),
            Create(prob_axis),
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bars],
                lag_ratio=0.12
            ),
            FadeIn(labels),
            run_time=1.6
        )

        amplified_caption = bottom_caption(
            "运行一次 Grover iteration 后，目标 action 的概率被明显放大",
            "After one Grover iteration, the target action becomes much more likely.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, amplified_caption), run_time=0.8)
        wait_s(1.4)

        # =========================
        # 9. collapseActionSelectionMethod：测量得到 bitstring
        # =========================
        play_s(
            FadeOut(grover_code),
            FadeOut(oracle_highlight),
            FadeOut(diffusion_highlight),
            run_time=0.8
        )

        measure_lines = [
            "def collapseActionSelectionMethod(qc, qr, cr):",
            "    qc.measure(qr[0], cr[0])",
            "    qc.measure(qr[1], cr[1])",
            "",
            "    backend = Aer.get_backend('qasm_simulator')",
            "    job = execute(qc, backend, shots=1)",
            "    counts = job.result().get_counts(qc)",
            "    bitstring = list(counts.keys())[0]",
            "    return int(bitstring, 2)",
        ]

        measure_code, measure_rows, measure_panel = code_block(
            measure_lines,
            "measurement.py",
            color=YELLOW,
            width=6.05,
            height=4.25
        )
        measure_code.move_to(RIGHT * 2.55 + DOWN * 0.05)

        play_s(FadeIn(measure_code, shift=LEFT), run_time=1.1)

        measure_highlight = SurroundingRectangle(
            VGroup(measure_rows[1], measure_rows[2]),
            color=YELLOW,
            buff=0.07,
            stroke_width=3
        )

        simulator_highlight = SurroundingRectangle(
            VGroup(measure_rows[4], measure_rows[5], measure_rows[6]),
            color=BLUE_B,
            buff=0.07,
            stroke_width=3
        )

        play_s(Create(measure_highlight), run_time=0.9)

        measure_caption = bottom_caption(
            "最后一步是 measure：量子态坍缩成一个具体 bitstring",
            "The last step is measurement: the quantum state collapses into one bitstring.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, measure_caption), run_time=0.8)
        wait_s(1.0)

        play_s(Create(simulator_highlight), run_time=0.9)

        simulator_caption = bottom_caption(
            "在本项目中，我们用 qasm_simulator 来模拟量子测量",
            "In this project, qasm_simulator is used to simulate quantum measurement.",
            color_cn=BLUE_B
        )

        play_s(Transform(caption, simulator_caption), run_time=0.8)
        wait_s(1.2)

        # =========================
        # 10. bitstring -> action
        # =========================
        bit_result_box = RoundedRectangle(
            width=3.45,
            height=1.15,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color="#211C0A",
            fill_opacity=0.92
        ).move_to(grid_center + DOWN * 0.05)

        bit_result = MathTex(
            r"\text{measure} \Rightarrow \lvert 11\rangle",
            font_size=29,
            color=YELLOW
        ).move_to(bit_result_box.get_center() + UP * 0.18)

        action_result = Text(
            "bitstring 11  ->  action = down",
            font=font_en,
            font_size=17,
            color=GRAY_A
        ).next_to(bit_result, DOWN, buff=0.10)

        bit_group = VGroup(bit_result_box, bit_result, action_result)

        play_s(
            FadeIn(bit_group, scale=1.08),
            Flash(bars[3], color=YELLOW, flash_radius=0.45),
            run_time=1.1
        )

        action_caption = bottom_caption(
            "于是，量子线路输出的 bitstring 被转换成一个具体 action",
            "The measured bitstring is converted into a concrete action.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, action_caption), run_time=0.8)
        wait_s(1.4)

        # 在环境中执行 action
        final_arrow = Arrow(
            decision_point,
            cell_pos(3, 2),
            buff=0.16,
            stroke_width=6,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.25
        )

        play_s(GrowArrow(final_arrow), agent.animate.move_to(cell_pos(3, 2)), run_time=1.0)

        execute_caption = bottom_caption(
            "action 选出来之后，流程又回到经典环境中执行",
            "Once the action is selected, it is executed in the classical environment.",
            color_cn=GREEN_B
        )

        play_s(Transform(caption, execute_caption), run_time=0.8)
        wait_s(1.6)

        # =========================
        # 11. 总结代码层面的结构
        # =========================
        summary_box = RoundedRectangle(
            width=8.2,
            height=1.62,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#222222",
            fill_opacity=0.96
        ).to_edge(DOWN, buff=0.18)

        summary_line_1 = Text(
            "Quantum module = encode actions + Grover iteration + measurement",
            font=font_en,
            font_size=20,
            color=YELLOW
        )

        summary_line_2 = Text(
            "代码里并不是替代环境，而是替代 action selection 这一步",
            font=font_cn,
            font_size=22,
            color=WHITE
        ).next_to(summary_line_1, DOWN, buff=0.10)

        summary_en = Text(
            "It replaces action selection, not the whole reinforcement learning loop.",
            font=font_en,
            font_size=15,
            color=GRAY_B
        ).next_to(summary_line_2, DOWN, buff=0.06)

        summary_text = VGroup(summary_line_1, summary_line_2, summary_en)
        summary_text.move_to(summary_box.get_center())
        summary_group = VGroup(summary_box, summary_text)

        play_s(
            FadeOut(caption),
            FadeIn(summary_group, shift=UP),
            run_time=1.0
        )
        wait_s(2.0)

        # =========================
        # 12. 为下一段：量子与经典闭环铺垫
        # =========================
        play_s(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)

        next_hint_cn = Text(
            "量子线路选出 action 后，经典 TD 如何继续学习？",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "After the quantum circuit selects an action, how does classical TD learning continue?",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        play_s(FadeIn(next_hint, shift=UP), run_time=1.1)
        wait_s(2.2)