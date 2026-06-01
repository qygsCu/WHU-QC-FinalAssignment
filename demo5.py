from manim import *
import numpy as np


class ClassicalBottleneck(Scene):
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

        def make_flow_box(label, color, width=1.72):
            box = RoundedRectangle(
                width=width,
                height=0.68,
                corner_radius=0.12,
                stroke_color=color,
                stroke_width=2,
                fill_color="#1A1A1A",
                fill_opacity=0.9
            )
            text = Text(
                label,
                font=font_en,
                font_size=17,
                color=color
            ).move_to(box.get_center())

            return VGroup(box, text)

        # =========================
        # 1. 标题
        # =========================
        title = bilingual_text(
            "经典算法的痛点：动作选择",
            "The Bottleneck of Classical RL: Action Selection",
            font_size_cn=36,
            font_size_en=21,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.5
        ).to_edge(UP, buff=0.35)

        self.play(FadeIn(title, shift=DOWN), run_time=1.5)
        self.wait(0.6)

        # =========================
        # 2. 左侧 Gridworld
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
        agent = Dot(agent_pos, radius=0.11, color=BLUE_B)

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
            "前面的算法都离不开一个步骤：先选一个 action",
            "Every previous method still needs to select an action first.",
            color_cn=GRAY_A
        )

        self.play(FadeIn(caption, shift=UP), run_time=1.0)
        self.wait(0.7)

        # =========================
        # 3. 四个动作：小动作空间很容易比较
        # =========================
        self.play(FadeOut(agent_label), run_time=0.35)
        arrow_len = 0.56
        arrow_color = TEAL_A

        left_arrow = Arrow(
            agent_pos,
            agent_pos + LEFT * arrow_len,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )
        up_arrow = Arrow(
            agent_pos,
            agent_pos + UP * arrow_len,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )
        right_arrow = Arrow(
            agent_pos,
            agent_pos + RIGHT * arrow_len,
            buff=0.15,
            color=GREEN_B,
            stroke_width=5
        )
        down_arrow = Arrow(
            agent_pos,
            agent_pos + DOWN * arrow_len,
            buff=0.15,
            color=arrow_color,
            stroke_width=5
        )

        action_arrows = VGroup(left_arrow, up_arrow, right_arrow, down_arrow)

        labels = VGroup(
            Text("left", font=font_en, font_size=14, color=arrow_color).next_to(left_arrow, LEFT, buff=0.06),
            Text("up", font=font_en, font_size=14, color=arrow_color).next_to(up_arrow, UP, buff=0.06),
            Text("right", font=font_en, font_size=14, color=GREEN_B).next_to(right_arrow, RIGHT, buff=0.06),
            Text("down", font=font_en, font_size=14, color=arrow_color).next_to(down_arrow, DOWN, buff=0.06),
        )

        q_values = VGroup(
            MathTex(r"0.2", font_size=22, color=GRAY_A).next_to(left_arrow, DOWN, buff=0.04),
            MathTex(r"0.4", font_size=22, color=GRAY_A).next_to(up_arrow, LEFT, buff=0.04),
            MathTex(r"0.9", font_size=24, color=GREEN_B).next_to(right_arrow, UP, buff=0.04),
            MathTex(r"-0.3", font_size=22, color=GRAY_A).next_to(down_arrow, RIGHT, buff=0.04),
        )

        self.play(
            LaggedStart(
                GrowArrow(left_arrow),
                GrowArrow(up_arrow),
                GrowArrow(right_arrow),
                GrowArrow(down_arrow),
                lag_ratio=0.15
            ),
            run_time=1.6
        )

        self.play(FadeIn(labels), FadeIn(q_values), run_time=0.9)

        small_caption = bottom_caption(
            "如果只有四个动作，比较 Q 值并不困难",
            "With only four actions, comparing Q-values is easy.",
            color_cn=GREEN_B
        )

        self.play(Transform(caption, small_caption), run_time=0.8)

        best_box = SurroundingRectangle(
            VGroup(right_arrow, labels[2], q_values[2]),
            color=GREEN_B,
            buff=0.12,
            stroke_width=3
        )

        self.play(Create(best_box), run_time=0.9)
        self.wait(1.2)

        # =========================
        # 4. 右侧流程：经典强化学习闭环
        # =========================
        flow_panel = RoundedRectangle(
            width=5.25,
            height=2.25,
            corner_radius=0.16,
            stroke_color=GRAY_B,
            stroke_width=2,
            fill_color="#171717",
            fill_opacity=0.9
        ).move_to(RIGHT * 2.35 + UP * 0.85)

        flow_title = bilingual_text(
            "经典强化学习闭环",
            "Classical RL loop",
            font_size_cn=23,
            font_size_en=15,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=4.8
        ).move_to(flow_panel.get_top() + DOWN * 0.38)

        select_box = make_flow_box("select action", YELLOW, width=1.85)
        env_box = make_flow_box("env.step", BLUE_B, width=1.65)
        update_box = make_flow_box("TD update", GREEN_B, width=1.75)

        flow_boxes = VGroup(select_box, env_box, update_box).arrange(RIGHT, buff=0.30)
        flow_boxes.move_to(flow_panel.get_center() + DOWN * 0.25)

        flow_arrow_1 = Arrow(
            select_box.get_right(),
            env_box.get_left(),
            buff=0.08,
            color=GRAY_A,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25
        )

        flow_arrow_2 = Arrow(
            env_box.get_right(),
            update_box.get_left(),
            buff=0.08,
            color=GRAY_A,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.25
        )

        flow_group = VGroup(
            flow_panel,
            flow_title,
            flow_boxes,
            flow_arrow_1,
            flow_arrow_2
        )

        self.play(FadeIn(flow_panel), FadeIn(flow_title), run_time=0.9)
        self.play(
            LaggedStart(
                FadeIn(select_box, shift=UP * 0.1),
                GrowArrow(flow_arrow_1),
                FadeIn(env_box, shift=UP * 0.1),
                GrowArrow(flow_arrow_2),
                FadeIn(update_box, shift=UP * 0.1),
                lag_ratio=0.25
            ),
            run_time=2.0
        )

        select_highlight = SurroundingRectangle(
            select_box,
            color=YELLOW,
            buff=0.06,
            stroke_width=4
        )

        bottleneck_caption = bottom_caption(
            "瓶颈恰恰出现在第一步：select action",
            "The bottleneck appears at the very first step: select action.",
            color_cn=YELLOW
        )

        self.play(
            Transform(caption, bottleneck_caption),
            Create(select_highlight),
            run_time=1.0
        )
        self.wait(1.4)

        # =========================
        # 5. 动作空间膨胀
        # =========================
        big_action_caption = bottom_caption(
            "当 action space 变大，逐个比较就会越来越慢",
            "As the action space grows, one-by-one comparison becomes slow.",
            color_cn=RED_B
        )

        self.play(Transform(caption, big_action_caption), run_time=0.8)

        # 从 4 个箭头扩展出很多方向
        np.random.seed(7)
        many_arrows = VGroup()

        for i in range(28):
            angle = 2 * np.pi * i / 28
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            length = np.random.uniform(0.45, 0.82)
            color = GRAY_B

            arrow = Arrow(
                agent_pos,
                agent_pos + direction * length,
                buff=0.16,
                color=color,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.22
            )
            arrow.set_opacity(0.55)
            many_arrows.add(arrow)

        self.play(
            FadeOut(best_box),
            FadeOut(q_values),
            FadeOut(labels),
            LaggedStart(
                *[GrowArrow(a) for a in many_arrows],
                lag_ratio=0.025
            ),
            run_time=1.7
        )
        self.wait(0.8)

        # =========================
        # 6. 清出空间，进入 N actions 搜索场景
        # =========================
        self.play(
            FadeOut(grid),
            FadeOut(agent),
            FadeOut(goal_star),
            FadeOut(goal_glow),
            FadeOut(traps),
            FadeOut(action_arrows),
            FadeOut(many_arrows),
            FadeOut(flow_group),
            FadeOut(select_highlight),
            FadeOut(caption),
            run_time=1.0
        )

        new_title = bilingual_text(
            "动作选择，本质上像一个搜索问题",
            "Action selection is essentially a search problem",
            font_size_cn=35,
            font_size_en=20,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.5
        ).to_edge(UP, buff=0.35)

        self.play(Transform(title, new_title), run_time=1.0)

        # =========================
        # 7. 左侧：小动作空间；右侧：大动作空间
        # =========================
        small_box = RoundedRectangle(
            width=3.15,
            height=2.55,
            corner_radius=0.18,
            stroke_color=GREEN_B,
            stroke_width=2,
            fill_color="#171717",
            fill_opacity=0.9
        ).move_to(LEFT * 3.1 + DOWN * 0.1)

        large_box = RoundedRectangle(
            width=5.85,
            height=3.65,
            corner_radius=0.18,
            stroke_color=RED_B,
            stroke_width=2,
            fill_color="#171717",
            fill_opacity=0.9
        ).move_to(RIGHT * 2.05 + DOWN * 0.05)

        small_title = Text(
            "4 actions",
            font=font_en,
            font_size=24,
            color=GREEN_B
        ).move_to(small_box.get_top() + DOWN * 0.35)

        large_title = Text(
            "N actions",
            font=font_en,
            font_size=25,
            color=RED_B
        ).move_to(large_box.get_top() + DOWN * 0.35)

        self.play(
            FadeIn(small_box),
            FadeIn(large_box),
            FadeIn(small_title),
            FadeIn(large_title),
            run_time=1.0
        )

        small_dots = VGroup()
        small_positions = [
            small_box.get_center() + LEFT * 0.55 + UP * 0.15,
            small_box.get_center() + RIGHT * 0.55 + UP * 0.15,
            small_box.get_center() + LEFT * 0.55 + DOWN * 0.55,
            small_box.get_center() + RIGHT * 0.55 + DOWN * 0.55,
        ]

        for i, p in enumerate(small_positions):
            color = GREEN_B if i == 1 else GRAY_B
            dot = Dot(p, radius=0.09, color=color)
            small_dots.add(dot)

        best_small_label = Text(
            "best action",
            font=font_en,
            font_size=16,
            color=GREEN_B
        ).next_to(small_dots[1], UP, buff=0.10)

        # 大动作空间点云
        candidate_dots = VGroup()
        candidate_positions = []
        best_index = 63

        np.random.seed(3)
        for i in range(96):
            x = np.random.uniform(
                large_box.get_left()[0] + 0.35,
                large_box.get_right()[0] - 0.35
            )
            y = np.random.uniform(
                large_box.get_bottom()[1] + 0.35,
                large_box.get_top()[1] - 0.65
            )
            pos = np.array([x, y, 0])
            candidate_positions.append(pos)

            color = YELLOW if i == best_index else GRAY_B
            radius = 0.075 if i == best_index else 0.035
            dot = Dot(pos, radius=radius, color=color)
            if i != best_index:
                dot.set_opacity(0.72)
            candidate_dots.add(dot)

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.7) for dot in small_dots],
                lag_ratio=0.15
            ),
            FadeIn(best_small_label),
            run_time=1.1
        )

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.5) for dot in candidate_dots],
                lag_ratio=0.006
            ),
            run_time=2.0
        )

        search_caption = bottom_caption(
            "如果只能逐个检查，找到 best action 的代价会随着 N 增长",
            "If we check actions one by one, the cost grows with N.",
            color_cn=RED_B
        )

        self.play(FadeIn(search_caption, shift=UP), run_time=1.0)
        self.wait(0.6)

        # =========================
        # 8. 经典搜索：一个一个试
        # =========================
        search_cursor = Circle(
            radius=0.13,
            stroke_color=RED_B,
            stroke_width=4
        ).move_to(candidate_positions[0])

        try_text = Text(
            "try one by one",
            font=font_en,
            font_size=18,
            color=RED_B
        ).next_to(large_box, DOWN, buff=0.18)

        self.play(FadeIn(search_cursor), FadeIn(try_text), run_time=0.7)

        scan_indices = [0, 8, 16, 25, 33, 42, 55, best_index]
        for idx in scan_indices:
            self.play(
                search_cursor.animate.move_to(candidate_positions[idx]),
                run_time=0.32
            )

        self.play(
            Flash(candidate_dots[best_index], color=YELLOW, flash_radius=0.40),
            candidate_dots[best_index].animate.scale(1.35),
            run_time=0.8
        )
        self.wait(0.6)

        # =========================
        # 9. 复杂度 O(N)
        # =========================
        complexity_box = RoundedRectangle(
            width=4.2,
            height=1.35,
            corner_radius=0.16,
            stroke_color=RED_B,
            stroke_width=3,
            fill_color="#1A1A1A",
            fill_opacity=0.94
        ).move_to(RIGHT * 2.05 + DOWN * 2.45)

        classical_complexity = MathTex(
            r"\text{Classical search: } O(N)",
            font_size=32,
            color=RED_B
        ).move_to(complexity_box.get_center() + UP * 0.18)

        complexity_note = Text(
            "linear growth",
            font=font_en,
            font_size=16,
            color=GRAY_B
        ).next_to(classical_complexity, DOWN, buff=0.10)

        self.play(
            FadeIn(complexity_box, shift=UP),
            Write(classical_complexity),
            FadeIn(complexity_note),
            run_time=1.2
        )

        red_cross = Cross(
            complexity_box,
            stroke_color=RED_B,
            stroke_width=5
        )

        self.play(Create(red_cross), run_time=0.8)
        self.wait(0.8)

        pain_caption = bottom_caption(
            "这就是经典探索的痛点：动作空间越大，搜索越慢",
            "This is the pain point: larger action spaces make exploration slower.",
            color_cn=RED_B
        )

        self.play(
            Transform(search_caption, pain_caption),
            FadeOut(complexity_box),
            FadeOut(classical_complexity),
            FadeOut(complexity_note),
            FadeOut(red_cross),
            run_time=0.9
        )
        self.wait(1.4)

        # =========================
        # 10. 引出量子叠加与 Grover
        # =========================
        grover_hint_box = RoundedRectangle(
            width=7.9,
            height=1.35,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#222222",
            fill_opacity=0.96
        ).to_edge(DOWN, buff=0.18)

        grover_hint_cn = Text(
            "能不能不要逐个试，而是先把所有 action 同时摆上舞台？",
            font=font_cn,
            font_size=24,
            color=YELLOW
        )

        grover_hint_en = Text(
            "Can we place all actions on the stage before measuring one?",
            font=font_en,
            font_size=16,
            color=GRAY_B
        ).next_to(grover_hint_cn, DOWN, buff=0.07)

        grover_hint_text = VGroup(grover_hint_cn, grover_hint_en)
        grover_hint_text.scale_to_fit_width(7.35)
        grover_hint_text.move_to(grover_hint_box.get_center())

        grover_hint = VGroup(grover_hint_box, grover_hint_text)

        self.play(
            FadeOut(search_caption),
            FadeIn(grover_hint, shift=UP),
            run_time=1.1
        )
        self.wait(1.4)

        # 按前面形式：清屏后居中引出下一段
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)

        next_hint_cn = Text(
            "如果所有 action 可以同时处于叠加态，会发生什么？",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "What if all actions could exist in superposition at once?",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        self.play(FadeIn(next_hint, shift=UP), run_time=1.1)
        self.wait(2.2)