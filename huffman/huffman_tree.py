from manimlib_import_ext import *

class HuffmanTree(Scene):
    def construct(self):
        # ==========================================
        # SETUP
        # ==========================================
        title = Text("Huffman Tree Construction (Hardware State)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        NODE_SCALE = 0.7  # Define a scale factor for node size

        # --- Positions for Tree Structure ---
        # Leaves at the bottom
        leaf_y = -3.0
        pos_1 = np.array([-4, leaf_y, 0])
        pos_2 = np.array([0, leaf_y, 0])
        pos_3 = np.array([4, leaf_y, 0])
        
        # Parent Nodes (Calculated positions)
        pos_grp1 = np.array([-2, -0.5, 0])  # Between 1 and 2, higher up
        pos_root = np.array([1, 1.5, 0])   # Between Grp1 and 3, higher up

        # --- Helper: Create Node Visual ---
        def create_node(label, freq, mask_str, color, pos, scale=1.0):
            # Circle
            c = Circle(radius=1.2 * scale, color=color)
            c.set_fill(color, opacity=0.2)
            
            # Text Elements
            lbl = Text(label, font_size=24*scale, weight=BOLD).next_to(c, UP, buff=0.1)
            frq = Text(f"Freq: {freq}", font_size=28*scale, color=WHITE).move_to(c.get_center() + UP*0.4*scale)
            
            # Mask Info
            mask_lbl = Text("Mask:", font_size=32*scale, color=GREY_B).next_to(frq, DOWN, buff=0.1*scale)
            mask_val = Text(mask_str, font_size=32*scale, font="Consolas", color=YELLOW).next_to(mask_lbl, DOWN, buff=0.05*scale)
            
            # Code/Len Info (Important for Leaves)
            code_val = Text("Code: -", font_size=32*scale, font="Consolas", color=GREEN).next_to(mask_val, DOWN, buff=0.2*scale)
            
            # Grouping
            group = VGroup(c, lbl, frq, mask_lbl, mask_val, code_val)
            group.move_to(pos)
            
            # Return dict of parts for easy updates
            return {
                "group": group, "circle": c, "freq": frq, 
                "mask": mask_val, "code": code_val, "pos": pos, "label": lbl
            }

        # --- Create Leaves ---
        n1 = create_node("Sym 1", 2, "001", BLUE, pos_1, scale=NODE_SCALE)
        n2 = create_node("Sym 2", 3, "010", RED, pos_2, scale=NODE_SCALE)
        n3 = create_node("Sym 3", 4, "100", ORANGE, pos_3, scale=NODE_SCALE)

        self.play(FadeIn(n1["group"]), FadeIn(n2["group"]), FadeIn(n3["group"]))
        self.wait(1)

        # ==========================================
        # MERGE 1: Sym 1 (Min1) + Sym 2 (Min2)
        # ==========================================
        
        step1_txt = Text("Step 1: Merge Min1 (Sym1) & Min2 (Sym2)", font_size=28, color=TEAL).next_to(title, DOWN)
        self.play(Write(step1_txt))

        # 1. Highlight Children
        rect1 = SurroundingRectangle(n1["group"], color=YELLOW)
        rect2 = SurroundingRectangle(n2["group"], color=YELLOW)
        self.play(ShowCreation(rect1), ShowCreation(rect2))
        
        # 2. Logic Animation: Masks move to Parent Position
        calc_m1 = n1["mask"].copy()
        calc_m2 = n2["mask"].copy()
        
        self.play(
            calc_m1.animate.move_to(pos_grp1 + LEFT*1).scale(1.2),
            calc_m2.animate.move_to(pos_grp1 + RIGHT*1).scale(1.2)
        )
        
        or_txt = Text("|", font_size=30).move_to(pos_grp1)
        res_mask = Text("011", font_size=30, font="Consolas", color=PURPLE).move_to(pos_grp1 + DOWN*0.5)
        
        self.play(Write(or_txt))
        self.play(TransformFromCopy(VGroup(calc_m1, calc_m2), res_mask))
        self.wait(0.5)
        
        # 3. Spawn Parent Node (Group 1)
        # In Hardware: This is CNT[1] updated
        grp1 = create_node("Group 1", 5, "011", PURPLE, pos_grp1, scale=NODE_SCALE)
        
        self.play(
            FadeOut(calc_m1), FadeOut(calc_m2), FadeOut(or_txt), FadeOut(res_mask),
            FadeIn(grp1["group"])
        )
        
        # 4. Connect Tree (Draw Edges)
        edge1 = Line(grp1["circle"].get_bottom(), n1["circle"].get_top(), color=GREY)
        edge2 = Line(grp1["circle"].get_bottom(), n2["circle"].get_top(), color=GREY)
        
        # Add Edge Weights (The hardware logic: Winner=1, Loser=0)
        # Wait, hardware logic: Min1 (Winner) gets '1', Min2 (Loser) gets '0'
        w1 = Text("1", font_size=24, color=GREEN).move_to(edge1.get_center())
        w2 = Text("0", font_size=24, color=GREEN).move_to(edge2.get_center())

        self.play(ShowCreation(edge1), ShowCreation(edge2), Write(w1), Write(w2))
        
        # 5. Parallel Update of Leaves
        # Hardware loops through 1..8. 
        # If inside Winner Mask (Sym 1) -> Prepend 1
        # If inside Loser Mask (Sym 2) -> Prepend 0
        
        new_c1 = Text("Code: 1000", font_size=20, font="Consolas", color=GREEN).move_to(n1["code"].get_center())
        new_c2 = Text("Code: 0000", font_size=20, font="Consolas", color=GREEN).move_to(n2["code"].get_center())
        
        self.play(
            Transform(n1["code"], new_c1),
            Transform(n2["code"], new_c2),
            FadeOut(rect1), FadeOut(rect2)
        )
        self.wait(1)

        # ==========================================
        # MERGE 2: Sym 3 (Min1) + Group 1 (Min2)
        # ==========================================
        
        step2_txt = Text("Step 2: Merge Min1 (Sym3) & Min2 (Group1)", font_size=28, color=TEAL).next_to(title, DOWN)
        self.play(Transform(step1_txt, step2_txt))
        
        # 1. Highlight Candidates
        # Note: We highlight the ROOT of the group (grp1) and Sym 3
        rect3 = SurroundingRectangle(n3["group"], color=YELLOW)
        rect_grp = SurroundingRectangle(grp1["group"], color=YELLOW)
        self.play(ShowCreation(rect3), ShowCreation(rect_grp))
        
        # 2. Logic Animation: Masks move to Root Position
        calc_m3 = n3["mask"].copy()
        calc_m_grp = grp1["mask"].copy()
        
        self.play(
            calc_m3.animate.move_to(pos_root + RIGHT*1.5).scale(1.2),
            calc_m_grp.animate.move_to(pos_root + LEFT*1.5).scale(1.2)
        )
        
        or_txt2 = Text("|", font_size=30).move_to(pos_root)
        res_mask2 = Text("111", font_size=30, font="Consolas", color=GOLD).move_to(pos_root + DOWN*0.5)
        
        self.play(Write(or_txt2))
        self.play(TransformFromCopy(VGroup(calc_m3, calc_m_grp), res_mask2))
        
        # 3. Spawn Root Node
        root = create_node("ROOT", 9, "111", GOLD, pos_root, scale=NODE_SCALE)
        
        self.play(
            FadeOut(calc_m3), FadeOut(calc_m_grp), FadeOut(or_txt2), FadeOut(res_mask2),
            FadeIn(root["group"])
        )
        
        # 4. Connect Tree
        edge3 = Line(root["circle"].get_bottom(), n3["circle"].get_top(), color=GREY)
        edge_grp = Line(root["circle"].get_bottom(), grp1["circle"].get_top(), color=GREY)
        
        # Weights: Min1 (Sym 3) gets 1, Min2 (Group 1) gets 0
        w3 = Text("1", font_size=24, color=GREEN).move_to(edge3.get_center())
        w_grp = Text("0", font_size=24, color=GREEN).move_to(edge_grp.get_center())
        
        self.play(ShowCreation(edge3), ShowCreation(edge_grp), Write(w3), Write(w_grp))
        
        # 5. Parallel Update of Leaves
        # This is the "Magic" of node_group. 
        # Sym 3 (in Winner Mask) -> Prepend 1
        # Sym 1 & 2 (in Loser Mask) -> Prepend 0
        
        final_c3 = Text("Code: 1", font_size=20, font="Consolas", color=GREEN).move_to(n3["code"].get_center())
        final_c1 = Text("Code: 01", font_size=20, font="Consolas", color=GREEN).move_to(n1["code"].get_center())
        final_c2 = Text("Code: 00", font_size=20, font="Consolas", color=GREEN).move_to(n2["code"].get_center())
        
        # Also update intermediate group code just for visual consistency (though hardware doesn't store group codes)
        grp_c = Text("Code: 0000", font_size=20, font="Consolas", color=GREEN).move_to(grp1["code"].get_center())
        
        self.play(
            Transform(n3["code"], final_c3),
            Transform(n1["code"], final_c1),
            Transform(n2["code"], final_c2),
            Transform(grp1["code"], grp_c),
            FadeOut(rect3), FadeOut(rect_grp)
        )
        
        self.wait(2)
        
        # ==========================================
        # CONCLUSION
        # ==========================================
        self.play(FadeOut(step1_txt))
        
        final_lbl = Text("Completed Huffman Tree & Codes", font_size=32, color=GOLD).next_to(title, DOWN)
        self.play(Write(final_lbl))
        
        self.wait(3)
        
