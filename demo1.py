from manim import *
import numpy as np


class OpeningGridworld(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 基础参数
        # =========================
        cell_size = 0.75
        grid_n = 5
        grid_origin = ORIGIN

        def cell_pos(row, col):
            """
            row, col 从 0 开始
            row=0 是第一行，col=0 是第一列
            """
            x = (col - 2) * cell_size
            y = (2 - row) * cell_size
            return np.array([x, y, 0])

        # =========================
        # 1. 标题淡入
        # =========================
        title = Text(
            "一个小智能体，如何学会走出迷宫？",
            font="SimSun",
            font_size=36,
            color=WHITE
        ).to_edge(UP)

        subtitle = Text(
            "From trial-and-error to quantum search",
            font_size=24,
            color=GRAY_B
        ).next_to(title, DOWN, buff=0.15)

        self.play(FadeIn(title, shift=DOWN), FadeIn(subtitle, shift=DOWN), run_time=1.5)
        self.wait(1.5)

        # =========================
        # 2. 构造 5x5 网格
        # =========================
        grid = VGroup()

        for r in range(grid_n):
            for c in range(grid_n):
                square = Square(
                    side_length=cell_size,
                    stroke_color=GRAY_B,
                    stroke_width=2,
                    fill_color="#1E1E1E",
                    fill_opacity=0.65
                )
                square.move_to(cell_pos(r, c))
                grid.add(square)

        grid.shift(DOWN * 0.25)

        self.play(
            LaggedStart(
                *[FadeIn(cell, scale=0.8) for cell in grid],
                lag_ratio=0.03
            ),
            run_time=2
        )

        # =========================
        # 3. 起点智能体、终点、陷阱
        # =========================
        agent_start = cell_pos(0, 0) + DOWN * 0.25
        target_pos = cell_pos(4, 4) + DOWN * 0.25

        agent = Dot(
            point=agent_start,
            radius=0.12,
            color=BLUE
        )

        agent_label = Text(
            "Agent",
            font_size=20,
            color=BLUE
        ).next_to(agent, UP, buff=0.12)

        target = Star(
            n=5,
            outer_radius=0.22,
            inner_radius=0.10,
            color=YELLOW,
            fill_opacity=1
        ).move_to(target_pos)

        target_glow = Circle(
            radius=0.35,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=YELLOW,
            fill_opacity=0.15
        ).move_to(target_pos)

        target_label = Text(
            "Goal",
            font_size=20,
            color=YELLOW
        ).next_to(target, DOWN, buff=0.12)

        trap_cells = [(0, 4), (1, 1), (2, 0), (3, 4), (1, 4)]
        traps = VGroup()

        for r, c in trap_cells:
            trap = Square(
                side_length=cell_size * 0.72,
                stroke_width=0,
                fill_color=RED,
                fill_opacity=1
            ).move_to(cell_pos(r, c) + DOWN * 0.25)
            traps.add(trap)

        self.play(
            FadeIn(agent, scale=1.3),
            FadeIn(agent_label),
            FadeIn(target_glow, scale=1.6),
            FadeIn(target, scale=1.3),
            FadeIn(target_label),
            run_time=1.5
        )

        self.play(
            LaggedStart(
                *[FadeIn(trap, scale=1.5) for trap in traps],
                lag_ratio=0.2
            ),
            run_time=1.3
        )

        self.wait(1.5)

        # =========================
        # 4. 四个动作箭头
        # =========================
        arrow_color = TEAL_A

        left_arrow = Arrow(
            agent.get_center(),
            agent.get_center() + LEFT * 0.55,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )
        up_arrow = Arrow(
            agent.get_center(),
            agent.get_center() + UP * 0.55,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )
        right_arrow = Arrow(
            agent.get_center(),
            agent.get_center() + RIGHT * 0.55,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )
        down_arrow = Arrow(
            agent.get_center(),
            agent.get_center() + DOWN * 0.55,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )

        action_arrows = VGroup(left_arrow, up_arrow, right_arrow, down_arrow)

        action_text = Text(
            "每一步，只能从四个动作中选择一个",
            font="SimSun",
            font_size=28,
            color=WHITE
        ).next_to(grid, DOWN, buff=0.55)

        self.play(
            LaggedStart(
                GrowArrow(left_arrow),
                GrowArrow(up_arrow),
                GrowArrow(right_arrow),
                GrowArrow(down_arrow),
                lag_ratio=0.18
            ),
            FadeIn(action_text, shift=UP),
            run_time=2.2
        )

        self.wait(1)

        # =========================
        # 5. 简单试错路径
        # =========================
        trial_path = [
            cell_pos(0, 1) + DOWN * 0.25,
            cell_pos(1, 1) + DOWN * 0.25,
            cell_pos(1, 0) + DOWN * 0.25,
            cell_pos(2, 0) + DOWN * 0.25,
        ]

        reward_bad = Text(
            "reward = -10",
            font_size=26,
            color=RED
        ).next_to(grid, RIGHT, buff=0.6)

        trial_text = Text(
            "它只能试错：走一步，得到反馈，再修正判断",
            font="SimSun",
            font_size=28,
            color=GRAY_A
        ).move_to(action_text)

        self.play(
            Transform(action_text, trial_text),
            FadeOut(action_arrows),
            run_time=1
        )

        for i, p in enumerate(trial_path):
            self.play(
                agent.animate.move_to(p),
                agent_label.animate.next_to(agent, UP, buff=0.12),
                run_time=0.55
            )

            if i == 1:
                self.play(FadeIn(reward_bad, shift=LEFT), run_time=0.4)
                self.play(Indicate(traps[0], color=RED), run_time=0.6)
                self.play(FadeOut(reward_bad), run_time=0.4)

        self.wait(1)

        # =========================
        # 6. 动作空间从小变大
        # =========================
        big_question = Text(
            "如果动作不是 4 个，而是 40000 个呢？",
            font="SimSun",
            font_size=36,
            color=WHITE
        ).to_edge(UP)

        self.play(
            Transform(title, big_question),
            FadeOut(subtitle),
            FadeOut(action_text),
            run_time=1
        )

        # 镜头拉远
        self.play(
            self.camera.frame.animate.scale(1.25).shift(RIGHT * 1.3),
            run_time=1.5
        )

        # 右侧制造大量候选动作点
        candidate_dots = VGroup()
        np.random.seed(2)

        for _ in range(90):
            x = np.random.uniform(1.7, 5.8)
            y = np.random.uniform(-2.3, 1.9)
            dot = Dot(
                point=np.array([x, y, 0]),
                radius=0.035,
                color=GRAY_B
            )
            candidate_dots.add(dot)

        chosen_dot = Dot(
            point=np.array([4.8, 0.6, 0]),
            radius=0.07,
            color=YELLOW
        )

        search_label = Text(
            "巨大的动作空间",
            font="SimSun",
            font_size=28,
            color=GRAY_A
        ).next_to(candidate_dots, UP, buff=0.35)

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.4) for dot in candidate_dots],
                lag_ratio=0.01
            ),
            FadeIn(search_label),
            run_time=2
        )

        self.play(
            FadeIn(chosen_dot, scale=2),
            Flash(chosen_dot, color=YELLOW, flash_radius=0.45),
            run_time=1
        )

        # =========================
        # 7. 引出核心问题
        # =========================
        classical_text = MathTex(
            r"\text{Classical search: } O(N)",
            font_size=34,
            color=RED_B
        ).next_to(candidate_dots, DOWN, buff=0.4)

        quantum_hint = MathTex(
            r"\text{Grover search: } O(\sqrt{N})",
            font_size=34,
            color=BLUE_B
        ).next_to(classical_text, DOWN, buff=0.25)


        self.play(Write(classical_text), run_time=1)
        self.wait(0.3)
        self.play(Write(quantum_hint), run_time=1)

        self.wait(2)