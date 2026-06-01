from manim import *
import numpy as np


class QuantumSuperposition(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 全局字体
        # =========================
        font_cn = "SimSun"          # 宋体；如果不显示，可改为 "宋体"
        font_en = "Times New Roman"

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
            max_width=7.9
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
                width=max(text_group.width + 0.58, 5.8),
                height=text_group.height + 0.40,
                corner_radius=0.14,
                stroke_color=GRAY_D,
                stroke_width=1,
                fill_color=box_color,
                fill_opacity=0.88
            )

            group = VGroup(bg, text_group)
            group.to_edge(DOWN, buff=0.18)
            text_group.move_to(bg.get_center())

            return group

        def make_ket_card(ket, action, color):
            card = RoundedRectangle(
                width=1.42,
                height=1.02,
                corner_radius=0.14,
                stroke_color=color,
                stroke_width=2,
                fill_color="#1A1A1A",
                fill_opacity=0.92
            )

            ket_tex = MathTex(
                ket,
                font_size=31,
                color=color
            ).move_to(card.get_center() + UP * 0.18)

            action_label = Text(
                action,
                font=font_en,
                font_size=16,
                color=GRAY_A
            ).next_to(ket_tex, DOWN, buff=0.08)

            return VGroup(card, ket_tex, action_label)

        # =========================
        # 1. 标题
        # =========================
        title = bilingual_text(
            "量子叠加：把所有 action 同时摆上舞台",
            "Quantum Superposition: Put All Actions on the Stage",
            font_size_cn=35,
            font_size_en=21,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.7
        ).to_edge(UP, buff=0.35)

        self.play(FadeIn(title, shift=DOWN), run_time=1.5)
        self.wait(0.6)

        # =========================
        # 2. 左侧 Gridworld：经典 action 选择
        # =========================
        cell_size = 0.58
        grid_n = 5
        grid_center = LEFT * 3.55 + DOWN * 0.05

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

        agent_pos = cell_pos(2, 2)
        next_pos = cell_pos(2, 3)

        agent = Dot(
            agent_pos,
            radius=0.11,
            color=BLUE_B
        )

        agent_label = Text(
            "Agent",
            font=font_en,
            font_size=18,
            color=BLUE_B
        ).next_to(agent, UP, buff=0.08)

        goal = cell_pos(4, 4)
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
            Text("×", font=font_en, font_size=36, color=RED_B).move_to(cell_pos(1, 1)),
            Text("×", font=font_en, font_size=36, color=RED_B).move_to(cell_pos(2, 4)),
            Text("×", font=font_en, font_size=36, color=RED_B).move_to(cell_pos(4, 1)),
        )

        self.play(
            LaggedStart(
                *[FadeIn(s, scale=0.85) for s in grid],
                lag_ratio=0.018
            ),
            run_time=1.7
        )

        self.play(
            FadeIn(agent, scale=1.25),
            FadeIn(agent_label),
            FadeIn(goal_glow, scale=1.4),
            FadeIn(goal_star, scale=1.15),
            LaggedStart(
                *[FadeIn(t, scale=1.2) for t in traps],
                lag_ratio=0.12
            ),
            run_time=1.3
        )

        caption = bottom_caption(
            "在经典强化学习中，Agent 每一刻只能真正执行一个 action",
            "In classical RL, the agent can only execute one action at a time.",
            color_cn=GRAY_A
        )

        self.play(FadeIn(caption, shift=UP), run_time=1.0)
        self.wait(0.7)

        # =========================
        # 3. 展示一次经典移动：Agent 开始移动时删除 Agent 标识
        # =========================
        classical_arrow = Arrow(
            agent_pos,
            next_pos,
            buff=0.18,
            stroke_width=6,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.25
        )

        action_label = Text(
            "right",
            font=font_en,
            font_size=16,
            color=YELLOW
        ).next_to(classical_arrow, UP, buff=0.10)

        # 关键要求：Agent 刚开始移动时就删除 Agent 标识
        self.play(
            FadeOut(agent_label),
            GrowArrow(classical_arrow),
            FadeIn(action_label),
            agent.animate.move_to(next_pos),
            run_time=1.2
        )

        self.wait(0.5)

        one_action_caption = bottom_caption(
            "这就是经典视角：一次只能落到一个具体 action 上",
            "Classically, the decision finally lands on one concrete action.",
            color_cn=YELLOW
        )

        self.play(
            FadeOut(caption),
            FadeIn(one_action_caption, shift=UP),
            run_time=0.8
        )
        self.wait(1.0)

        # =========================
        # 4. 右侧：用 2 个 qubits 编码 4 个 actions
        # =========================
        encoding_panel = RoundedRectangle(
            width=5.35,
            height=3.25,
            corner_radius=0.16,
            stroke_color=BLUE_B,
            stroke_width=2,
            fill_color="#171717",
            fill_opacity=0.92
        ).move_to(RIGHT * 2.35 + UP * 0.35)

        encoding_title = bilingual_text(
            "换一个视角：用 qubits 编码 action",
            "Encode actions using qubits",
            font_size_cn=23,
            font_size_en=15,
            color_cn=BLUE_B,
            color_en=GRAY_B,
            max_width=4.95
        ).move_to(encoding_panel.get_top() + DOWN * 0.45)

        two_qubit_note = MathTex(
            r"2\ \text{qubits} \Rightarrow 2^2 = 4\ \text{actions}",
            font_size=30,
            color=YELLOW
        ).next_to(encoding_title, DOWN, buff=0.28)

        cards = VGroup(
            make_ket_card(r"\lvert 00\rangle", "left", BLUE_B),
            make_ket_card(r"\lvert 01\rangle", "up", BLUE_B),
            make_ket_card(r"\lvert 10\rangle", "right", BLUE_B),
            make_ket_card(r"\lvert 11\rangle", "down", BLUE_B),
        ).arrange(RIGHT, buff=0.16)

        cards.scale_to_fit_width(4.85)
        cards.next_to(two_qubit_note, DOWN, buff=0.34)

        self.play(
            FadeIn(encoding_panel),
            FadeIn(encoding_title),
            run_time=0.9
        )

        self.play(Write(two_qubit_note), run_time=1.2)

        self.play(
            LaggedStart(
                *[FadeIn(card, shift=UP * 0.12) for card in cards],
                lag_ratio=0.16
            ),
            run_time=1.8
        )

        encode_caption = bottom_caption(
            "现在，四个 action 被写成四个 basis states",
            "Now the four actions are written as four basis states.",
            color_cn=BLUE_B
        )

        self.play(
            FadeOut(one_action_caption),
            FadeIn(encode_caption, shift=UP),
            run_time=0.8
        )
        self.wait(1.0)

        # =========================
        # 5. 清出空间，进入量子线路视角
        # =========================
        self.play(
            FadeOut(grid),
            FadeOut(agent),
            FadeOut(goal_star),
            FadeOut(goal_glow),
            FadeOut(traps),
            FadeOut(classical_arrow),
            FadeOut(action_label),
            FadeOut(encoding_panel),
            FadeOut(encoding_title),
            FadeOut(two_qubit_note),
            FadeOut(cards),
            FadeOut(encode_caption),
            run_time=1.0
        )

        new_title = bilingual_text(
            "H gate：把确定状态变成 superposition",
            "H Gate: From a Definite State to Superposition",
            font_size_cn=35,
            font_size_en=21,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.7
        ).to_edge(UP, buff=0.35)

        self.play(Transform(title, new_title), run_time=1.0)

        # =========================
        # 6. 两个 qubits 经过 H gate
        # =========================
        q0_line = Line(LEFT * 4.7 + UP * 1.15, RIGHT * 4.7 + UP * 1.15, color=GRAY_B, stroke_width=3)
        q1_line = Line(LEFT * 4.7 + DOWN * 0.05, RIGHT * 4.7 + DOWN * 0.05, color=GRAY_B, stroke_width=3)

        q0_label = MathTex(
            r"\lvert 0\rangle",
            font_size=31,
            color=BLUE_B
        ).next_to(q0_line.get_left(), LEFT, buff=0.18)

        q1_label = MathTex(
            r"\lvert 0\rangle",
            font_size=31,
            color=BLUE_B
        ).next_to(q1_line.get_left(), LEFT, buff=0.18)

        q0_name = Text(
            "qubit 0",
            font=font_en,
            font_size=15,
            color=GRAY_A
        ).next_to(q0_label, UP, buff=0.06)

        q1_name = Text(
            "qubit 1",
            font=font_en,
            font_size=15,
            color=GRAY_A
        ).next_to(q1_label, UP, buff=0.06)

        h_gate_0 = Square(
            side_length=0.62,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color="#2B250D",
            fill_opacity=0.85
        ).move_to(LEFT * 2.3 + UP * 1.15)

        h_gate_1 = Square(
            side_length=0.62,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color="#2B250D",
            fill_opacity=0.85
        ).move_to(LEFT * 2.3 + DOWN * 0.05)

        h_text_0 = Text(
            "H",
            font=font_en,
            font_size=28,
            color=YELLOW
        ).move_to(h_gate_0)

        h_text_1 = Text(
            "H",
            font=font_en,
            font_size=28,
            color=YELLOW
        ).move_to(h_gate_1)

        h_gates = VGroup(h_gate_0, h_gate_1, h_text_0, h_text_1)

        circuit_group = VGroup(q0_line, q1_line, q0_label, q1_label, q0_name, q1_name)

        self.play(
            Create(q0_line),
            Create(q1_line),
            FadeIn(q0_label),
            FadeIn(q1_label),
            FadeIn(q0_name),
            FadeIn(q1_name),
            run_time=1.4
        )

        h_caption = bottom_caption(
            "H gate 的作用，是把一个确定的 qubit 变成两种状态的叠加",
            "The H gate turns one definite qubit into a superposition of two states.",
            color_cn=YELLOW
        )

        self.play(FadeIn(h_caption, shift=UP), run_time=0.9)
        self.play(FadeIn(h_gates, scale=0.8), run_time=1.0)

        # 两个 qubits 经过 H 后的状态
        plus0 = MathTex(
            r"{1\over\sqrt{2}}(\lvert 0\rangle+\lvert 1\rangle)",
            font_size=30,
            color=GREEN_B
        ).next_to(q0_line.get_right(), RIGHT, buff=0.18)

        plus1 = MathTex(
            r"{1\over\sqrt{2}}(\lvert 0\rangle+\lvert 1\rangle)",
            font_size=30,
            color=GREEN_B
        ).next_to(q1_line.get_right(), RIGHT, buff=0.18)

        self.play(
            FadeIn(plus0, shift=RIGHT),
            FadeIn(plus1, shift=RIGHT),
            run_time=1.3
        )
        self.wait(0.8)

        # =========================
        # 7. 形成四个 actions 的均匀 superposition
        # =========================
        superposition_formula = MathTex(
            r"\lvert \psi \rangle",
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
            font_size=35
        ).move_to(DOWN * 1.45)

        for idx in [4, 6, 8, 10]:
            superposition_formula[idx].set_color(BLUE_B)

        self.play(
            FadeOut(h_caption),
            Write(superposition_formula),
            run_time=2.2
        )

        formula_caption = bottom_caption(
            "让四个 action 同时拥有振幅",
            "This does not read four answers at once; it gives all actions amplitudes.",
            color_cn=BLUE_B
        )

        self.play(FadeIn(formula_caption, shift=UP), run_time=0.9)
        self.wait(1.4)

        # =========================
        # 8. 概率柱：每个 action 初始概率 25%
        # =========================
        self.play(
            FadeOut(circuit_group),
            FadeOut(h_gates),
            FadeOut(plus0),
            FadeOut(plus1),
            FadeOut(superposition_formula),
            FadeOut(formula_caption),
            run_time=0.9
        )

        bars_title = bilingual_text(
            "测量前：四个 action 的概率相等",
            "Before measurement: four actions have equal probability",
            font_size_cn=31,
            font_size_en=19,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.0
        ).to_edge(UP, buff=0.48)

        self.play(Transform(title, bars_title), run_time=1.0)

        axes_line = Line(
            LEFT * 4.2 + DOWN * 1.65,
            RIGHT * 4.2 + DOWN * 1.65,
            color=GRAY_B,
            stroke_width=2
        )

        action_names = ["left", "up", "right", "down"]
        ket_names = [
            r"\lvert 00\rangle",
            r"\lvert 01\rangle",
            r"\lvert 10\rangle",
            r"\lvert 11\rangle",
        ]

        bar_group = VGroup()
        bar_labels = VGroup()
        prob_labels = VGroup()

        for i in range(4):
            x = -2.7 + i * 1.8
            height = 1.35

            bar = Rectangle(
                width=0.55,
                height=height,
                stroke_color=BLUE_B,
                stroke_width=2,
                fill_color=BLUE_B,
                fill_opacity=0.65
            ).move_to(np.array([x, -1.65 + height / 2, 0]))

            ket_label = MathTex(
                ket_names[i],
                font_size=27,
                color=BLUE_B
            ).next_to(bar, DOWN, buff=0.18)

            action_text = Text(
                action_names[i],
                font=font_en,
                font_size=16,
                color=GRAY_A
            ).next_to(ket_label, DOWN, buff=0.06)

            prob_text = MathTex(
                r"25\%",
                font_size=26,
                color=YELLOW
            ).next_to(bar, UP, buff=0.12)

            bar_group.add(bar)
            bar_labels.add(VGroup(ket_label, action_text))
            prob_labels.add(prob_text)

        self.play(Create(axes_line), run_time=0.6)

        self.play(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in bar_group],
                lag_ratio=0.14
            ),
            run_time=1.6
        )

        self.play(
            FadeIn(bar_labels),
            FadeIn(prob_labels),
            run_time=1.0
        )

        equal_caption = bottom_caption(
            "刚生成 superposition 时，每个 action 被测到的概率都是 25%",
            "At this moment, each action has a 25% chance of being measured.",
            color_cn=YELLOW
        )

        self.play(FadeIn(equal_caption, shift=UP), run_time=0.9)
        self.wait(1.3)

        # =========================
        # 9. 测量只能得到一个 action
        # =========================
        measurement_box = RoundedRectangle(
            width=2.3,
            height=0.85,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color="#2A220C",
            fill_opacity=0.92
        ).move_to(UP * 1.25)

        measure_text = Text(
            "measure",
            font=font_en,
            font_size=26,
            color=YELLOW
        ).move_to(measurement_box)

        measure_arrow = Arrow(
            measurement_box.get_bottom(),
            bar_group[2].get_top(),
            buff=0.12,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )

        measure_group = VGroup(measurement_box, measure_text, measure_arrow)

        self.play(FadeIn(measure_group, shift=DOWN), run_time=0.9)
        self.play(
            Flash(bar_group[2], color=YELLOW, flash_radius=0.55),
            bar_group[2].animate.set_fill(YELLOW, opacity=0.85).set_stroke(YELLOW),
            prob_labels[2].animate.set_color(YELLOW),
            run_time=1.0
        )

        measure_caption = bottom_caption(
            "注意：一旦 measure，最终仍然只会坍缩成一个 action",
            "Important: measurement still collapses the state to one action.",
            color_cn=RED_B
        )

        self.play(
            FadeOut(equal_caption),
            FadeIn(measure_caption, shift=UP),
            run_time=0.8
        )
        self.wait(1.5)

        # =========================
        # 10. 引出 Grover：测量前能否改变概率？
        # =========================
        pre_grover_caption = bottom_caption(
            "真正的关键是：measure 之前，能不能先改变这些概率？",
            "The key is: can we reshape these probabilities before measurement?",
            color_cn=YELLOW
        )

        self.play(
            FadeOut(measure_caption),
            FadeIn(pre_grover_caption, shift=UP),
            run_time=0.9
        )
        self.wait(1.4)

        # 按前面风格：清屏后居中引出下一段
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)

        next_hint_cn = Text(
            "如何把 best action 的概率从 25% 放大到接近 1？",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "How can we amplify the probability of the best action toward 1?",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        self.play(FadeIn(next_hint, shift=UP), run_time=1.1)
        self.wait(2.2)