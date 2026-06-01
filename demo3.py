from manim import *
import numpy as np


class TDLearningIntro(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 全局字体
        # =========================
        font_cn = "SimSun"     # 宋体；如果不显示，可以改成 "宋体"
        font_en = "Times New Roman"

        # =========================
        # 基础参数
        # =========================
        cell_size = 0.62
        grid_n = 5
        grid_center = LEFT * 3.25 + DOWN * 0.15

        def cell_pos(row, col):
            x = (col - 2) * cell_size
            y = (2 - row) * cell_size
            return grid_center + np.array([x, y, 0])

        # =========================
        # 1. 标题：从蒙特卡洛过渡到 TD
        # =========================
        title_cn = Text(
            "时序差分 TD：边走边学习",
            font=font_cn,
            font_size=38,
            color=WHITE
        ).to_edge(UP)

        title_en = Text(
            "Temporal Difference: Learn After Every Step",
            font=font_en,
            font_size=22,
            color=GRAY_B
        ).next_to(title_cn, DOWN, buff=0.12)

        self.play(
            FadeIn(title_cn, shift=DOWN),
            FadeIn(title_en, shift=DOWN),
            run_time=1.6
        )
        self.wait(0.8)

        # =========================
        # 2. 左侧构造 Gridworld
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
                ).move_to(cell_pos(r, c))
                grid.add(square)

        start = cell_pos(0, 0)
        next_state = cell_pos(0, 1)
        goal = cell_pos(4, 4)

        agent = Dot(start, radius=0.11, color=BLUE_B)

        agent_label = Text(
            "Agent",
            font=font_en,
            font_size=18,
            color=BLUE_B
        ).next_to(agent, UP, buff=0.08)


        agent_label = VGroup(agent_label)

        goal_star = Star(
            n=5,
            outer_radius=0.18,
            inner_radius=0.08,
            color=YELLOW,
            fill_opacity=1
        ).move_to(goal)

        goal_glow = Circle(
            radius=0.30,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color=YELLOW,
            fill_opacity=0.13
        ).move_to(goal)

        trap_positions = [(1, 1), (2, 3), (4, 2)]
        traps = VGroup(*[
            Text(
                "×",
                font=font_en,
                font_size=36,
                color=RED_B
            ).move_to(cell_pos(r, c))
            for r, c in trap_positions
        ])

        self.play(
            LaggedStart(
                *[FadeIn(s, scale=0.85) for s in grid],
                lag_ratio=0.02
            ),
            run_time=2.0
        )

        self.play(
            FadeIn(agent, scale=1.3),
            FadeIn(agent_label),
            FadeIn(goal_glow, scale=1.4),
            FadeIn(goal_star, scale=1.2),
            LaggedStart(
                *[FadeIn(t, scale=1.2) for t in traps],
                lag_ratio=0.12
            ),
            run_time=1.5
        )

        # =========================
        # 3. 对比：Monte Carlo 等到最后，TD 现在就更新
        # =========================
        mc_box = RoundedRectangle(
            width=4.65,
            height=1.55,
            corner_radius=0.16,
            stroke_color=RED_B,
            fill_color="#1A1A1A",
            fill_opacity=0.85
        ).to_edge(RIGHT).shift(UP * 1.5 + LEFT * 0.15)

        mc_cn = Text(
            "蒙特卡洛",
            font=font_cn,
            font_size=26,
            color=RED_B
        ).move_to(mc_box.get_top() + DOWN * 0.35)

        mc_en = Text(
            "Monte Carlo",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(mc_cn, DOWN, buff=0.03)

        mc_text_cn = Text(
            "等一整局结束后再更新",
            font=font_cn,
            font_size=22,
            color=WHITE
        ).next_to(mc_en, DOWN, buff=0.18)

        mc_text_en = Text(
            "update after the episode ends",
            font=font_en,
            font_size=15,
            color=GRAY_B
        ).next_to(mc_text_cn, DOWN, buff=0.04)

        mc_group = VGroup(mc_box, mc_cn, mc_en, mc_text_cn, mc_text_en)

        td_box = RoundedRectangle(
            width=4.65,
            height=1.55,
            corner_radius=0.16,
            stroke_color=BLUE_B,
            fill_color="#1A1A1A",
            fill_opacity=0.85
        ).next_to(mc_box, DOWN, buff=0.45)

        td_cn = Text(
            "TD 方法",
            font=font_cn,
            font_size=26,
            color=BLUE_B
        ).move_to(td_box.get_top() + DOWN * 0.35)

        td_en = Text(
            "Temporal Difference",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(td_cn, DOWN, buff=0.03)

        td_text_cn = Text(
            "每走一步，立刻更新",
            font=font_cn,
            font_size=22,
            color=WHITE
        ).next_to(td_en, DOWN, buff=0.18)

        td_text_en = Text(
            "update after every step",
            font=font_en,
            font_size=15,
            color=GRAY_B
        ).next_to(td_text_cn, DOWN, buff=0.04)

        td_group = VGroup(td_box, td_cn, td_en, td_text_cn, td_text_en)

        self.play(FadeIn(mc_group, shift=LEFT), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(td_group, shift=LEFT), run_time=1.2)
        self.wait(0.8)

        # 给蒙特卡洛加一个叉，突出 TD 的优势
        mc_cross = Cross(mc_box, stroke_color=RED_B, stroke_width=5)
        td_glow = SurroundingRectangle(td_box, color=BLUE_B, buff=0.08, stroke_width=4)

        self.play(Create(mc_cross), run_time=0.8)
        self.play(Create(td_glow), run_time=0.9)
        self.wait(0.7)

        # =========================
        # 4. 走一步：s_t, a_t, r_t, s_{t+1}
        # =========================
        step_title_cn = Text(
            "只看眼前这一步",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).next_to(grid, DOWN, buff=0.42)

        step_title_en = Text(
            "Look at one transition",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(step_title_cn, DOWN, buff=0.06)

        step_title = VGroup(step_title_cn, step_title_en)

        self.play(
            FadeOut(mc_group),
            FadeOut(mc_cross),
            FadeOut(td_group),
            FadeOut(td_glow),
            FadeIn(step_title, shift=UP),
            run_time=1.2
        )

        # 当前状态 s_t 的高亮框
        current_cell_box = Square(
            side_length=cell_size * 0.95,
            stroke_color=BLUE_B,
            stroke_width=4
        ).move_to(start)

        st_label = MathTex(
            r"s_t",
            font_size=30,
            color=BLUE_B
        ).next_to(current_cell_box, UP, buff=0.08)

        self.play(Create(current_cell_box), FadeIn(st_label), run_time=0.9)
        self.wait(0.4)

        action_arrow = Arrow(
            start,
            next_state,
            buff=0.18,
            stroke_width=6,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.25
        )

        action_label = Text(
            "action: Right",
            font=font_en,
            font_size=22,
            color=YELLOW
        ).next_to(action_arrow, UP, buff=0.12)

        

        action_label = VGroup(action_label)

        self.play(GrowArrow(action_arrow), FadeIn(action_label), run_time=1.0)

        # 智能体移动一步
        self.play(
            agent.animate.move_to(next_state),
            FadeOut(agent_label),
            run_time=0.9
        )
        
        next_cell_box = Square(
            side_length=cell_size * 0.95,
            stroke_color=GREEN_B,
            stroke_width=4
        ).move_to(next_state)

        st1_label = MathTex(
            r"s_{t+1}",
            font_size=30,
            color=GREEN_B
        ).next_to(next_cell_box, UP, buff=0.08)

        reward_label = MathTex(
            r"r_t = 0",
            font_size=30,
            color=WHITE
        ).next_to(action_arrow, DOWN, buff=0.12)

        self.play(
            Create(next_cell_box),
            FadeIn(st1_label),
            FadeIn(reward_label, shift=UP),
            run_time=1.0
        )
        self.wait(1.5)

        self.play(
            FadeOut(action_label),
            FadeOut(reward_label),
            runtime=0.9
        )


        # =========================
        # 5. 右侧显示 transition 四元组
        # =========================
        transition_box = RoundedRectangle(
            width=4.9,
            height=2.1,
            corner_radius=0.16,
            stroke_color=GRAY_B,
            fill_color="#1A1A1A",
            fill_opacity=0.86
        ).to_edge(RIGHT).shift(UP * 1.25 + LEFT * 0.1)

        transition_title_cn = Text(
            "一步就能得到的信息",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).move_to(transition_box.get_top() + DOWN * 0.35)

        transition_title_en = Text(
            "Information from one step",
            font=font_en,
            font_size=16,
            color=GRAY_B
        ).next_to(transition_title_cn, DOWN, buff=0.03)

        transition_formula = MathTex(
            r"(s_t,\ a_t,\ r_t,\ s_{t+1})",
            font_size=34,
            color=YELLOW
        ).next_to(transition_title_en, DOWN, buff=0.25)

        transition_meaning_cn = Text(
            "状态、动作、奖励、下一状态",
            font=font_cn,
            font_size=21,
            color=GRAY_A
        ).next_to(transition_formula, DOWN, buff=0.20)

        transition_meaning_en = Text(
            "state, action, reward, next state",
            font=font_en,
            font_size=14,
            color=GRAY_B
        ).next_to(transition_meaning_cn, DOWN, buff=0.03)

        transition_group = VGroup(
            transition_box,
            transition_title_cn,
            transition_title_en,
            transition_formula,
            transition_meaning_cn,
            transition_meaning_en
        )

        self.play(FadeIn(transition_group, shift=LEFT), run_time=1.3)
        self.wait(1.0)

        # =========================
        # 6. TD 更新公式
        # =========================
        formula_panel = RoundedRectangle(
            width=6.5,
            height=2.75,
            corner_radius=0.16,
            stroke_color=BLUE_B,
            fill_color="#151515",
            fill_opacity=0.92
        ).next_to(grid, RIGHT, buff=1.8).align_to(grid, DOWN)

        formula_title_cn = Text(
            "TD 更新公式",
            font=font_cn,
            font_size=26,
            color=BLUE_B
        ).move_to(formula_panel.get_top() + DOWN * 0.35)

        formula_title_en = Text(
            "TD Update Rule",
            font=font_en,
            font_size=16,
            color=GRAY_B
        ).next_to(formula_title_cn, DOWN, buff=0.03)

        update_formula = MathTex(
            r"Q(s_t,a_t)",
            r"\leftarrow",
            r"Q(s_t,a_t)",
            r"+",
            r"\alpha",
            r"\delta_t",
            font_size=34
        ).next_to(formula_title_en, DOWN, buff=0.35)

        update_formula[0].set_color(BLUE_B)
        update_formula[2].set_color(GRAY_A)
        update_formula[4].set_color(YELLOW)
        update_formula[5].set_color(RED_B)

        delta_formula = MathTex(
            r"\delta_t",
            r"=",
            r"r_t",
            r"+",
            r"\gamma Q(s_{t+1},a_{t+1})",
            r"-",
            r"Q(s_t,a_t)",
            font_size=30
        ).next_to(update_formula, DOWN, buff=0.42)

        delta_formula[0].set_color(RED_B)
        delta_formula[2].set_color(YELLOW)
        delta_formula[4].set_color(GREEN_B)
        delta_formula[6].set_color(BLUE_B)

        formula_group = VGroup(
            formula_panel,
            formula_title_cn,
            formula_title_en,
            update_formula,
            delta_formula
        )

        self.play(
            FadeOut(transition_group),
            FadeIn(formula_panel),
            FadeIn(formula_title_cn),
            FadeIn(formula_title_en),
            run_time=0.9
        )

        self.play(Write(update_formula), run_time=2.0)
        self.wait(0.5)
        self.play(Write(delta_formula), run_time=2.2)
        self.wait(0.6)

        # =========================
        # 7. 高亮 TD 误差
        # =========================
        td_error_rect = SurroundingRectangle(
            delta_formula,
            color=RED_B,
            buff=0.12,
            stroke_width=4
        )

        td_error_label_cn = Text(
            "TD 误差：新的判断 - 旧的判断",
            font=font_cn,
            font_size=25,
            color=RED_B
        ).to_edge(DOWN)

        td_error_label_en = Text(
            "TD error = new estimate minus old estimate",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(td_error_label_cn, DOWN, buff=0.06)

        td_error_label = VGroup(td_error_label_cn, td_error_label_en)

        self.play(
            Create(td_error_rect),
            FadeIn(td_error_label, shift=UP),
            run_time=1.2
        )
        self.wait(1.8)

        # 分别强调新判断和旧判断
        new_est_rect = SurroundingRectangle(
            VGroup(delta_formula[2], delta_formula[3], delta_formula[4]),
            color=GREEN_B,
            buff=0.10,
            stroke_width=3
        )

        old_est_rect = SurroundingRectangle(
            delta_formula[6],
            color=BLUE_B,
            buff=0.10,
            stroke_width=3
        )

        new_est_label_cn = Text(
            "新判断",
            font=font_cn,
            font_size=22,
            color=GREEN_B
        ).next_to(new_est_rect, UP, buff=0.12)

        old_est_label_cn = Text(
            "旧判断",
            font=font_cn,
            font_size=22,
            color=BLUE_B
        ).next_to(old_est_rect, DOWN, buff=0.12)

        self.play(
            Create(new_est_rect),
            FadeIn(new_est_label_cn),
            run_time=1.0
        )
        self.wait(0.6)

        self.play(
            Create(old_est_rect),
            FadeIn(old_est_label_cn),
            run_time=1.0
        )
        self.wait(1.0)

        # =========================
        # 8. 用数值展示一次更新
        # =========================
        self.play(
            FadeOut(td_error_label),
            FadeOut(td_error_rect),
            FadeOut(new_est_rect),
            FadeOut(old_est_rect),
            FadeOut(new_est_label_cn),
            FadeOut(old_est_label_cn),
            run_time=0.8
        )

        example_title_cn = Text(
            "一次具体的价值更新",
            font=font_cn,
            font_size=27,
            color=YELLOW
        ).to_edge(DOWN)

        example_title_en = Text(
            "A concrete update example",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(example_title_cn, DOWN, buff=0.06)

        example_title = VGroup(example_title_cn, example_title_en)

        self.play(FadeIn(example_title, shift=UP), run_time=0.8)

        # 左侧当前格子显示旧价值
        q_old = DecimalNumber(
            0.30,
            num_decimal_places=2,
            font_size=34,
            color=BLUE_B
        ).move_to(start + DOWN * 0.03)

        q_old_label = Text(
            "old value",
            font=font_en,
            font_size=18,
            color=BLUE_B
        ).next_to(q_old, LEFT, buff=0.12)

        q_new_label = Text(
            "new value",
            font=font_en,
            font_size=18,
            color=BLUE_B
        ).next_to(q_old, LEFT, buff=0.12)

        q_value_group = VGroup(q_old, q_old_label, q_new_label)

        self.play(FadeIn(q_value_group, scale=1.2), run_time=0.8)
        self.wait(0.4)

        numeric_delta = MathTex(
            r"\delta_t = 0 + 0.9 \times 0.80 - 0.30 = 0.42",
            font_size=32,
            color=RED_B
        ).move_to(delta_formula)

        self.play(Transform(delta_formula, numeric_delta), run_time=1.4)
        self.wait(0.8)

        numeric_update = MathTex(
            r"Q_{\text{new}} = 0.30 + 0.5 \times 0.42 = 0.51",
            font_size=32,
            color=GREEN_B
        ).move_to(update_formula)

        self.play(Transform(update_formula, numeric_update), run_time=1.4)
        self.wait(0.8)

        # 数值从 0.30 更新到 0.51
        
        self.play(
            q_old.animate.set_value(0.51).set_color(GREEN_B),
            q_old_label.animate.set_color(GREEN_B),
            current_cell_box.animate.set_stroke(GREEN_B, width=5),
            Transform(q_old_label, q_new_label),
            run_time=2.0
        )

        self.play(
            FadeOut(example_title),
            run_time=0.9
        )
        self.wait(1.4)

        # =========================
        # 9. 总结：边走边记账
        # =========================
        summary_box = RoundedRectangle(
            width=10,
            height=1.1,
            corner_radius=0.16,
            stroke_color=BLUE_B,
            fill_color="#222222",
            fill_opacity=0.96
        ).to_edge(DOWN)

        summary_cn = Text(
            "TD 方法：每走一步就修正一次估计，不是事后算账",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).move_to(summary_box.get_center() + UP * 0.18)

        summary_en = Text(
            "TD learns online: one step, one correction.",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(summary_cn, DOWN, buff=0.08)

        summary = VGroup(summary_cn, summary_en)

        self.play(
            FadeOut(step_title), 
            FadeIn(summary_box, shift=UP),
            FadeIn(summary, shift=UP),
            run_time=1.2
        )
        self.wait(3.6)

        # 为下一段 SARSA / Q-Learning 铺垫
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)
        next_hint_cn = Text(
            "但下一步的价值，应该用“实际动作”，还是“最优动作”？",
            font=font_cn,
            font_size=27,
            color=YELLOW
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "Should the next value follow the actual action or the best action?",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        self.play(FadeIn(next_hint, shift=UP), run_time=1.1)
        self.wait(2.2)