from manim import *

class CartoonSlime(Scene):
    def construct(self):
        # 1. 建立角色：一個圓潤的卡通史萊姆 (Slime)
        body = Circle(radius=1.5, color=PINK, fill_opacity=0.8)
        eye_l = Dot(point=[-0.5, 0.3, 0], radius=0.2, color=BLACK)
        eye_r = Dot(point=[0.5, 0.3, 0], radius=0.2, color=BLACK)
        mouth = Arc(radius=0.5, start_angle=220*DEGREES, angle=100*DEGREES, color=BLACK)
        mouth.shift(DOWN * 0.2)
        
        slime = VGroup(body, eye_l, eye_r, mouth)
        
        # 2. 標題
        title = Text("Cartoon Animation Study", font_size=36, color=YELLOW).to_edge(UP)

        # 3. 動畫流程 (總計約 15 秒)

        # [0-3s] 史萊姆從下方跳入並打招呼
        self.play(Write(title))
        slime.shift(DOWN * 5)
        self.play(slime.animate.shift(UP * 5), run_time=2, rate_func=ease_out_back)
        self.wait(1)

        # [4-7s] 史萊姆開心地左右搖晃 (卡通感擠壓)
        self.play(
            slime.animate.scale(1.2).set_color(LIGHT_PINK),
            run_time=1
        )
        self.play(
            slime.animate.rotate(20*DEGREES, about_point=slime.get_bottom()),
            run_time=0.5
        )
        self.play(
            slime.animate.rotate(-40*DEGREES, about_point=slime.get_bottom()),
            run_time=1
        )
        self.play(
            slime.animate.rotate(20*DEGREES, about_point=slime.get_bottom()),
            run_time=0.5
        )
        self.wait(1)

        # [8-11s] 史萊姆變換表情 (驚訝)
        new_mouth = Circle(radius=0.2, color=BLACK).shift(DOWN * 0.3)
        self.play(Transform(mouth, new_mouth))
        self.play(slime.animate.shift(UP * 1), run_time=0.5, rate_func=there_and_back)
        self.wait(1.5)

        # [12-15s] 史萊姆旋轉並變成彩虹圖案消失
        rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        rainbow_group = VGroup(*[
            Circle(radius=1.5 - i*0.2, color=rainbow_colors[i], fill_opacity=0.5)
            for i in range(len(rainbow_colors))
        ])
        
        self.play(FadeOut(eye_l), FadeOut(eye_r), FadeOut(mouth))
        self.play(ReplacementTransform(body, rainbow_group))
        self.play(
            Rotate(rainbow_group, angle=PI*2),
            rainbow_group.animate.scale(0),
            FadeOut(title),
            run_time=2
        )
        self.wait(1)
