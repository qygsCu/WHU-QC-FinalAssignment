from manim import *
import numpy as np


class QuantumClassicalLoop(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 时间倍率
        # =========================
        # 这一段目标约 55~65s
        # 如果想更慢，可以改成 1.4
        TIME_SCALE = 1.25

        def play_s(*animations, run_time=1.0, **kwargs):
            self.play(*animations, run_time=run_time * TIME_SCALE, **kwargs)

        def wait_s(duration=1.0):
            self.wait(duration * TIME_SCALE)

        # =========================
        # 字体
        # =========================
        font_cn = "SimSun"          # 宋体；如果不显示，可改成 "宋体"
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

        def make_node(label, color, width=2.05, height=0.78):
            box = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.16,
                stroke_color=color,
                stroke_width=3,
                fill_color="#181818",
                fill_opacity=0.92
            )

            text = Text(
                label,
                font=font_en,
                font_size=20,
                color=color
            ).move_to(box)

            return VGroup(box, text)

        def code_panel(lines, title_text, color=BLUE_B, width=5.7, height=2.65):
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
                font_size=20,
                color=color
            ).move_to(panel.get_top() + DOWN * 0.30)

            rows = []
            row_group = VGroup()

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

            row_group.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            row_group.next_to(title, DOWN, buff=0.22)
            row_group.align_to(panel.get_left() + RIGHT * 0.22, LEFT)

            if row_group.width > width - 0.35:
                row_group.scale_to_fit_width(width - 0.35)
                row_group.next_to(title, DOWN, buff=0.22)
                row_group.align_to(panel.get_left() + RIGHT * 0.22, LEFT)

            group = VGroup(panel, title, row_group)

            return group, rows, panel

        def highlight_row(row, color=YELLOW):
            return SurroundingRectangle(
                row,
                color=color,
                buff=0.06,
                stroke_width=3
            )

        # =========================
        # 1. 标题
        # =========================
        title = bilingual_text(
            "量子与经典的闭环",
            "The Quantum-Classical Reinforcement Learning Loop",
            font_size_cn=36,
            font_size_en=21,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.8
        ).to_edge(UP, buff=0.35)

        play_s(FadeIn(title, shift=DOWN), run_time=1.4)
        wait_s(0.7)

        # =========================
        # 2. 左侧 Gridworld
        # =========================
        cell_size = 0.52
        grid_n = 5
        grid_center = LEFT * 3.85 + DOWN * 0.10

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

        start = cell_pos(2, 2)
        next_state = cell_pos(2, 3)
        goal = cell_pos(4, 4)

        agent = Dot(
            start,
            radius=0.10,
            color=BLUE_B
        )

        agent_label = Text(
            "Agent",
            font=font_en,
            font_size=18,
            color=BLUE_B
        ).next_to(agent, UP, buff=0.08)

        goal_star = Star(
            n=5,
            outer_radius=0.16,
            inner_radius=0.07,
            color=YELLOW,
            fill_opacity=1
        ).move_to(goal)

        goal_glow = Circle(
            radius=0.27,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=YELLOW,
            fill_opacity=0.12
        ).move_to(goal)

        traps = VGroup(
            Text("×", font=font_en, font_size=33, color=RED_B).move_to(cell_pos(1, 1)),
            Text("×", font=font_en, font_size=33, color=RED_B).move_to(cell_pos(2, 4)),
            Text("×", font=font_en, font_size=33, color=RED_B).move_to(cell_pos(4, 1)),
        )

        grid_label = Text(
            "GridworldEnv",
            font=font_en,
            font_size=21,
            color=BLUE_B
        ).next_to(grid, UP, buff=0.25)

        play_s(
            LaggedStart(
                *[FadeIn(s, scale=0.85) for s in grid],
                lag_ratio=0.018
            ),
            FadeIn(grid_label),
            run_time=1.7
        )

        play_s(
            FadeIn(agent, scale=1.25),
            FadeIn(agent_label),
            FadeIn(goal_glow, scale=1.3),
            FadeIn(goal_star, scale=1.1),
            LaggedStart(
                *[FadeIn(t, scale=1.2) for t in traps],
                lag_ratio=0.12
            ),
            run_time=1.3
        )

        caption = bottom_caption(
            "这套算法不是全量子算法，而是 quantum module 与 classical loop 的配合",
            "This is not a fully quantum algorithm, but a quantum-classical hybrid loop.",
            color_cn=YELLOW
        )

        play_s(FadeIn(caption, shift=UP), run_time=1.0)
        wait_s(1.2)

        # =========================
        # 3. 右侧闭环结构
        # =========================
        quantum_node = make_node("quantum module", YELLOW, width=2.35)
        env_node = make_node("env.step", BLUE_B, width=1.85)
        td_node = make_node("TD update", GREEN_B, width=1.95)
        memory_node = make_node("memory", PURPLE_B, width=1.75)

        quantum_node.move_to(RIGHT * 2.50 + UP * 1.35)
        env_node.move_to(RIGHT * 4.50 + DOWN * 0.05)
        td_node.move_to(RIGHT * 2.50 + DOWN * 1.45)
        memory_node.move_to(RIGHT * 0.50 + DOWN * 0.05)

        arrow_q_env = Arrow(
            quantum_node.get_right(),
            env_node.get_top(),
            buff=0.18,
            color=GRAY_A,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )

        arrow_env_td = Arrow(
            env_node.get_bottom(),
            td_node.get_right(),
            buff=0.18,
            color=GRAY_A,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )

        arrow_td_mem = Arrow(
            td_node.get_left(),
            memory_node.get_bottom(),
            buff=0.18,
            color=GRAY_A,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )

        arrow_mem_q = Arrow(
            memory_node.get_top(),
            quantum_node.get_left(),
            buff=0.18,
            color=GRAY_A,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )

        loop_group = VGroup(
            quantum_node,
            env_node,
            td_node,
            memory_node,
            arrow_q_env,
            arrow_env_td,
            arrow_td_mem,
            arrow_mem_q
        )

        loop_title = bilingual_text(
            "一次决策循环",
            "One decision loop",
            font_size_cn=24,
            font_size_en=15,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=4.8
        ).move_to(RIGHT * 2.50 + UP * 2.35)

        play_s(FadeIn(loop_title, shift=LEFT), run_time=0.8)

        play_s(
            LaggedStart(
                FadeIn(quantum_node, shift=UP * 0.1),
                GrowArrow(arrow_q_env),
                FadeIn(env_node, shift=RIGHT * 0.1),
                GrowArrow(arrow_env_td),
                FadeIn(td_node, shift=DOWN * 0.1),
                GrowArrow(arrow_td_mem),
                FadeIn(memory_node, shift=LEFT * 0.1),
                GrowArrow(arrow_mem_q),
                lag_ratio=0.20
            ),
            run_time=3.2
        )

        loop_caption = bottom_caption(
            "Quantum module 只替代 action selection，后面的学习仍然是经典 TD",
            "The quantum module replaces only action selection; learning is still classical TD.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, loop_caption), run_time=0.9)
        wait_s(1.3)

        # =========================
        # 4. 第一步：quantum module 选择 action
        # =========================
        q_highlight = SurroundingRectangle(
            quantum_node,
            color=YELLOW,
            buff=0.08,
            stroke_width=4
        )

        quantum_result_box = RoundedRectangle(
            width=3.35,
            height=1.05,
            corner_radius=0.15,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color="#211C0A",
            fill_opacity=0.92
        ).move_to(grid_center + DOWN * 1.40)

        quantum_result_1 = MathTex(
            r"\text{measure} \Rightarrow \lvert 10\rangle",
            font_size=27,
            color=YELLOW
        ).move_to(quantum_result_box.get_center() + UP * 0.18)

        quantum_result_2 = Text(
            "bitstring 10  ->  action = right",
            font=font_en,
            font_size=16,
            color=GRAY_A
        ).next_to(quantum_result_1, DOWN, buff=0.09)

        quantum_result = VGroup(
            quantum_result_box,
            quantum_result_1,
            quantum_result_2
        )

        play_s(Create(q_highlight), run_time=0.8)

        action_caption = bottom_caption(
            "第一步，quantum module 对放大后的量子态 measure，得到一个 action",
            "First, the quantum module measures the amplified quantum state and outputs an action.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, action_caption), run_time=0.9)

        play_s(
            FadeIn(quantum_result, scale=1.05),
            Flash(quantum_node, color=YELLOW, flash_radius=0.45),
            run_time=1.2
        )
        wait_s(1.3)

        # =========================
        # 5. 第二步：env.step 执行动作
        # =========================
        play_s(
            FadeOut(q_highlight),
            Indicate(env_node, color=BLUE_B),
            run_time=0.8
        )

        action_arrow = Arrow(
            start,
            next_state,
            buff=0.16,
            stroke_width=6,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.25
        )

        action_label = Text(
            "right",
            font=font_en,
            font_size=16,
            color=YELLOW
        ).next_to(action_arrow, UP, buff=0.08)

        env_output_box = RoundedRectangle(
            width=3.45,
            height=1.10,
            corner_radius=0.15,
            stroke_color=BLUE_B,
            stroke_width=3,
            fill_color="#111A24",
            fill_opacity=0.92
        ).move_to(grid_center + DOWN * 1.40)

        env_output_1 = Text(
            "next_state = s'",
            font=font_code,
            font_size=17,
            color=BLUE_B
        ).move_to(env_output_box.get_center() + UP * 0.22)

        env_output_2 = Text(
            "reward = +1,  done = False",
            font=font_code,
            font_size=16,
            color=GRAY_A
        ).next_to(env_output_1, DOWN, buff=0.12)

        env_output = VGroup(env_output_box, env_output_1, env_output_2)

        env_caption = bottom_caption(
            "第二步，classical environment 执行 action，并返回 next_state 与 reward",
            "Second, the classical environment executes the action and returns next_state and reward.",
            color_cn=BLUE_B
        )

        play_s(Transform(caption, env_caption), run_time=0.9)

        # Agent 开始移动时删除 Agent 标识，避免 grid 文字重叠
        play_s(
            FadeOut(agent_label),
            GrowArrow(action_arrow),
            FadeIn(action_label),
            agent.animate.move_to(next_state),
            run_time=1.1
        )

        play_s(
            FadeOut(quantum_result),
            FadeIn(env_output, scale=1.05),
            run_time=1.0
        )
        wait_s(1.2)

        # =========================
        # 6. 第三步：TD update
        # =========================
        play_s(
            Indicate(td_node, color=GREEN_B),
            run_time=0.8
        )

        td_formula = MathTex(
            r"V(s)",
            r"\leftarrow",
            r"V(s)",
            r"+",
            r"\alpha",
            r"[",
            r"r+\gamma V(s')-V(s)",
            r"]",
            font_size=32
        ).move_to(RIGHT * 2.55 + DOWN * 2.55)

        td_formula[0].set_color(GREEN_B)
        td_formula[2].set_color(GRAY_A)
        td_formula[4].set_color(YELLOW)
        td_formula[6].set_color(RED_B)

        td_formula_box = SurroundingRectangle(
            td_formula,
            color=GREEN_B,
            buff=0.16,
            stroke_width=2
        )

        td_caption = bottom_caption(
            "第三步，拿到 reward 后，classical TD 开始更新 value",
            "Third, after receiving the reward, classical TD updates the value estimate.",
            color_cn=GREEN_B
        )

        play_s(Transform(caption, td_caption), run_time=0.9)

        play_s(
            FadeIn(td_formula_box),
            Write(td_formula),
            run_time=1.7
        )

        td_error_rect = SurroundingRectangle(
            td_formula[6],
            color=RED_B,
            buff=0.10,
            stroke_width=4
        )

        td_error_label = Text(
            "TD error",
            font=font_en,
            font_size=20,
            color=RED_B
        ).next_to(td_error_rect, UP, buff=0.08)

        play_s(
            Create(td_error_rect),
            FadeIn(td_error_label),
            run_time=0.9
        )
        wait_s(1.1)

        # =========================
        # 7. 具体数值更新
        # =========================
        value_box = RoundedRectangle(
            width=2.35,
            height=1.25,
            corner_radius=0.16,
            stroke_color=GREEN_B,
            stroke_width=3,
            fill_color="#132016",
            fill_opacity=0.92
        ).move_to(grid_center + RIGHT * 0.05 + UP * 1.45)

        value_title = Text(
            "memory[s]",
            font=font_en,
            font_size=18,
            color=GREEN_B
        ).move_to(value_box.get_top() + DOWN * 0.25)

        value_num = DecimalNumber(
            0.30,
            num_decimal_places=2,
            font_size=34,
            color=BLUE_B
        ).move_to(value_box.get_center() + DOWN * 0.12)

        value_group = VGroup(value_box, value_title, value_num)

        play_s(FadeIn(value_group, scale=1.05), run_time=0.9)

        numeric_formula = MathTex(
            r"0.30 + 0.5 \times (1 + 0.9\times 0.50 - 0.30)",
            font_size=25,
            color=GREEN_B
        ).move_to(td_formula)

        play_s(
            Transform(td_formula, numeric_formula),
            FadeOut(td_error_rect),
            FadeOut(td_error_label),
            run_time=1.2
        )

        update_caption = bottom_caption(
            "value 不是一次算完，而是在每次 interaction 后一点点修正",
            "The value is not solved at once; it is corrected step by step after each interaction.",
            color_cn=GREEN_B
        )

        play_s(Transform(caption, update_caption), run_time=0.9)

        play_s(
            value_num.animate.set_value(0.88).set_color(GREEN_B),
            value_box.animate.set_stroke(GREEN_B, width=4),
            run_time=1.8
        )

        play_s(
            Flash(value_box, color=GREEN_B, flash_radius=0.45),
            run_time=0.8
        )
        wait_s(1.4)

        # =========================
        # 8. memory 回流到下一轮 quantum module
        # =========================
        play_s(
            Indicate(memory_node, color=PURPLE_B),
            run_time=0.8
        )

        memory_caption = bottom_caption(
            "更新后的 memory 会影响下一轮 action selection",
            "The updated memory influences the next round of action selection.",
            color_cn=PURPLE_B
        )

        play_s(Transform(caption, memory_caption), run_time=0.9)

        pulse_dot = Dot(
            memory_node.get_center(),
            radius=0.08,
            color=PURPLE_B
        )

        play_s(FadeIn(pulse_dot, scale=1.2), run_time=0.4)

        path_to_q = VMobject()
        path_to_q.set_points_smoothly([
            memory_node.get_top(),
            RIGHT * 1.15 + UP * 0.70,
            quantum_node.get_left()
        ])
        path_to_q.set_color(PURPLE_B)
        path_to_q.set_stroke(width=4)

        play_s(MoveAlongPath(pulse_dot, path_to_q), run_time=1.8)
        play_s(
            Flash(quantum_node, color=PURPLE_B, flash_radius=0.50),
            FadeOut(pulse_dot),
            run_time=0.8
        )
        wait_s(1.0)

        # =========================
        # 9. 代码层面对应关系
        # =========================
        play_s(
            FadeOut(td_formula),
            FadeOut(td_formula_box),
            FadeOut(value_group),
            FadeOut(env_output),
            FadeOut(action_arrow),
            FadeOut(action_label),
            run_time=0.9
        )

        code_lines = [
            "action = quantum_action_selection(state, memory)",
            "next_state, reward, done = env.step(action)",
            "td_error = reward + gamma * V[next_state] - V[state]",
            "V[state] += alpha * td_error",
            "memory[state] = V[state]",
        ]

        loop_code, code_rows, code_bg = code_panel(
            code_lines,
            "hybrid_loop.py",
            color=YELLOW,
            width=7.1,
            height=2.35
        )
        loop_code.move_to(ORIGIN + DOWN * 0.55)

        code_caption = bottom_caption(
            "代码结构也很清楚：quantum 负责选，classical 负责交互和更新",
            "The code structure is clear: quantum selects, classical interacts and updates.",
            color_cn=YELLOW
        )

        play_s(Transform(caption, code_caption), run_time=0.9)
        play_s(FadeIn(loop_code, shift=UP), run_time=1.1)

        h1 = highlight_row(code_rows[0], color=YELLOW)
        h2 = highlight_row(code_rows[1], color=BLUE_B)
        h3 = SurroundingRectangle(
            VGroup(code_rows[2], code_rows[3], code_rows[4]),
            color=GREEN_B,
            buff=0.07,
            stroke_width=3
        )

        play_s(Create(h1), run_time=0.7)
        wait_s(0.4)
        play_s(Create(h2), run_time=0.7)
        wait_s(0.4)
        play_s(Create(h3), run_time=0.9)
        wait_s(1.4)

        # =========================
        # 10. 总结收束，不提问题
        # =========================
        play_s(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)

        summary_box = RoundedRectangle(
            width=9.0,
            height=2.25,
            corner_radius=0.18,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color="#1A1A1A",
            fill_opacity=0.95
        ).move_to(ORIGIN)

        summary_title = Text(
            "Quantum-Classical Loop",
            font=font_en,
            font_size=31,
            color=YELLOW
        ).move_to(summary_box.get_top() + DOWN * 0.42)

        summary_cn_1 = Text(
            "Quantum module：负责更高效的 action selection",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).next_to(summary_title, DOWN, buff=0.28)

        summary_cn_2 = Text(
            "Classical loop：负责 environment interaction 与 TD update",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).next_to(summary_cn_1, DOWN, buff=0.18)

        summary_en = Text(
            "Quantum chooses. Classical learns. Together they form the hybrid RL loop.",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(summary_cn_2, DOWN, buff=0.18)

        summary_group = VGroup(
            summary_box,
            summary_title,
            summary_cn_1,
            summary_cn_2,
            summary_en
        )

        play_s(FadeIn(summary_group, scale=1.03), run_time=1.2)
        wait_s(3.0)