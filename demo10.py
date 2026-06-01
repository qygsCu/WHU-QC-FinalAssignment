from manim import *


class FinalSummaryCredits(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # =========================
        # 时间倍率
        # =========================
        # 目标时长约 45~55 秒
        TIME_SCALE = 1.15

        def play_s(*animations, run_time=1.0, **kwargs):
            self.play(*animations, run_time=run_time * TIME_SCALE, **kwargs)

        def wait_s(duration=1.0):
            self.wait(duration * TIME_SCALE)

        # =========================
        # 字体
        # =========================
        font_cn = "SimSun"          # 宋体；如果不显示，可改为 "宋体"
        font_en = "Times New Roman"

        # =========================
        # 工具函数
        # =========================
        def bilingual_text(
            cn,
            en,
            font_size_cn=26,
            font_size_en=16,
            color_cn=WHITE,
            color_en=GRAY_B,
            buff=0.07,
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

        def make_card(title, subtitle, color, width=2.75, height=1.55):
            card = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.18,
                stroke_color=color,
                stroke_width=3,
                fill_color="#141414",
                fill_opacity=0.95
            )

            title_obj = Text(
                title,
                font=font_en,
                font_size=23,
                color=color
            ).move_to(card.get_center() + UP * 0.30)

            subtitle_obj = Text(
                subtitle,
                font=font_cn,
                font_size=18,
                color=GRAY_A
            ).next_to(title_obj, DOWN, buff=0.15)

            group = VGroup(card, title_obj, subtitle_obj)

            return group

        # =========================
        # 1. 全黑开头：Summary
        # =========================
        summary_word = Text(
            "Summary",
            font=font_en,
            font_size=64,
            color=WHITE
        ).move_to(ORIGIN)

        summary_sub = Text(
            "总结",
            font=font_cn,
            font_size=32,
            color=GRAY_B
        ).next_to(summary_word, DOWN, buff=0.22)

        summary_open = VGroup(summary_word, summary_sub)

        play_s(FadeIn(summary_open, scale=1.08), run_time=1.6)
        wait_s(1.0)

        play_s(
            summary_open.animate.scale(0.58).to_edge(UP, buff=0.35),
            run_time=1.2
        )

        # =========================
        # 2. 四个核心模块总结
        # =========================
        card_1 = make_card(
            "Classical RL",
            "价值更新",
            BLUE_B
        )

        card_2 = make_card(
            "Superposition",
            "展开动作空间",
            PURPLE_B
        )

        card_3 = make_card(
            "Grover",
            "放大优质动作",
            YELLOW
        )

        card_4 = make_card(
            "TD Update",
            "经典闭环学习",
            GREEN_B
        )

        cards = VGroup(card_1, card_2, card_3, card_4).arrange(
            RIGHT,
            buff=0.38
        ).move_to(UP * 0.65)

        arrows = VGroup()

        for i in range(3):
            arrow = Arrow(
                cards[i].get_right(),
                cards[i + 1].get_left(),
                buff=0.12,
                color=GRAY_A,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18
            )
            arrows.add(arrow)

        play_s(
            LaggedStart(
                FadeIn(card_1, shift=UP * 0.15),
                GrowArrow(arrows[0]),
                FadeIn(card_2, shift=UP * 0.15),
                GrowArrow(arrows[1]),
                FadeIn(card_3, shift=UP * 0.15),
                GrowArrow(arrows[2]),
                FadeIn(card_4, shift=UP * 0.15),
                lag_ratio=0.20
            ),
            run_time=3.0
        )

        wait_s(0.8)

        # =========================
        # 3. 一句话总结核心思想
        # =========================
        main_idea_box = RoundedRectangle(
            width=9.2,
            height=1.25,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#181818",
            fill_opacity=0.94
        ).to_edge(DOWN, buff=0.38)

        main_idea_cn = Text(
            "核心思想：量子计算不替代强化学习，而是加速其中最像搜索的 action selection",
            font=font_cn,
            font_size=25,
            color=WHITE
        )

        main_idea_en = Text(
            "Quantum computing does not replace RL; it accelerates the search-like action selection step.",
            font=font_en,
            font_size=16,
            color=GRAY_B
        ).next_to(main_idea_cn, DOWN, buff=0.08)

        main_idea_text = VGroup(main_idea_cn, main_idea_en)
        main_idea_text.scale_to_fit_width(8.65)
        main_idea_text.move_to(main_idea_box.get_center())

        main_idea = VGroup(main_idea_box, main_idea_text)

        play_s(FadeIn(main_idea, shift=UP), run_time=1.2)
        wait_s(2.0)

        # =========================
        # 4. 逐步强调三句话
        # =========================
        play_s(
            FadeOut(main_idea),
            cards.animate.shift(UP * 0.30).scale(0.90),
            arrows.animate.shift(UP * 0.30).scale(0.90),
            run_time=1.0
        )

        point_box = RoundedRectangle(
            width=8.8,
            height=2.10,
            corner_radius=0.18,
            stroke_color=GRAY_B,
            stroke_width=2,
            fill_color="#111111",
            fill_opacity=0.96
        ).move_to(DOWN * 1.30)

        point_1 = bilingual_text(
            "第一，经典 RL 的瓶颈之一，是大动作空间中的探索效率。",
            "First, one bottleneck of classical RL is exploration in large action spaces.",
            font_size_cn=23,
            font_size_en=15,
            color_cn=BLUE_B,
            color_en=GRAY_B,
            max_width=8.1
        ).move_to(point_box.get_center() + UP * 0.55)

        point_2 = bilingual_text(
            "第二，Grover 可以通过 amplitude amplification 提高 best action 的测量概率。",
            "Second, Grover increases the probability of measuring the best action.",
            font_size_cn=23,
            font_size_en=15,
            color_cn=YELLOW,
            color_en=GRAY_B,
            max_width=8.1
        ).move_to(point_box.get_center())

        point_3 = bilingual_text(
            "第三，最终的学习仍由 classical TD update 稳定完成。",
            "Third, learning is still completed by the classical TD update.",
            font_size_cn=23,
            font_size_en=15,
            color_cn=GREEN_B,
            color_en=GRAY_B,
            max_width=8.1
        ).move_to(point_box.get_center() + DOWN * 0.55)

        points = VGroup(point_box, point_1, point_2, point_3)

        play_s(FadeIn(point_box), run_time=0.8)
        play_s(FadeIn(point_1, shift=RIGHT * 0.2), run_time=1.0)
        wait_s(0.8)
        play_s(FadeIn(point_2, shift=RIGHT * 0.2), run_time=1.0)
        wait_s(0.8)
        play_s(FadeIn(point_3, shift=RIGHT * 0.2), run_time=1.0)
        wait_s(1.8)

        # =========================
        # 5. 最终结论句
        # =========================
        play_s(
            FadeOut(cards),
            FadeOut(arrows),
            FadeOut(points),
            run_time=1.0
        )

        conclusion_cn = Text(
            "Quantum chooses. Classical learns.",
            font=font_en,
            font_size=44,
            color=YELLOW
        ).move_to(UP * 0.35)

        conclusion_sub = Text(
            "量子负责更快地选择，经典负责稳定地学习。",
            font=font_cn,
            font_size=28,
            color=WHITE
        ).next_to(conclusion_cn, DOWN, buff=0.22)

        conclusion_en = Text(
            "This is the core idea of quantum-enhanced reinforcement learning.",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(conclusion_sub, DOWN, buff=0.12)

        conclusion = VGroup(conclusion_cn, conclusion_sub, conclusion_en)

        play_s(FadeIn(conclusion, scale=1.05), run_time=1.4)
        wait_s(2.4)

        # =========================
        # 6. 致谢页
        # =========================
        play_s(
            FadeOut(summary_open),
            FadeOut(conclusion),
            run_time=1.0
        )

        thanks_title = Text(
            "Thank You",
            font=font_en,
            font_size=58,
            color=WHITE
        ).move_to(UP * 1.95)

        thanks_cn = Text(
            "感谢观看",
            font=font_cn,
            font_size=32,
            color=GRAY_A
        ).next_to(thanks_title, DOWN, buff=0.18)

        line = Line(
            LEFT * 3.5,
            RIGHT * 3.5,
            color=GRAY_D,
            stroke_width=2
        ).next_to(thanks_cn, DOWN, buff=0.35)

        course_info = Text(
            "量子信息与量子计算基础结课作业",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).next_to(line, DOWN, buff=0.42)

        project_info = Text(
            "基于 Grover 搜索的量子强化学习算法",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).next_to(course_info, DOWN, buff=0.25)

        authors_title = Text(
            "Authors",
            font=font_en,
            font_size=22,
            color=GRAY_B
        ).next_to(project_info, DOWN, buff=0.48)

        authors = Text(
            "武汉大学计算机学院 24 级  侯芃泽 · 李定松 · 田园",
            font=font_cn,
            font_size=25,
            color=WHITE
        ).next_to(authors_title, DOWN, buff=0.18)

        final_note = Text(
            "School of Computer Science, Wuhan University",
            font=font_en,
            font_size=18,
            color=GRAY_B
        ).next_to(authors, DOWN, buff=0.18)

        credit_group = VGroup(
            thanks_title,
            thanks_cn,
            line,
            course_info,
            project_info,
            authors_title,
            authors,
            final_note
        )

        play_s(FadeIn(thanks_title, shift=DOWN), FadeIn(thanks_cn, shift=DOWN), run_time=1.3)
        play_s(Create(line), run_time=0.8)
        play_s(FadeIn(course_info, shift=UP), run_time=1.0)
        play_s(FadeIn(project_info, shift=UP), run_time=1.0)
        play_s(FadeIn(authors_title), FadeIn(authors, shift=UP), FadeIn(final_note, shift=UP), run_time=1.2)

        wait_s(3.0)

        # =========================
        # 7. 淡出结束
        # =========================
        play_s(FadeOut(credit_group), run_time=1.8)
        wait_s(0.8)