from manimlib import *

class HuffmanArchitecture(Scene):
    def construct(self):
        # --- CONFIGURATION (Customize here) ---
        CONFIG = {
            "node_width": 2.2,
            "node_height": 1.0,
            "h_buff": 1.0,        # Horizontal spacing between groups
            "v_buff": 0.5,        # Vertical spacing in Group 3
            "node_color": "#222222",
            "stroke_color": WHITE,
            "text_scale": 0.75,
            "bg_group_color": "#444444",
            "bg_opacity": 0.3,
            "arrow_color": GREY_B
        }

        # --- HELPER FUNCTIONS ---
        def create_box(text_str, width=CONFIG["node_width"], height=CONFIG["node_height"]):
            box = Rectangle(
                width=width, height=height, 
                fill_color=CONFIG["node_color"], fill_opacity=1, 
                stroke_color=CONFIG["stroke_color"]
            )
            text = Text(text_str, font_size=24, t2c={"Min1": YELLOW, "Min2": YELLOW, "CNT": BLUE})
            text.scale(CONFIG["text_scale"])
            # Auto-wrap text slightly if too wide
            if text.get_width() > width - 0.2:
                text.set_width(width - 0.4)
            return VGroup(box, text)

        def create_cylinder(text_str):
            # Custom shape for the Register/Database
            w, h = 1.9, 1.2
            ellipse_top = Circle(radius=w/2).stretch(0.3, 1).set_fill(CONFIG["node_color"], 1)
            ellipse_bottom = ellipse_top.copy()
            rect = Rectangle(width=w, height=h, fill_color=CONFIG["node_color"], fill_opacity=1, stroke_opacity=0)
            
            ellipse_top.move_to(rect.get_top())
            ellipse_bottom.move_to(rect.get_bottom())
            
            # Visual layering
            body = VGroup(ellipse_bottom, rect, ellipse_top)
            # Outline
            lines = VGroup(
                Line(rect.get_corner(UL), rect.get_corner(DL)),
                Line(rect.get_corner(UR), rect.get_corner(DR))
            ).set_stroke(CONFIG["stroke_color"])
            
            content = VGroup(body, lines, ellipse_top.copy().set_fill(opacity=0).set_stroke(CONFIG["stroke_color"]))
            
            text = Text(text_str, font_size=24)
            text.scale(CONFIG["text_scale"])
            text.move_to(rect.get_center())
            
            return VGroup(content, text)

        def create_group_bg(nodes, label_text):
            # Calculate scaled dimensions based on original node size
            new_width = nodes.get_width() * 1.1
            new_height = nodes.get_height() * 1.7
            
            bg = Rectangle(
                width=new_width, 
                height=new_height,
                color=GREY, 
                fill_color=CONFIG["bg_group_color"], 
                fill_opacity=CONFIG["bg_opacity"]
            )
            bg.move_to(nodes.get_center())
            bg.set_stroke(width=0)
            
            label = Text(label_text, font_size=16, color=GREY_A).next_to(bg.get_top(), DOWN, buff=0.1)
            return VGroup(bg, label)

        # --- 1. CREATE NODES ---
        
        # Input
        input_node = Rectangle(width=1.8, height=0.8, fill_color="#333", fill_opacity=1)
        input_text = Text("Input: gray_data", font_size=20)
        input_grp = VGroup(input_node, input_text).to_edge(LEFT)

        # Group 1: Data Reading
        freq_logic = create_box("Frequency Counter\nLogic (CNT[i] + 1)")
        freq_regs = create_cylinder("Frequency\nRegisters (CNT Array)")
        
        # Group 2: Comparator
        step1 = create_box("Step 1: Find Absolute\nMin (Min1)")
        step2 = create_box("Step 2: Mask Min1\n(Set Index to Max)")
        step3 = create_box("Step 3: Find Absolute\nMin (Min2)")

        # Group 3: Merge & Code
        merge_calc = create_box("Merge Calculation\n(New CNT = Min1 + Min2)")
        code_gen = create_box("Code Generation\n(Update Registers)")
        
        # Output
        output_node = Rectangle(width=1.6, height=0.8, fill_color="#333", fill_opacity=1)
        output_text = Text("Output: HC & M", font_size=20)
        output_grp = VGroup(output_node, output_text)

        # --- 2. POSITIONING ---
        
        # Layout Group 1
        freq_logic.next_to(input_grp, RIGHT, buff=0.6)
        freq_regs.next_to(freq_logic, RIGHT, buff=0.3)
        
        # Layout Group 2 (Sequential Line)
        step1.next_to(freq_regs, RIGHT, buff=0.8) # Bigger gap for the crossing arrows
        step2.next_to(step1, RIGHT, buff=0.3)
        step3.next_to(step2, RIGHT, buff=0.3)

        # Layout Group 3 (Vertical Stack)
        # Center this group relative to the end of step 3
        merge_calc.next_to(step3, RIGHT, buff=0.8).shift(UP * 0.8)
        code_gen.next_to(step3, RIGHT, buff=0.8).shift(DOWN * 0.8)
        
        output_grp.next_to(code_gen, RIGHT, buff=0.6)

        # Create Backgrounds (must be done after positioning)
        bg1 = create_group_bg(VGroup(freq_logic, freq_regs), "1. Data Reading & Counting")
        self.play(FadeIn(bg1))

        bg2 = create_group_bg(VGroup(step1, step2, step3), "2. Comparator Process - Sequential")
        self.play(FadeIn(bg2))

        bg3 = create_group_bg(VGroup(merge_calc, code_gen), "3. Code Assignment & Merge")
        self.play(FadeIn(bg3))

        # --- ANIMATE NODES & BACKGROUNDS ---
        self.play(
            Write(input_grp), 
            Write(output_grp),
            Write(VGroup(freq_logic, freq_regs)),
            Write(VGroup(step1, step2, step3)),
            Write(VGroup(merge_calc, code_gen))
        )

        # --- 3. CONNECTIONS (ARROWS) ---
        
        arrows = VGroup()
        labels = VGroup()

        # Simple linear flow
        arrows.add(Arrow(input_grp.get_right(), freq_logic.get_left(), color=CONFIG["arrow_color"]))
        arrows.add(Arrow(freq_logic.get_right(), freq_regs.get_left(), color=CONFIG["arrow_color"]))
        
        arrows.add(Arrow(step1.get_right(), step2.get_left(), color=CONFIG["arrow_color"]))
        arrows.add(Arrow(step2.get_right(), step3.get_left(), color=CONFIG["arrow_color"]))
        
        # Branching from Step 3
        a_to_merge = Arrow(step3.get_right(), merge_calc.get_left(), color=CONFIG["arrow_color"])
        a_to_code = Arrow(step3.get_right(), code_gen.get_left(), color=CONFIG["arrow_color"])
        arrows.add(a_to_merge, a_to_code)

        # Output flow
        arrows.add(Arrow(code_gen.get_right(), output_grp.get_left(), color=CONFIG["arrow_color"]))

        # Complex Flows (Dashed / Feedback)
        
        # 1. Feedback Loop: Merge -> Registers
        # Go Up from Merge, Left across everything, Down to Registers
        path_points = [
            merge_calc.get_top(),
            merge_calc.get_top() + UP * 0.5,
            freq_regs.get_top() + UP * 0.5 + RIGHT * 0.5, # Slightly offset
            freq_regs.get_top()
        ]
        feedback_arrow = Arrow(
             start=merge_calc.get_top(), end=freq_regs.get_top(), path_arc=1.5, color=GREY_A
        )
        # Custom path for rectangular feedback
        feedback_line = VMobject().set_points_as_corners([
            merge_calc.get_top(),
            merge_calc.get_top() + UP * 0.8,
            freq_regs.get_top() + UP * 0.8,
            freq_regs.get_top()
        ])
        feedback_arrow = Arrow(path_points[-2], path_points[-1], color=GREY_A)
        # Actually, let's just draw lines + tip manually for clean elbow look
        fb_path = VMobject().set_points_as_corners([
            merge_calc.get_top(),
            merge_calc.get_top() + UP * 0.5,
            freq_regs.get_top() + UP * 0.5,
            freq_regs.get_top()
        ]).set_stroke(GREY_A)
        fb_tip = Arrow(freq_regs.get_top() + UP*0.4, freq_regs.get_top(), buff=0, color=GREY_A)
        
        fb_label = Text("Update CNT", font_size=14, color=GREY_A).next_to(fb_path, UP, buff=0.05)
        
        # 2. "Read Data" Dashed lines
        # From Regs to Step 1 and Step 2/3 (Conceptual)
        d_line = DashedLine(freq_regs.get_right(), step1.get_left(), color=GREY_A)
        d_label = Text("Read Data", font_size=14, color=GREY_A).next_to(d_line, UP, buff=0.05)

        # 3. Internal Labels
        l1 = Text("Latch Min1 Index", font_size=14, color=GREY_B).next_to(step1, DOWN, buff=0.1)
        # l2 = Text("Masked Data", font_size=14, color=GREY_B).next_to(step2, RIGHT, buff=0.1).shift(UP*0.2)

        labels.add(fb_label, d_label, l1)

        # --- ANIMATE CONNECTIONS & LABELS ---
        self.play(ShowCreation(arrows), ShowCreation(d_line), ShowCreation(fb_path), FadeIn(fb_tip))
        self.play(Write(labels))

        self.frame.reorient(0, 0, 0, (np.float32(3.35), np.float32(0.31), np.float32(0.0)), 11.56)
