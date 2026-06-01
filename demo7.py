from manim import *
import numpy as np


class GroverAmplitudeAmplification(Scene):
    def construct(self):
        self.camera.background_color = "#111111"

        # =========================
        # 全局时间倍率
        # =========================
        # 原视频约 55s，1.55 倍后约 80~90s
        # 如果还短，改成 1.7；如果太慢，改成 1.35
        TIME_SCALE = 1.55

        def play_s(*animations, run_time=1.0, **kwargs):
            self.play(*animations, run_time=run_time * TIME_SCALE, **kwargs)

        def wait_s(duration=1.0):
            self.wait(duration * TIME_SCALE)

        # =========================
        # 全局字体
        # =========================
        font_cn = "SimSun"          # 宋体；如果不显示，可改成 "宋体"
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

        def make_operator_box(label, color, center):
            box = RoundedRectangle(
                width=2.25,
                height=0.82,
                corner_radius=0.15,
                stroke_color=color,
                stroke_width=3,
                fill_color="#1A1A1A",
                fill_opacity=0.92
            ).move_to(center)

            text = Text(
                label,
                font=font_en,
                font_size=25,
                color=color
            ).move_to(box)

            return VGroup(box, text)

        def make_prob_bars(probs, axis_y=-1.45, scale=2.6):
            x_positions = [-2.7, -0.9, 0.9, 2.7]
            colors = [BLUE_B, BLUE_B, YELLOW, BLUE_B]
            bars = VGroup()
            labels = VGroup()
            prob_texts = VGroup()

            ket_names = [
                r"\lvert 00\rangle",
                r"\lvert 01\rangle",
                r"\lvert 10\rangle",
                r"\lvert 11\rangle"
            ]
            action_names = ["left", "up", "right", "down"]

            for i, p in enumerate(probs):
                height = max(p * scale, 0.018)

                bar = Rectangle(
                    width=0.56,
                    height=height,
                    stroke_color=colors[i],
                    stroke_width=2,
                    fill_color=colors[i],
                    fill_opacity=0.66
                ).move_to(np.array([x_positions[i], axis_y + height / 2, 0]))

                ket_label = MathTex(
                    ket_names[i],
                    font_size=27,
                    color=colors[i] if i == 2 else BLUE_B
                ).next_to(bar, DOWN, buff=0.18)

                action_label = Text(
                    action_names[i],
                    font=font_en,
                    font_size=16,
                    color=GRAY_A
                ).next_to(ket_label, DOWN, buff=0.06)

                if p >= 0.995:
                    prob_str = r"100\%"
                elif p <= 0.005:
                    prob_str = r"0\%"
                else:
                    prob_str = rf"{int(round(p * 100))}\%"

                prob_label = MathTex(
                    prob_str,
                    font_size=26,
                    color=YELLOW if i == 2 else GRAY_A
                ).next_to(bar, UP, buff=0.12)

                bars.add(bar)
                labels.add(VGroup(ket_label, action_label))
                prob_texts.add(prob_label)

            return bars, labels, prob_texts

        def make_amp_bars(values, axis_y=-0.35, scale=2.25):
            x_positions = [-2.7, -0.9, 0.9, 2.7]
            bars = VGroup()
            value_labels = VGroup()

            for i, v in enumerate(values):
                color = YELLOW if i == 2 else BLUE_B
                height = max(abs(v) * scale, 0.018)

                if abs(v) < 1e-6:
                    center_y = axis_y
                    fill_opacity = 0.25
                    stroke_color = GRAY_B
                    fill_color = GRAY_B
                else:
                    center_y = axis_y + np.sign(v) * height / 2
                    fill_opacity = 0.68
                    stroke_color = color
                    fill_color = color

                bar = Rectangle(
                    width=0.56,
                    height=height,
                    stroke_color=stroke_color,
                    stroke_width=2,
                    fill_color=fill_color,
                    fill_opacity=fill_opacity
                ).move_to(np.array([x_positions[i], center_y, 0]))

                bars.add(bar)

                if abs(v - 0.5) < 1e-6:
                    tex = r"+\frac{1}{2}"
                elif abs(v + 0.5) < 1e-6:
                    tex = r"-\frac{1}{2}"
                elif abs(v - 1.0) < 1e-6:
                    tex = r"1"
                elif abs(v) < 1e-6:
                    tex = r"0"
                else:
                    tex = rf"{v:.2f}"

                if v >= 0:
                    value_label = MathTex(
                        tex,
                        font_size=25,
                        color=stroke_color
                    ).next_to(bar, UP, buff=0.10)
                else:
                    value_label = MathTex(
                        tex,
                        font_size=25,
                        color=stroke_color
                    ).next_to(bar, DOWN, buff=0.10)

                value_labels.add(value_label)

            return bars, value_labels

        def make_amp_labels(axis_y=-0.35):
            x_positions = [-2.7, -0.9, 0.9, 2.7]
            ket_names = [
                r"\lvert 00\rangle",
                r"\lvert 01\rangle",
                r"\lvert 10\rangle",
                r"\lvert 11\rangle"
            ]
            action_names = ["left", "up", "right", "down"]

            labels = VGroup()

            for i in range(4):
                ket_label = MathTex(
                    ket_names[i],
                    font_size=27,
                    color=YELLOW if i == 2 else BLUE_B
                ).move_to(np.array([x_positions[i], axis_y - 1.0, 0]))

                action_label = Text(
                    action_names[i],
                    font=font_en,
                    font_size=16,
                    color=GRAY_A
                ).next_to(ket_label, DOWN, buff=0.06)

                labels.add(VGroup(ket_label, action_label))

            return labels

        # =========================
        # 1. 标题
        # =========================
        title = bilingual_text(
            "Grover 振幅放大：把 best action 的概率调大",
            "Grover Amplitude Amplification: Turn Up the Best Action",
            font_size_cn=35,
            font_size_en=21,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.8
        ).to_edge(UP, buff=0.35)

        play_s(FadeIn(title, shift=DOWN), run_time=1.5)
        wait_s(0.8)

        # =========================
        # 2. 从上一段的 25% 概率开始
        # =========================
        axis = Line(
            LEFT * 4.25 + DOWN * 1.45,
            RIGHT * 4.25 + DOWN * 1.45,
            color=GRAY_B,
            stroke_width=2
        )

        init_probs = [0.25, 0.25, 0.25, 0.25]
        prob_bars, prob_labels, prob_texts = make_prob_bars(init_probs)

        caption = bottom_caption(
            "刚生成 superposition 时，每个 action 被测到的概率都是 25%",
            "Right after superposition, each action has a 25% chance of being measured.",
            color_cn=BLUE_B
        )

        play_s(Create(axis), run_time=0.8)

        play_s(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in prob_bars],
                lag_ratio=0.14
            ),
            FadeIn(prob_labels),
            FadeIn(prob_texts),
            run_time=2.0
        )

        play_s(FadeIn(caption, shift=UP), run_time=1.0)
        wait_s(1.5)

        # =========================
        # 3. 标记 best action
        # =========================
        best_box = SurroundingRectangle(
            VGroup(prob_bars[2], prob_labels[2], prob_texts[2]),
            color=YELLOW,
            buff=0.14,
            stroke_width=4
        )

        best_tag = Text(
            "best action",
            font=font_en,
            font_size=22,
            color=YELLOW
        ).next_to(best_box, UP, buff=0.14)

        best_caption = bottom_caption(
            "如果直接 measure，best action 也只有 25% 的概率被选中",
            "If we measure directly, the best action is still selected only 25% of the time.",
            color_cn=YELLOW
        )

        play_s(Create(best_box), FadeIn(best_tag, shift=UP), run_time=1.1)
        play_s(Transform(caption, best_caption), run_time=1.0)
        wait_s(1.8)

        # =========================
        # 4. 切换到 amplitude 视角
        # =========================
        amp_title = bilingual_text(
            "先别看概率，改看 amplitude",
            "Instead of probability, look at amplitude first",
            font_size_cn=33,
            font_size_en=20,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.0
        ).to_edge(UP, buff=0.38)

        play_s(
            FadeOut(best_box),
            FadeOut(best_tag),
            FadeOut(caption),
            FadeOut(axis),
            FadeOut(prob_bars),
            FadeOut(prob_labels),
            FadeOut(prob_texts),
            Transform(title, amp_title),
            run_time=1.2
        )

        amp_axis_y = -0.35
        amp_axis = Line(
            LEFT * 4.25 + UP * amp_axis_y,
            RIGHT * 4.25 + UP * amp_axis_y,
            color=GRAY_B,
            stroke_width=2
        )

        zero_label = MathTex(
            r"0",
            font_size=24,
            color=GRAY_B
        ).next_to(amp_axis.get_left(), LEFT, buff=0.12)

        amp_bars, amp_value_labels = make_amp_bars([0.5, 0.5, 0.5, 0.5], axis_y=amp_axis_y)
        amp_labels = make_amp_labels(axis_y=amp_axis_y)

        amp_formula = MathTex(
            r"P_i = |a_i|^2",
            font_size=34,
            color=YELLOW
        ).move_to(RIGHT * 3.3 + UP * 1.65)

        amp_formula_box = SurroundingRectangle(
            amp_formula,
            color=YELLOW,
            buff=0.18,
            stroke_width=2
        )

        play_s(Create(amp_axis), FadeIn(zero_label), run_time=0.9)

        play_s(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in amp_bars],
                lag_ratio=0.14
            ),
            FadeIn(amp_labels),
            FadeIn(amp_value_labels),
            run_time=2.1
        )

        play_s(FadeIn(amp_formula_box), Write(amp_formula), run_time=1.5)

        amp_caption = bottom_caption(
            "概率来自 amplitude 的平方，所以我们可以先改 amplitude",
            "Probability comes from squared amplitude, so we reshape amplitude first.",
            color_cn=YELLOW
        )

        play_s(FadeIn(amp_caption, shift=UP), run_time=1.0)
        wait_s(1.8)

        # =========================
        # 5. 第一步：Oracle 相位翻转
        # =========================
        oracle_box = make_operator_box(
            "Oracle",
            RED_B,
            RIGHT * 3.25 + UP * 1.45
        )

        oracle_caption = bottom_caption(
            "第一步，Oracle 标记 best action：把它的 phase 翻转",
            "Step 1: the Oracle marks the best action by flipping its phase.",
            color_cn=RED_B
        )

        play_s(
            FadeOut(amp_caption),
            FadeOut(amp_formula),
            FadeOut(amp_formula_box),
            FadeIn(oracle_box, shift=LEFT),
            FadeIn(oracle_caption, shift=UP),
            run_time=1.2
        )
        wait_s(0.8)

        target_mark = SurroundingRectangle(
            VGroup(amp_bars[2], amp_labels[2], amp_value_labels[2]),
            color=RED_B,
            buff=0.14,
            stroke_width=4
        )

        flip_formula = MathTex(
            r"a_{\text{best}} \rightarrow -a_{\text{best}}",
            font_size=32,
            color=RED_B
        ).next_to(oracle_box, DOWN, buff=0.28)

        play_s(Create(target_mark), Write(flip_formula), run_time=1.5)
        wait_s(1.0)

        oracle_bars, oracle_values = make_amp_bars([0.5, 0.5, -0.5, 0.5], axis_y=amp_axis_y)

        play_s(
            Transform(amp_bars, oracle_bars),
            Transform(amp_value_labels, oracle_values),
            run_time=2.0
        )

        play_s(
            Flash(amp_bars[2], color=RED_B, flash_radius=0.52),
            run_time=1.0
        )
        wait_s(1.4)

        # =========================
        # 6. 第二步：Diffusion 关于平均值反射
        # =========================
        mean_value = 0.25
        scale = 2.25
        mean_y = amp_axis_y + mean_value * scale

        mean_line = DashedLine(
            LEFT * 4.1 + UP * mean_y,
            RIGHT * 4.1 + UP * mean_y,
            color=GREEN_B,
            stroke_width=3,
            dash_length=0.18
        )

        mean_label = Text(
            "mean",
            font=font_en,
            font_size=20,
            color=GREEN_B
        ).next_to(mean_line, LEFT, buff=0.12)

        mean_tex = MathTex(
            r"\bar a = 0.25",
            font_size=28,
            color=GREEN_B
        ).next_to(mean_line, RIGHT, buff=0.16)

        mean_caption = bottom_caption(
            "现在所有 amplitude 的平均值是 0.25",
            "Now the mean amplitude is 0.25.",
            color_cn=GREEN_B
        )

        play_s(
            FadeOut(oracle_caption),
            FadeIn(mean_caption, shift=UP),
            Create(mean_line),
            FadeIn(mean_label),
            FadeIn(mean_tex),
            run_time=1.5
        )
        wait_s(1.4)

        diffusion_box = make_operator_box(
            "Diffusion",
            GREEN_B,
            RIGHT * 3.25 + UP * 1.45
        )

        diffusion_caption = bottom_caption(
            "第二步，Diffusion：让所有 amplitude 关于平均值反射",
            "Step 2: Diffusion reflects all amplitudes about the mean.",
            color_cn=GREEN_B
        )

        reflect_formula = MathTex(
            r"a_i \rightarrow 2\bar a - a_i",
            font_size=32,
            color=GREEN_B
        ).move_to(flip_formula)

        play_s(
            FadeOut(oracle_box),
            FadeOut(flip_formula),
            FadeIn(diffusion_box, shift=LEFT),
            Transform(mean_caption, diffusion_caption),
            Write(reflect_formula),
            run_time=1.5
        )
        wait_s(1.4)

        diffused_bars, diffused_values = make_amp_bars([0.0, 0.0, 1.0, 0.0], axis_y=amp_axis_y)

        play_s(
            FadeOut(target_mark),
            Transform(amp_bars, diffused_bars),
            Transform(amp_value_labels, diffused_values),
            run_time=2.2
        )

        play_s(
            Flash(amp_bars[2], color=YELLOW, flash_radius=0.70),
            run_time=1.1
        )

        amplified_caption = bottom_caption(
            "经过一次 Grover iteration，best action 的 amplitude 被放大",
            "After one Grover iteration, the best action amplitude is amplified.",
            color_cn=YELLOW
        )

        play_s(Transform(mean_caption, amplified_caption), run_time=1.0)
        wait_s(1.9)

        # =========================
        # 7. 回到概率视角
        # =========================
        prob_title = bilingual_text(
            "回到概率：best action 现在几乎必然被测到",
            "Back to Probability: The Best Action Is Almost Certain",
            font_size_cn=33,
            font_size_en=20,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.3
        ).to_edge(UP, buff=0.38)

        play_s(
            FadeOut(mean_caption),
            FadeOut(diffusion_box),
            FadeOut(reflect_formula),
            FadeOut(mean_line),
            FadeOut(mean_label),
            FadeOut(mean_tex),
            FadeOut(amp_axis),
            FadeOut(zero_label),
            FadeOut(amp_bars),
            FadeOut(amp_value_labels),
            FadeOut(amp_labels),
            Transform(title, prob_title),
            run_time=1.2
        )

        prob_axis = Line(
            LEFT * 4.25 + DOWN * 1.45,
            RIGHT * 4.25 + DOWN * 1.45,
            color=GRAY_B,
            stroke_width=2
        )

        final_probs = [0.0, 0.0, 1.0, 0.0]
        final_bars, final_labels, final_prob_texts = make_prob_bars(final_probs)

        play_s(Create(prob_axis), run_time=0.8)

        play_s(
            LaggedStart(
                *[GrowFromEdge(bar, DOWN) for bar in final_bars],
                lag_ratio=0.14
            ),
            FadeIn(final_labels),
            FadeIn(final_prob_texts),
            run_time=2.1
        )

        measure_box = make_operator_box(
            "measure",
            YELLOW,
            UP * 1.55
        )

        measure_arrow = Arrow(
            measure_box.get_bottom(),
            final_bars[2].get_top(),
            buff=0.12,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.18
        )

        measure_caption = bottom_caption(
            "这时再 measure，就会高概率坍缩到 best action",
            "Now measurement collapses to the best action with high probability.",
            color_cn=YELLOW
        )

        play_s(
            FadeIn(measure_box, shift=DOWN),
            GrowArrow(measure_arrow),
            FadeIn(measure_caption, shift=UP),
            run_time=1.4
        )

        play_s(
            Flash(final_bars[2], color=YELLOW, flash_radius=0.65),
            final_bars[2].animate.set_fill(YELLOW, opacity=0.88).set_stroke(YELLOW),
            run_time=1.1
        )
        wait_s(1.7)

        # =========================
        # 8. 复杂度：O(N) 到 O(sqrt(N))
        # =========================
        play_s(
            FadeOut(prob_axis),
            FadeOut(final_bars),
            FadeOut(final_labels),
            FadeOut(final_prob_texts),
            FadeOut(measure_box),
            FadeOut(measure_arrow),
            FadeOut(measure_caption),
            run_time=1.1
        )

        complexity_title = bilingual_text(
            "这就是 Grover 带来的二次加速",
            "This Is the Quadratic Speedup from Grover Search",
            font_size_cn=34,
            font_size_en=20,
            color_cn=WHITE,
            color_en=GRAY_B,
            max_width=11.5
        ).to_edge(UP, buff=0.38)

        play_s(Transform(title, complexity_title), run_time=1.2)

        classical_box = RoundedRectangle(
            width=4.65,
            height=1.55,
            corner_radius=0.16,
            stroke_color=RED_B,
            stroke_width=3,
            fill_color="#1A1A1A",
            fill_opacity=0.93
        ).move_to(LEFT * 2.65 + UP * 0.15)

        grover_box = RoundedRectangle(
            width=4.65,
            height=1.55,
            corner_radius=0.16,
            stroke_color=GREEN_B,
            stroke_width=3,
            fill_color="#1A1A1A",
            fill_opacity=0.93
        ).move_to(RIGHT * 2.65 + UP * 0.15)

        classical_formula = MathTex(
            r"\text{Classical search: } O(N)",
            font_size=31,
            color=RED_B
        ).move_to(classical_box.get_center() + UP * 0.18)

        classical_note = Text(
            "try one by one",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(classical_formula, DOWN, buff=0.12)

        grover_formula = MathTex(
            r"\text{Grover search: } O(\sqrt{N})",
            font_size=31,
            color=GREEN_B
        ).move_to(grover_box.get_center() + UP * 0.18)

        grover_note = Text(
            "amplify before measure",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(grover_formula, DOWN, buff=0.12)

        arrow_between = Arrow(
            classical_box.get_right(),
            grover_box.get_left(),
            buff=0.25,
            color=YELLOW,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.18
        )

        n_note = MathTex(
            r"N = 2^n\ \text{actions}",
            font_size=33,
            color=YELLOW
        ).next_to(arrow_between, DOWN, buff=0.45)

        play_s(
            FadeIn(classical_box),
            Write(classical_formula),
            FadeIn(classical_note),
            run_time=1.4
        )

        play_s(GrowArrow(arrow_between), run_time=1.0)

        play_s(
            FadeIn(grover_box),
            Write(grover_formula),
            FadeIn(grover_note),
            Write(n_note),
            run_time=1.7
        )

        speed_caption = bottom_caption(
            "注意这里的 N 是候选 action 数量，不是 qubit 数量",
            "Here N is the number of candidate actions, not the number of qubits.",
            color_cn=YELLOW
        )

        play_s(FadeIn(speed_caption, shift=UP), run_time=1.0)
        wait_s(2.4)

        # =========================
        # 9. 总结 Grover iteration
        # =========================
        summary_box = RoundedRectangle(
            width=8.1,
            height=1.55,
            corner_radius=0.16,
            stroke_color=YELLOW,
            stroke_width=2,
            fill_color="#222222",
            fill_opacity=0.96
        ).to_edge(DOWN, buff=0.18)

        summary_line_1 = Text(
            "Grover iteration = Oracle phase flip + Diffusion reflection",
            font=font_en,
            font_size=21,
            color=YELLOW
        )

        summary_line_2 = Text(
            "先标记 best action，再把它的 amplitude 放大",
            font=font_cn,
            font_size=22,
            color=WHITE
        ).next_to(summary_line_1, DOWN, buff=0.10)

        summary_en = Text(
            "Mark the target, then amplify its amplitude before measurement.",
            font=font_en,
            font_size=15,
            color=GRAY_B
        ).next_to(summary_line_2, DOWN, buff=0.06)

        summary_text = VGroup(summary_line_1, summary_line_2, summary_en)
        summary_text.move_to(summary_box.get_center())

        summary_group = VGroup(summary_box, summary_text)

        play_s(
            FadeOut(speed_caption),
            FadeIn(summary_group, shift=UP),
            run_time=1.2
        )
        wait_s(2.4)

        # =========================
        # 10. 为下一段代码演示铺垫
        # =========================
        play_s(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)

        next_hint_cn = Text(
            "这些 Oracle 和 Diffusion，代码里到底长什么样？",
            font=font_cn,
            font_size=28,
            color=YELLOW
        ).move_to(ORIGIN + UP * 0.08)

        next_hint_en = Text(
            "What do Oracle and Diffusion look like in code?",
            font=font_en,
            font_size=17,
            color=GRAY_B
        ).next_to(next_hint_cn, DOWN, buff=0.06)

        next_hint = VGroup(next_hint_cn, next_hint_en)

        play_s(FadeIn(next_hint, shift=UP), run_time=1.2)
        wait_s(2.8)