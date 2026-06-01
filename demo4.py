from manim import *
import numpy as np


class SarsaQLearningCompare(Scene):
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
            max_width=7.8
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
                width=max(text_group.width + 0.55, 5.8),
                height=text_group.height + 0.38,
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

        # =========================
        # 基础参数
        # =========================
        cell_size = 0.58
        grid_n = 5
        grid_center = LEFT * 3.55 + DOWN * 0.05

        def cell_pos(row, col):
            x = (col - 2) * cell_size
            y = (2 - row) * cell_size
            return grid_center + np.array([x, y, 0])

        # =========================
        # 1. 标题
        # =========================
        title = bilingual_text(
            "SARSA 到 Q-Learning：实际动作，还是最优动作？",
            "SARSA vs Q-Learning: Actual Action or Best Action?",
            font_size_cn=33,
            font_size_en=20,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.8
        ).to_edge(UP, buff=0.35)

        self.play(FadeIn(title, shift=DOWN), run_time=1.6)
        self.wait(0.7)

        # =========================
        # 2. 构造 Gridworld
        # =========================
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

        s_t = cell_pos(2, 1)
        s_next = cell_pos(2, 2)
        actual_next = cell_pos(3, 2)
        best_next = cell_pos(2, 3)
        goal = cell_pos(4, 4)

        agent = Dot(s_t, radius=0.105, color=BLUE_B)

        # 短标签：直接英文
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
            Text("×", font=font_en, font_size=36, color=RED_B).move_to(actual_next),
            Text("×", font=font_en, font_size=36, color=RED_B).move_to(cell_pos(1, 3)),
            Text("×", font=font_en, font_size=36, color=RED_B).move_to(cell_pos(4, 1)),
        )

        self.play(
            LaggedStart(
                *[FadeIn(s, scale=0.85) for s in grid],
                lag_ratio=0.018
            ),
            run_time=1.8
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
            run_time=1.4
        )

        # =========================
        # 3. 当前一步：从 s_t 到 s_{t+1}
        # =========================
        caption = bottom_caption(
            "先看这一步：Agent 从当前状态走到下一状态",
            "First, the agent moves from the current state to the next state.",
            color_cn=GRAY_A
        )

        self.play(FadeIn(caption, shift=UP), run_time=1.0)
        self.wait(0.4)

        s_t_box = Square(
            side_length=cell_size * 0.95,
            stroke_color=BLUE_B,
            stroke_width=4
        ).move_to(s_t)

        s_t_label = MathTex(
            r"s_t",
            font_size=30,
            color=BLUE_B
        ).next_to(s_t_box, UP, buff=0.08)

        self.play(
            Create(s_t_box),
            FadeIn(s_t_label),
            FadeOut(agent_label),
            run_time=0.8
        )

        first_arrow = Arrow(
            s_t,
            s_next,
            buff=0.18,
            stroke_width=6,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.25
        )

        action_label = MathTex(
            r"a_t",
            font_size=30,
            color=YELLOW
        ).next_to(first_arrow, UP, buff=0.12)

        self.play(
            GrowArrow(first_arrow),
            FadeIn(action_label),
            run_time=0.9
        )

        self.play(
            agent.animate.move_to(s_next),
            run_time=0.85
        )

        s_next_box = Square(
            side_length=cell_size * 0.95,
            stroke_color=GREEN_B,
            stroke_width=4
        ).move_to(s_next)

        s_next_label = MathTex(
            r"s_{t+1}",
            font_size=30,
            color=GREEN_B
        ).next_to(s_next_box, UP, buff=0.08)

        reward_label = MathTex(
            r"r_t",
            font_size=30,
            color=WHITE
        ).next_to(first_arrow, DOWN, buff=0.10)

        self.play(
            Create(s_next_box),
            FadeIn(s_next_label),
            FadeIn(reward_label),
            run_time=0.9
        )
        self.wait(0.7)

        # =========================
        # 4. 右上区域：分岔问题
        # =========================
        right_top_box = RoundedRectangle(
            width=5.15,
            height=1.35,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#181818",
            fill_opacity=0.88
        ).move_to(RIGHT * 2.45 + UP * 1.75)

        branch_question = bilingual_text(
            "关键分岔：下一步的价值应该看谁？",
            "Which next action should be used for backup?",
            font_size_cn=24,
            font_size_en=15,
            color_cn=YELLOW,
            color_en=GRAY_B,
            max_width=4.75
        ).move_to(right_top_box.get_center())

        self.play(
            FadeOut(caption),
            FadeIn(right_top_box, shift=LEFT),
            FadeIn(branch_question, shift=LEFT),
            FadeOut(first_arrow),
            FadeOut(action_label),
            FadeOut(reward_label),
            run_time=1.0
        )
        self.wait(0.5)

        # 实际动作：探索导致向下
        actual_arrow = Arrow(
            s_next,
            actual_next,
            buff=0.18,
            stroke_width=6,
            color=RED_B,
            max_tip_length_to_length_ratio=0.25
        )

        actual_label = Text(
            "actual action",
            font=font_en,
            font_size=18,
            color=RED_B
        ).next_to(actual_arrow, LEFT, buff=0.10)

        actual_q = MathTex(
            r"Q=-0.8",
            font_size=25,
            color=RED_B
        ).next_to(actual_label, DOWN, buff=0.15)

        self.play(
            GrowArrow(actual_arrow),
            FadeIn(actual_label),
            FadeIn(actual_q),
            FadeOut(s_t_box),
            FadeOut(s_t_label),
            FadeOut(s_next_box),
            FadeOut(s_next_label),
            run_time=1.2
        )
        self.wait(0.4)

        warning = bottom_caption(
            "训练时会探索，所以 actual action 不一定最好",
            "Exploration may choose a risky action.",
            color_cn=RED_B
        )

        self.play(
            FadeIn(warning, shift=UP),
            Indicate(traps[0], color=RED_B),
            run_time=1.2
        )
        self.wait(0.8)

        # 最优动作：当前估计下最好的动作
        best_arrow = Arrow(
            s_next,
            best_next,
            buff=0.18,
            stroke_width=6,
            color=GREEN_B,
            max_tip_length_to_length_ratio=0.25
        )

        best_q = MathTex(
            r"Q=0.9",
            font_size=25,
            color=GREEN_B
        ).next_to(best_arrow, UP, buff=0.10)

        best_label = Text(
            "best action",
            font=font_en,
            font_size=18,
            color=GREEN_B
        ).next_to(best_q, UP, buff=0.15)

        self.play(
            GrowArrow(best_arrow),
            FadeIn(best_label),
            FadeIn(best_q),
            run_time=1.2
        )
        self.wait(0.7)

        self.play(FadeOut(warning), run_time=0.5)

        # =========================
        # 5. 右下区域：SARSA 公式
        # =========================
        formula_panel = RoundedRectangle(
            width=6.25,
            height=2.35,
            corner_radius=0.16,
            stroke_color=RED_B,
            stroke_width=3,
            fill_color="#151515",
            fill_opacity=0.93
        ).move_to(RIGHT * 2.45 + DOWN * 1.45)

        sarsa_title = bilingual_text(
            "SARSA：按照 actual action 来学习",
            "On-policy: learn from the actual next action",
            font_size_cn=23,
            font_size_en=15,
            color_cn=RED_B,
            color_en=GRAY_B,
            max_width=5.75
        ).move_to(formula_panel.get_top() + DOWN * 0.43)

        sarsa_formula = MathTex(
            r"Q(s_t,a_t)",
            r"\leftarrow",
            r"Q(s_t,a_t)",
            r"+\alpha[",
            r"r_t+\gamma Q(s_{t+1},a_{t+1})",
            r"-Q(s_t,a_t)]",
            font_size=28
        )

        sarsa_formula[0].set_color(BLUE_B)
        sarsa_formula[4].set_color(RED_B)

        if sarsa_formula.width > formula_panel.width - 0.45:
            sarsa_formula.scale_to_fit_width(formula_panel.width - 0.45)

        sarsa_formula.move_to(formula_panel.get_center() + DOWN * 0.02)

        sarsa_note = bilingual_text(
            "备份目标使用真实发生的下一步动作",
            "It backs up the action actually taken.",
            font_size_cn=19,
            font_size_en=13,
            color_cn=RED_B,
            color_en=GRAY_B,
            max_width=5.65
        ).move_to(formula_panel.get_bottom() + UP * 0.34)

        self.play(
            FadeIn(formula_panel),
            FadeIn(sarsa_title),
            run_time=0.9
        )

        self.play(Write(sarsa_formula), run_time=2.0)

        sarsa_highlight = SurroundingRectangle(
            sarsa_formula[4],
            color=RED_B,
            buff=0.08,
            stroke_width=4
        )

        self.play(Create(sarsa_highlight), FadeIn(sarsa_note), run_time=1.0)
        self.wait(1.2)

        # =========================
        # 6. SARSA 的保守性
        # =========================
        actual_path_glow = SurroundingRectangle(
            VGroup(actual_arrow, actual_label, actual_q),
            color=RED_B,
            buff=0.12,
            stroke_width=3
        )

        conservative = bottom_caption(
            "所以 SARSA 会把“未来可能探索犯错”也计算进去",
            "SARSA is cautious because it accounts for exploration mistakes.",
            color_cn=RED_B
        )

        self.play(
            Create(actual_path_glow),
            FadeIn(conservative, shift=UP),
            run_time=1.1
        )
        self.wait(1.8)

        # =========================
        # 7. On-policy 图示
        # =========================
        policy_box = RoundedRectangle(
            width=5.15,
            height=1.45,
            corner_radius=0.16,
            stroke_color=RED_B,
            stroke_width=2,
            fill_color="#1A1A1A",
            fill_opacity=0.9
        ).move_to(RIGHT * 2.45 + UP * 1.55)

        behavior_label = Text(
            "behavior policy",
            font=font_en,
            font_size=16,
            color=RED_B
        ).move_to(policy_box.get_center() + LEFT * 1.25 + UP * 0.22)

        target_label = Text(
            "target policy",
            font=font_en,
            font_size=16,
            color=RED_B
        ).move_to(policy_box.get_center() + RIGHT * 1.25 + UP * 0.22)

        equal_sign = MathTex(
            r"=",
            font_size=36,
            color=WHITE
        ).move_to(policy_box.get_center() + UP * 0.20)

        on_policy_text = bilingual_text(
            "On-policy：怎么走，就怎么学",
            "Learn the same policy that generates behavior.",
            font_size_cn=19,
            font_size_en=12,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=4.65
        ).move_to(policy_box.get_center() + DOWN * 0.38)

        policy_group = VGroup(
            policy_box,
            behavior_label,
            target_label,
            equal_sign,
            on_policy_text
        )

        self.play(
            FadeOut(right_top_box),
            FadeOut(branch_question),
            FadeIn(policy_group, shift=LEFT),
            run_time=1.2
        )
        self.wait(1.6)

        # =========================
        # 8. Q-Learning：替换一项
        # =========================
        switch_tip = bottom_caption(
            "Q-Learning 只改了一个地方",
            "Q-Learning changes just one term.",
            color_cn=YELLOW
        )

        self.play(
            FadeOut(conservative),
            FadeOut(actual_path_glow),
            FadeOut(policy_group),
            FadeIn(switch_tip, shift=UP),
            run_time=1.1
        )
        self.wait(0.6)

        term_box = RoundedRectangle(
            width=5.15,
            height=1.75,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#181818",
            fill_opacity=0.9
        ).move_to(RIGHT * 2.45 + UP * 1.45)

        old_term = MathTex(
            r"Q(s_{t+1},a_{t+1})",
            font_size=38,
            color=RED_B
        ).move_to(term_box.get_center() + UP * 0.27)

        term_arrow = MathTex(
            r"\Longrightarrow",
            font_size=34,
            color=YELLOW
        ).move_to(term_box.get_center() + DOWN * 0.08)

        new_term = MathTex(
            r"\max_a Q(s_{t+1},a)",
            font_size=38,
            color=GREEN_B
        ).move_to(old_term)

        transform_label = Text(
            "use best action",
            font=font_en,
            font_size=17,
            color=GREEN_B
        ).move_to(term_box.get_center() + DOWN * 0.55)

        self.play(FadeIn(term_box), FadeIn(old_term, scale=1.08), run_time=0.9)
        self.wait(0.4)
        self.play(FadeIn(term_arrow), run_time=0.5)
        self.play(
            ReplacementTransform(old_term, new_term),
            FadeIn(transform_label, shift=UP),
            run_time=1.3
        )
        self.wait(1.2)

        # =========================
        # 9. 换成 Q-Learning 公式
        # =========================
        q_title = bilingual_text(
            "Q-Learning：朝着 best action 学习",
            "Off-policy: learn toward the greedy action",
            font_size_cn=23,
            font_size_en=15,
            color_cn=GREEN_B,
            color_en=GRAY_B,
            max_width=5.75
        ).move_to(sarsa_title)

        q_formula = MathTex(
            r"Q(s_t,a_t)",
            r"\leftarrow",
            r"Q(s_t,a_t)",
            r"+\alpha[",
            r"r_t+\gamma \max_a Q(s_{t+1},a)",
            r"-Q(s_t,a_t)]",
            font_size=28
        )

        q_formula[0].set_color(BLUE_B)
        q_formula[4].set_color(GREEN_B)

        if q_formula.width > formula_panel.width - 0.45:
            q_formula.scale_to_fit_width(formula_panel.width - 0.45)

        q_formula.move_to(sarsa_formula)

        q_note = bilingual_text(
            "备份目标使用下一状态下最大的动作价值",
            "It backs up the maximum action value.",
            font_size_cn=19,
            font_size_en=13,
            color_cn=GREEN_B,
            color_en=GRAY_B,
            max_width=5.65
        ).move_to(sarsa_note)

        self.play(
            FadeOut(term_box),
            FadeOut(new_term),
            FadeOut(term_arrow),
            FadeOut(transform_label),
            FadeOut(sarsa_title),
            FadeOut(sarsa_formula),
            FadeOut(sarsa_highlight),
            FadeOut(sarsa_note),
            FadeIn(q_title),
            formula_panel.animate.set_stroke(color=GREEN_B, width=3),
            run_time=1.1
        )

        self.play(Write(q_formula), run_time=2.0)

        q_highlight = SurroundingRectangle(
            q_formula[4],
            color=GREEN_B,
            buff=0.08,
            stroke_width=4
        )

        self.play(Create(q_highlight), FadeIn(q_note), run_time=1.0)
        self.wait(1.3)

        # =========================
        # 10. Q-Learning 的贪心目标
        # =========================
        best_path_glow = SurroundingRectangle(
            VGroup(best_arrow, best_label, best_q),
            color=GREEN_B,
            buff=0.12,
            stroke_width=3
        )

        greedy_caption = bottom_caption(
            "所以 Q-Learning 更贪心：它总是假设下一步会选 best action",
            "Q-Learning is greedy in its learning target.",
            color_cn=GREEN_B
        )

        self.play(
            FadeOut(switch_tip),
            FadeOut(actual_arrow),
            FadeOut(actual_label),
            FadeOut(actual_q),
            Create(best_path_glow),
            FadeIn(greedy_caption, shift=UP),
            run_time=1.1
        )
        self.wait(1.8)

        # =========================
        # 11. Off-policy 图示
        # =========================
        off_policy_box = RoundedRectangle(
            width=5.15,
            height=1.48,
            corner_radius=0.16,
            stroke_color=GREEN_B,
            stroke_width=2,
            fill_color="#1A1A1A",
            fill_opacity=0.9
        ).move_to(RIGHT * 2.45 + UP * 1.55)

        explore_label = Text(
            "explore policy",
            font=font_en,
            font_size=16,
            color=YELLOW
        ).move_to(off_policy_box.get_center() + LEFT * 1.25 + UP * 0.24)

        greedy_label = Text(
            "greedy policy",
            font=font_en,
            font_size=16,
            color=GREEN_B
        ).move_to(off_policy_box.get_center() + RIGHT * 1.25 + UP * 0.24)

        not_equal = MathTex(
            r"\ne",
            font_size=36,
            color=WHITE
        ).move_to(off_policy_box.get_center() + UP * 0.22)

        off_policy_text = bilingual_text(
            "Off-policy：一边探索，一边学习最优目标",
            "Behave with exploration, learn the greedy target.",
            font_size_cn=18,
            font_size_en=12,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=4.75
        ).move_to(off_policy_box.get_center() + DOWN * 0.40)

        off_policy_group = VGroup(
            off_policy_box,
            explore_label,
            greedy_label,
            not_equal,
            off_policy_text
        )

        self.play(FadeIn(off_policy_group, shift=LEFT), run_time=1.2)
        self.wait(1.8)

        # =========================
        # 12. 总结对比
        # =========================
        compare_box = RoundedRectangle(
            width=7.8,
            height=1.1,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#222222",
            fill_opacity=0.96
        ).to_edge(DOWN, buff=0.18)

        compare_cn = Text(
            "SARSA更保守；Q-Learning更接近最优目标",
            font=font_cn,
            font_size=22,
            color=RED_B
        )

        compare_en = Text(
            "The difference is only one term, but the learning behavior changes.",
            font=font_en,
            font_size=15,
            color=GRAY_B
        ).next_to(compare_cn, DOWN, buff=0.08)

        compare_text = VGroup(compare_cn, compare_en)
        compare_text.move_to(compare_box.get_center())
        compare_group = VGroup(compare_box, compare_text)

        self.play(
            FadeOut(greedy_caption),
            FadeIn(compare_group, shift=UP),
            run_time=1.2
        )
        self.wait(2.2)

        # =========================
        # 13. 为下一段：经典算法痛点铺垫
        # 按你的要求：先清空所有对象，再居中显示问题
        # =========================
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)

        next_hint_cn = Text(
            "但如果动作空间巨大，best action 真的容易找到吗？",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "But if the action space is huge, can we still find the best action easily?",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        self.play(FadeIn(next_hint, shift=UP), run_time=1.1)
        self.wait(2.2)