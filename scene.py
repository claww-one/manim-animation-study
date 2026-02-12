from manim import *

class StudyAnimation(Scene):
    def construct(self):
        # 1. 建立幾何圖形
        circle = Circle(radius=1.5, color=BLUE)
        square = Square(side_length=2, color=RED)
        triangle = Triangle().scale(1.5).set_color(GREEN)

        # 2. 文字標題
        title = Text("OpenClaw Animation Study", font_size=36).to_edge(UP)

        # 3. 動畫流程 (總計約 15 秒)
        
        # [0-2s] 標題與圓形出現
        self.play(Write(title))
        self.play(Create(circle))
        self.wait(1)

        # [3-6s] 圓形變形為正方形
        self.play(ReplacementTransform(circle, square))
        self.wait(1)

        # [7-10s] 正方形變形為三角形，並旋轉
        self.play(ReplacementTransform(square, triangle))
        self.play(Rotate(triangle, angle=PI*2), run_time=2)
        self.wait(1)

        # [11-15s] 三角形分裂並消失
        dots = VGroup(*[Dot(triangle.get_vertices()[i], color=triangle.get_color()) for i in range(3)])
        self.play(ReplacementTransform(triangle, dots))
        self.play(FadeOut(dots), FadeOut(title), run_time=2)
        self.wait(1)
