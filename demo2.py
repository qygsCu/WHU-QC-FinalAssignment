from manim import *
import numpy as np


class MonteCarloIntroLong(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 全局字体
        # =========================
        font_cn = "SimSun"   # 宋体；如果不显示，可改成 "宋体"
        font_en = "Times New Roman"

        # =========================
        # 基础参数
        # =========================
        cell_size = 0.62
        grid_n = 5
        grid_center = LEFT * 3.2 + DOWN * 0.1

        def cell_pos(row, col):
            x = (col - 2) * cell_size
            y = (2 - row) * cell_size
            return grid_center + np.array([x, y, 0])

        # =========================
        # 1. 标题：经典强化学习
        # =========================
        title_cn = Text(
            "经典强化学习：先试错，再复盘",
            font=font_cn,
            font_size=36,
            color=WHITE
        ).to_edge(UP)

        title_en = Text(
            "Classical Reinforcement Learning: Trial and Review",
            font=font_en,
            font_size=23,
            color=GRAY_B
        ).next_to(title_cn, DOWN, buff=0.12)

        self.play(
            FadeIn(title_cn, shift=DOWN),
            FadeIn(title_en, shift=DOWN),
            run_time=1.8
        )
        self.wait(0.8)

        # =========================
        # 2. 构造 5x5 网格世界
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
        goal = cell_pos(4, 4)

        agent = Dot(start, radius=0.11, color=BLUE_B)
        agent_label_cn = Text(
            "智能体",
            font=font_cn,
            font_size=18,
            color=BLUE_B
        ).next_to(agent, UP, buff=0.08)

        agent_label_en = Text(
            "Agent",
            font=font_en,
            font_size=14,
            color=BLUE_B
        ).next_to(agent_label_cn, DOWN, buff=0.02)

        agent_label = VGroup(agent_label_cn, agent_label_en)

        goal_star = Star(
            n=5,
            outer_radius=0.19,
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

        goal_label_cn = Text(
            "终点",
            font=font_cn,
            font_size=18,
            color=YELLOW
        ).next_to(goal_star, DOWN, buff=0.08)

        goal_label_en = Text(
            "Goal",
            font=font_en,
            font_size=14,
            color=YELLOW
        ).next_to(goal_label_cn, DOWN, buff=0.02)

        goal_label = VGroup(goal_label_cn, goal_label_en)

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
                lag_ratio=0.025
            ),
            run_time=2.4
        )

        self.play(
            FadeIn(agent, scale=1.3),
            FadeIn(agent_label),
            FadeIn(goal_glow, scale=1.5),
            FadeIn(goal_star, scale=1.2),
            FadeIn(goal_label),
            LaggedStart(
                *[FadeIn(t, scale=1.3) for t in traps],
                lag_ratio=0.15
            ),
            run_time=1.8
        )

        # =========================
        # 3. 解释 Episode
        # =========================
        episode_cn = Text(
            "Episode：从起点走到终点的一整局",
            font=font_cn,
            font_size=28,
            color=WHITE
        ).to_edge(RIGHT).shift(UP * 1.85 + LEFT * 0.15)

        episode_en = Text(
            "One complete trajectory from start to goal",
            font=font_en,
            font_size=20,
            color=GRAY_B
        ).next_to(episode_cn, DOWN, buff=0.12)

        episode_explain = VGroup(episode_cn, episode_en)

        self.play(FadeIn(episode_explain, shift=LEFT), run_time=1.2)
        self.wait(0.6)

        # 用一条淡线暗示完整轨迹
        preview_path = VMobject(color=YELLOW, stroke_width=4)
        preview_points = [
            cell_pos(0, 0),
            cell_pos(0, 1),
            cell_pos(1, 1),
            cell_pos(1, 2),
            cell_pos(2, 2),
            cell_pos(3, 2),
            cell_pos(3, 3),
            cell_pos(4, 3),
            cell_pos(4, 4),
        ]
        preview_path.set_points_as_corners(preview_points)
        preview_path.set_opacity(0.35)

        self.play(Create(preview_path), run_time=2.0)
        self.play(FadeOut(preview_path), run_time=0.7)

        # =========================
        # 4. 右侧轨迹记录表
        # =========================
        record_box = RoundedRectangle(
            width=4.65,
            height=3,
            corner_radius=0.15,
            stroke_color=GRAY_B,
            fill_color="#1A1A1A",
            fill_opacity=0.82
        ).to_edge(RIGHT).shift(DOWN * 0.35 + LEFT * 0.1)

        record_title_cn = Text(
            "本局轨迹记录",
            font=font_cn,
            font_size=24,
            color=YELLOW
        ).move_to(record_box.get_top() + DOWN * 0.35)

        record_title_en = Text(
            "Trajectory Log",
            font=font_en,
            font_size=16,
            color=GRAY_B
        ).next_to(record_title_cn, DOWN, buff=0.03)

        header = Text(
            "Step   State  Action  Reward",
            font="Consolas",
            font_size=17,
            color=GRAY_A
        ).next_to(record_title_en, DOWN, buff=0.18)

        self.play(
            FadeIn(record_box),
            FadeIn(record_title_cn),
            FadeIn(record_title_en),
            FadeIn(header),
            run_time=1.2
        )

        # =========================
        # 5. 智能体试错路径
        # =========================
        path_cells = [
            (0, 0),
            (0, 1),
            (1, 1),
            (1, 2),
            (2, 2),
            (3, 2),
            (3, 3),
            (4, 3),
            (4, 4),
        ]

        actions = [
            "Right",
            "Down",
            "Right",
            "Down",
            "Down",
            "Right",
            "Down",
            "Right",
        ]

        action_cn = [
            "向右",
            "向下",
            "向右",
            "向下",
            "向下",
            "向右",
            "向下",
            "向右",
        ]

        rewards = [0, -10, 0, 0, 0, 0, 0, 10]
        path_points = [cell_pos(r, c) for r, c in path_cells]

        arrows = VGroup()
        record_rows = VGroup()

        trial_cn = Text(
            "它并不知道哪一步是好的，只能先试一遍。",
            font=font_cn,
            font_size=26,
            color=GRAY_A
        ).to_edge(DOWN)

        trial_en = Text(
            "The agent does not know the best move yet.",
            font=font_en,
            font_size=19,
            color=GRAY_B
        ).next_to(trial_cn, DOWN, buff=0.08)

        trial_text = VGroup(trial_cn, trial_en)

        self.play(FadeIn(trial_text, shift=UP), run_time=1.0)
        self.wait(0.5)

        current_y = header.get_bottom()[1] - 0.26

        for i in range(len(path_points) - 1):
            start_p = path_points[i]
            end_p = path_points[i + 1]

            # 动作提示
            action_tip_cn = Text(
                f"尝试动作：{action_cn[i]}",
                font=font_cn,
                font_size=25,
                color=BLUE_B
            ).next_to(grid, DOWN, buff=0.38)

            action_tip_en = Text(
                f"Try action: {actions[i]}",
                font=font_en,
                font_size=18,
                color=GRAY_B
            ).next_to(action_tip_cn, DOWN, buff=0.05)

            action_tip = VGroup(action_tip_cn, action_tip_en)

            self.play(FadeIn(action_tip, shift=UP), run_time=0.35)

            arrow = Arrow(
                start_p,
                end_p,
                buff=0.18,
                stroke_width=5,
                color=BLUE_C,
                max_tip_length_to_length_ratio=0.28
            )
            arrows.add(arrow)

            self.play(
                GrowArrow(arrow),
                agent.animate.move_to(end_p),
                run_time=0.75
            )

            agent_label.next_to(agent, UP, buff=0.08)
            self.play(agent_label.animate.next_to(agent, UP, buff=0.08), run_time=0.15)

            self.wait(0.15)

            reward = rewards[i]

            # 奖励提示
            if reward < 0:
                reward_text_cn = Text(
                    "踩到陷阱：reward = -10",
                    font=font_cn,
                    font_size=24,
                    color=RED_B
                ).next_to(grid, DOWN, buff=0.38)

                reward_text_en = Text(
                    "Bad transition",
                    font=font_en,
                    font_size=18,
                    color=RED_B
                ).next_to(reward_text_cn, DOWN, buff=0.05)

                reward_text = VGroup(reward_text_cn, reward_text_en)

                self.play(
                    FadeOut(action_tip),
                    FadeIn(reward_text, shift=UP),
                    Indicate(traps[0], color=RED_B),
                    run_time=0.75
                )
                self.wait(0.2)
                self.play(FadeOut(reward_text), run_time=0.3)

            elif reward > 0:
                reward_text_cn = Text(
                    "到达终点：reward = +10",
                    font=font_cn,
                    font_size=24,
                    color=YELLOW
                ).next_to(grid, DOWN, buff=0.38)

                reward_text_en = Text(
                    "Goal reached",
                    font=font_en,
                    font_size=18,
                    color=YELLOW
                ).next_to(reward_text_cn, DOWN, buff=0.05)

                reward_text = VGroup(reward_text_cn, reward_text_en)

                self.play(
                    FadeOut(action_tip),
                    FadeIn(reward_text, shift=UP),
                    Flash(goal_star, color=YELLOW),
                    run_time=0.85
                )
                self.wait(0.25)
                self.play(FadeOut(reward_text), run_time=0.3)

            else:
                self.play(FadeOut(action_tip), run_time=0.25)

            # 右侧记录表增加一行
            state_number = path_cells[i][0] * 5 + path_cells[i][1] + 1

            row_color = WHITE
            if reward < 0:
                row_color = RED_B
            elif reward > 0:
                row_color = YELLOW

            row_text = Text(
                f"{i + 1:<6}    s={state_number:<2}       {actions[i]:<5}      {reward:+d}",
                font="Consolas",
                font_size=16,
                color=row_color
            )
            row_text.move_to(np.array([record_box.get_center()[0], current_y, 0]))
            current_y -= 0.215

            record_rows.add(row_text)
            self.play(FadeIn(row_text, shift=LEFT * 0.2), run_time=0.45)

        self.wait(0.5)

        # =========================
        # 6. Episode 结束：整条路径高亮
        # =========================
        finish_cn = Text(
            "Episode 结束",
            font=font_cn,
            font_size=31,
            color=YELLOW
        ).next_to(grid, UP, buff=0.32)

        finish_en = Text(
            "The whole episode is finished.",
            font=font_en,
            font_size=19,
            color=GRAY_B
        ).next_to(finish_cn, DOWN, buff=0.06)

        finish_text = VGroup(finish_cn, finish_en)

        self.play(
            FadeOut(trial_text),
            FadeIn(finish_text, scale=1.15),
            arrows.animate.set_color(YELLOW),
            run_time=1.2
        )

        self.play(
            Circumscribe(arrows, color=YELLOW, fade_out=True),
            run_time=1.4
        )

        # =========================
        # 7. 重点提示：现在才开始学习
        # =========================
        learn_now_cn = Text(
            "注意：直到这一刻，它才真正开始更新经验",
            font=font_cn,
            font_size=27,
            color=YELLOW
        ).to_edge(DOWN)

        learn_now_en = Text(
            "Only now can Monte Carlo update its value estimates.",
            font=font_en,
            font_size=19,
            color=GRAY_B
        ).next_to(learn_now_cn, DOWN, buff=0.08)

        learn_now = VGroup(learn_now_cn, learn_now_en)

        self.play(FadeIn(learn_now, shift=UP), run_time=1.0)
        self.wait(1.3)
        self.play(FadeOut(learn_now), run_time=0.5)

        # =========================
        # 8. 回头计算累计回报
        # =========================
        formula_title_cn = Text(
            "回头计算累计回报",
            font=font_cn,
            font_size=27,
            color=WHITE
        ).move_to(episode_cn)

        formula_title_en = Text(
            "Compute the return after the episode",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(formula_title_cn, DOWN, buff=0.08)

        formula_title = VGroup(formula_title_cn, formula_title_en)

        return_formula = MathTex(
            r"G_t = r_t + \gamma r_{t+1} + \gamma^2 r_{t+2} + \cdots",
            font_size=34,
            color=BLUE_B
        ).next_to(formula_title, DOWN, buff=0.48)

        formula_meaning_cn = Text(
            "也就是：把未来的奖励折算回当前这一步",
            font=font_cn,
            font_size=23,
            color=GRAY_A
        ).next_to(return_formula, DOWN, buff=0.28)

        formula_meaning_en = Text(
            "future rewards are discounted back to the current step",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(formula_meaning_cn, DOWN, buff=0.06)

        formula_meaning = VGroup(formula_meaning_cn, formula_meaning_en)

        self.play(
            FadeOut(episode_explain),
            FadeIn(formula_title, shift=LEFT),
            run_time=0.9
        )
        self.play(
            FadeOut(record_box),
            FadeOut(record_title_cn),
            FadeOut(record_title_en),
            FadeOut(header),
            FadeOut(record_rows),
            run_time=0.8
        )
        self.play(Write(return_formula), run_time=1.8)
        
        self.play(FadeIn(formula_meaning, shift=UP), run_time=1.0)
        self.wait(0.8)

        # =========================
        # 9. 从终点反向更新每一步价值
        # =========================
        review_cn = Text(
            "然后沿着刚才的轨迹，反向更新每一步的价值",
            font=font_cn,
            font_size=26,
            color=GREEN_B
        ).to_edge(DOWN)

        review_en = Text(
            "Review the trajectory backwards and update values.",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(review_cn, DOWN, buff=0.08)

        review_text = VGroup(review_cn, review_en)

        self.play(FadeIn(review_text, shift=UP), run_time=0.9)

        # 反向传播的绿色光点
        update_dots = VGroup()
        value_labels = VGroup()

        for index, (r, c) in enumerate(path_cells[:-1]):
            dot = Dot(cell_pos(r, c), radius=0.065, color=GREEN_B)
            update_dots.add(dot)

        # 反向依次出现更新点
        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=1.8) for dot in reversed(update_dots)],
                lag_ratio=0.14
            ),
            run_time=3.0
        )

        # 在部分格子旁显示 Value updated
        selected_indices = [0, 2, 5]
        for idx in selected_indices:
            label_cn = Text(
                "价值更新",
                font=font_cn,
                font_size=18,
                color=GREEN_B
            ).next_to(update_dots[idx], UP, buff=0.08)

            label_en = Text(
                "Value updated",
                font=font_en,
                font_size=12,
                color=GREEN_B
            ).next_to(label_cn, DOWN, buff=0.02)

            value_label = VGroup(label_cn, label_en)
            value_labels.add(value_label)

        self.play(
            LaggedStart(
                *[FadeIn(label, shift=UP * 0.1) for label in value_labels],
                lag_ratio=0.35
            ),
            run_time=1.8
        )

        # 从终点指回起点的大箭头
        curved_arrow = CurvedArrow(
            start_point=goal + RIGHT * 0.32,
            end_point=start + LEFT * 0.2,
            color=GREEN_B,
            stroke_width=5
        )

        back_cn = Text(
            "从结果反推前面的判断",
            font=font_cn,
            font_size=22,
            color=GREEN_B
        ).next_to(grid, LEFT, buff=0.35)

        back_en = Text(
            "learn after seeing the outcome",
            font=font_en,
            font_size=15,
            color=GRAY_B
        ).next_to(back_cn, DOWN, buff=0.05)

        back_text = VGroup(back_cn, back_en)

        self.play(
            Create(curved_arrow),
            FadeIn(back_text, shift=RIGHT),
            run_time=2.0
        )

        self.wait(0.8)

        # =========================
        # 10. 总结蒙特卡洛的优缺点
        # =========================
        summary_box = RoundedRectangle(
            width=10.4,
            height=1.2,
            corner_radius=0.16,
            stroke_color=YELLOW,
            fill_color="#222222",
            fill_opacity=0.96
        ).to_edge(DOWN)

        summary_cn = Text(
            "蒙特卡洛：结果直观可靠，但必须等一整局结束后才能更新",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).move_to(summary_box.get_center() + UP * 0.18)

        summary_en = Text(
            "Accurate and intuitive, but updates only after the episode ends.",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(summary_cn, DOWN, buff=0.08)

        summary = VGroup(summary_cn, summary_en)

        self.play(
            FadeOut(review_text),
            FadeOut(value_labels),
            FadeIn(summary_box, shift=UP),
            FadeIn(summary, shift=UP),
            run_time=1.2
        )
        self.wait(2.0)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.9)

        # 为下一段 TD 铺垫
        next_hint_cn = Text(
            "那么，能不能每走一步就学习一次？",
            font=font_cn,
            font_size=28,
            color=BLUE_B
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "Can we learn after every single step?",
            font=font_en,
            font_size=19,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        self.play(FadeIn(next_hint, shift=UP), run_time=1.0)
        self.wait(2.0)