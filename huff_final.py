from manimlib import *

class HuffmanHardware(Scene):
    def construct(self):
        # ==========================================
        # 1. SETUP & LAYOUT
        # ==========================================
        
        # Title
        title = Text("Huffman Hardware: Register Logic", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))

        # --- Data Structure for Hardware State ---
        # We simulate the hardware arrays here
        # Node indices: 0, 1, 2 (Mapped to Verilog 1, 2, 3)
        hw_data = [
            {"id": 1, "cnt": 2, "hc": "", "m": 0, "active": True},
            {"id": 2, "cnt": 3, "hc": "", "m": 0, "active": True},
            {"id": 3, "cnt": 4, "hc": "", "m": 0, "active": True},
        ]

        # --- Visual Elements: Register Table ---
        # We create a manual table to easily animate specific rows
        
        headers = VGroup(
            Text("Node", font_size=24, color=BLUE),
            Text("CNT (Freq)", font_size=24, color=YELLOW),
            Text("M (Len)", font_size=24, color=ORANGE),
            Text("HC (Code)", font_size=24, color=GREEN)
        ).arrange(RIGHT, buff=1.0)
        headers.to_edge(RIGHT, buff=1.0).shift(UP*1)
        
        # Lines for table
        h_line = Line(headers.get_left() + LEFT*0.2, headers.get_right() + RIGHT*0.2).next_to(headers, DOWN, buff=0.2)
        
        self.play(Write(headers), ShowCreation(h_line))

        # Row creation helper
        row_start_y = h_line.get_y() - 0.5
        
        def create_row_visuals(data_list):
            visual_rows = VGroup()
            for i, d in enumerate(data_list):
                y_pos = row_start_y - i * 0.8
                
                t_id = Text(f"#{d['id']}", font_size=24).move_to([headers[0].get_x(), y_pos, 0])
                t_cnt = Text(str(d['cnt']), font_size=24).move_to([headers[1].get_x(), y_pos, 0])
                t_m = Text(str(d['m']), font_size=24).move_to([headers[2].get_x(), y_pos, 0])
                # Display binary code or empty
                code_str = d['hc'] if d['hc'] else "-"
                t_hc = Text(code_str, font_size=24, font="Consolas").move_to([headers[3].get_x(), y_pos, 0])
                
                row_grp = VGroup(t_id, t_cnt, t_m, t_hc)
                visual_rows.add(row_grp)
            return visual_rows

        row_visuals = create_row_visuals(hw_data)
        self.play(FadeIn(row_visuals))

        # --- Visual Elements: Tree Nodes (Left Side) ---
        tree_origin = LEFT * 4 + DOWN * 2.5
        
        # Initial Leaf Positions
        leaf_nodes = VGroup()
        pos_map = {
            1: tree_origin + LEFT * 2,
            2: tree_origin,
            3: tree_origin + RIGHT * 2
        }
        
        node_circles = {} # Store circle objects to draw lines later

        for item in hw_data:
            c = Circle(radius=0.5, color=BLUE, fill_opacity=0.2).move_to(pos_map[item['id']])
            lbl = Text(str(item['cnt']), font_size=32).move_to(c)
            idx = Text(f"#{item['id']}", font_size=20, color=BLUE_B).next_to(c, DOWN)
            
            grp = VGroup(c, lbl, idx)
            leaf_nodes.add(grp)
            node_circles[item['id']] = c

        self.play(ShowCreation(leaf_nodes))
        self.wait(1)

        # ==========================================
        # ANIMATION HELPER: UPDATE ROW
        # ==========================================
        def animate_register_update(idx_list, new_data_list):
            # idx_list: list of row indices (0 to 2) to update
            # new_data_list: list of full data dicts
            
            anims = []
            new_rows_v = create_row_visuals(new_data_list)
            replacements = {}  # Store (row_idx, new_text_mobj) for cleanup
            
            for row_idx in idx_list:
                old_row = row_visuals[row_idx]
                new_row = new_rows_v[row_idx]
                
                # Highlight effect
                rect = SurroundingRectangle(old_row, color=YELLOW)
                anims.append(ShowCreationThenDestruction(rect))
                
                # Update underlying data reference immediately
                old_data = hw_data[row_idx]
                new_data = new_data_list[row_idx]
                
                # 1. Transform non-HC columns (ID, CNT, M)
                # Structure: 0=ID, 1=CNT, 2=M, 3=HC
                for i in range(3):
                    anims.append(Transform(old_row[i], new_row[i]))

                # 2. Handle HC Column
                old_hc_str = old_data['hc']
                new_hc_str = new_data['hc']
                
                # Check for append condition: Old is prefix of New, and New is longer
                is_append = (old_hc_str and new_hc_str and 
                             new_hc_str.startswith(old_hc_str) and 
                             len(new_hc_str) > len(old_hc_str))
                
                if is_append:
                    # Append Logic: Transform prefix, Fly In suffix
                    split_idx = len(old_hc_str)
                    target_hc = new_row[3]
                    
                    target_prefix = target_hc[:split_idx]
                    target_suffix = target_hc[split_idx:]
                    
                    # Transform old text to match the new prefix's position/style
                    anims.append(Transform(old_row[3], target_prefix))
                    
                    # Fly in the new suffix from the right (moving LEFT)
                    anims.append(FadeIn(target_suffix, shift=LEFT, run_time=2))
                    
                    # Mark for cleanup
                    replacements[row_idx] = target_hc
                else:
                    # Standard Transform
                    anims.append(Transform(old_row[3], new_row[3]))
                
                # Update main data list
                hw_data[row_idx] = new_data_list[row_idx]
            
            self.play(*anims)
            
            # Post-animation cleanup: Ensure row_visuals points to the correct new objects
            for r_idx, new_text_obj in replacements.items():
                row_grp = row_visuals[r_idx]
                old_text_obj = row_grp[3]
                
                # Swap in the clean new object
                row_grp.remove(old_text_obj)
                row_grp.add(new_text_obj)
                self.add(new_text_obj)  # Ensure it's in the scene

        # ==========================================
        # ITERATION 1
        # ==========================================
        # Logic: Compare #1(2) and #2(3) -> Min1=#1, Min2=#2
        
        iter1_text = Text("Iteration 1: Find 2 Smallest", font_size=28, color=YELLOW).to_edge(LEFT).shift(UP*2.5)
        self.play(Write(iter1_text))
        
        # 1. Highlight Min1 and Min2 in Table
        rect_min1 = SurroundingRectangle(row_visuals[0], color=GREEN) # Node 1
        rect_min2 = SurroundingRectangle(row_visuals[1], color=RED)   # Node 2
        label_min1 = Text("Min1 (Small)", font_size=20, color=GREEN).next_to(rect_min1, LEFT)
        label_min2 = Text("Min2 (Big)", font_size=20, color=RED).next_to(rect_min2, LEFT)
        
        self.play(
            ShowCreation(rect_min1), Write(label_min1),
            ShowCreation(rect_min2), Write(label_min2)
        )
        self.wait(0.5)

        # 2. Hardware Logic Description
        logic_text = Text(
            "Min1 (2) gets bit '1'\nMin2 (3) gets bit '0'", 
            font_size=24, color=WHITE
        ).next_to(iter1_text, DOWN, buff=0.3)
        self.play(Write(logic_text))

        # 3. Perform Merge (Update Registers)
        # Node 1: HC becomes "1", M becomes 1, CNT dies (0xFF)
        # Node 2: HC stays (adds 0 implicitly), M becomes 1, CNT becomes 2+3=5
        
        new_data = [d.copy() for d in hw_data]
        
        # Update Min1 (#1)
        new_data[0]['cnt'] = "0xFF" # 0xFF
        new_data[0]['m'] = 1
        new_data[0]['hc'] = "1"
        new_data[0]['active'] = False
        
        # Update Min2 (#2) -> Becomes Parent
        new_data[1]['cnt'] = 5
        new_data[1]['m'] = 1
        new_data[1]['hc'] = "0" # Actually remains 0 in value, but length 1
        
        self.play(FadeOut(logic_text))

        # Addition Animation: 2 (from #1) moves to 3 (at #2)
        add_src = row_visuals[0][1].copy()
        add_dst = row_visuals[1][1]
        
        # Create text "2+3"
        add_text = Text(f"{hw_data[0]['cnt']}+{hw_data[1]['cnt']}", font_size=24, color=YELLOW)
        add_text.move_to(add_dst.get_center())
        
        self.play(add_src.animate.move_to(add_dst.get_center()), run_time=0.8)
        self.play(Transform(add_src, add_text), FadeOut(add_dst))
        self.wait(0.5)
        self.remove(add_src, add_text)
        self.add(add_dst) # Restore original before update transforms it

        animate_register_update([0, 1], new_data)
        
        # 4. Visual Tree Merge
        # New parent node at position between 1 and 2
        p1_pos = pos_map[1] + UP * 1.5 + RIGHT * 1
        parent1 = Circle(radius=0.6, color=PURPLE, fill_opacity=0.2).move_to(p1_pos)
        p1_lbl = Text("5", font_size=32).move_to(parent1)
        p1_grp = VGroup(parent1, p1_lbl)
        
        # Reuse Node 2 ID visually
        p1_idx = Text("#2 (Merged)", font_size=20, color=PURPLE).next_to(parent1, UP)
        
        l1 = Line(parent1.get_bottom(), node_circles[1].get_top(), color=GREEN)
        l2 = Line(parent1.get_bottom(), node_circles[2].get_top(), color=RED)
        t_1 = Text("1", font_size=22, color=GREEN).move_to(l1.get_center()+LEFT*0.3)
        t_0 = Text("0", font_size=22, color=RED).move_to(l2.get_center()+RIGHT*0.3)
        
        bg_1 = SurroundingRectangle(t_1, color=BLACK, fill_opacity=0.7, buff=0.05).set_stroke(width=0)
        bg_0 = SurroundingRectangle(t_0, color=BLACK, fill_opacity=0.7, buff=0.05).set_stroke(width=0)
        t_1.add_to_back(bg_1)
        t_0.add_to_back(bg_0)
        
        self.play(
            ShowCreation(l1), ShowCreation(l2), 
            FadeIn(p1_grp), Write(p1_idx),
            FadeIn(t_1, scale=3), FadeIn(t_0, scale=3),
            FadeOut(rect_min1), FadeOut(rect_min2), FadeOut(label_min1), FadeOut(label_min2)
        )
        
        # Update map for next round
        node_circles[2] = parent1 # Node 2 is now represented by this parent
        
        self.wait(1)

        # ==========================================
        # ITERATION 2
        # ==========================================
        # Active Nodes: #2 (Freq 5), #3 (Freq 4)
        # Compare: 4 < 5. Min1 = #3, Min2 = #2
        
        iter2_text = Text("Iteration 2: #3(4) vs #2(5)", font_size=28, color=YELLOW).to_edge(LEFT).shift(UP*2.5)
        self.play(Transform(iter1_text, iter2_text))
        
        # 1. Highlight
        rect_min1 = SurroundingRectangle(row_visuals[2], color=GREEN) # Node 3 (Row index 2)
        rect_min2 = SurroundingRectangle(row_visuals[1], color=RED)   # Node 2 (Row index 1)
        label_min1 = Text("Min1 (Small)", font_size=20, color=GREEN).next_to(rect_min1, LEFT)
        label_min2 = Text("Min2 (Big)", font_size=20, color=RED).next_to(rect_min2, LEFT)
        
        self.play(
            ShowCreation(rect_min1), Write(label_min1),
            ShowCreation(rect_min2), Write(label_min2)
        )
        
        # 2. Logic Update
        # Min1 (#3): Gets '1'.
        # Min2 (#2): Gets '0'. Warning: This affects all children of #2 (Original #1 and #2)
        # Hardware: loops i=1..8. 
        #   If in group 1 (#1 is in group #2 now? No, group merge logic: group[min2] |= group[min1])
        #   So Group #2 contains {1, 2}. Now Group #2 merges with #3.
        #   The winner is #3. The loser is #2 (Group {1,2}).
        
        # Update Data
        new_data_2 = [d.copy() for d in hw_data]
        
        # Min1 (#3) updates
        new_data_2[2]['cnt'] = "0xFF"
        new_data_2[2]['m'] = 1
        new_data_2[2]['hc'] = "1"
        
        # Min2 (#2) updates - This represents the ROOT now
        new_data_2[1]['cnt'] = 9
        # IMPORTANT: Hardware updates ALL nodes belonging to the group
        
        # Node #3 (Winner Side):
        # Already set above.
        
        # Node #2 (Loser Side - Group):
        # The hardware iterates.
        # Original #1: Was in Group #2. Gets 0 added. Old HC="1". New HC="10" (visual order). M=2.
        # Original #2: Was in Group #2. Gets 0 added. Old HC="0". New HC="00". M=2.
        
        # Manually set the final register states for visualization
        new_data_2[0]['m'] = 2
        new_data_2[0]['hc'] = "10" # Logic: Old Code + 0 (appended)
        
        new_data_2[1]['m'] = 2
        new_data_2[1]['hc'] = "00"
        
        # self.play(FadeOut(logic_text)) # Clear old text
        logic_text_2 = Text("ALL in Group #2 -> add 0", font_size=24).next_to(iter1_text, DOWN, buff=0.3)
        logic_text_2p = Text("#3->add 1", font_size=24).next_to(logic_text_2, DOWN, buff=0.2)
        logic_text_2_group = VGroup(logic_text_2, logic_text_2p);
        logic_text_2_group.shift(RIGHT*0.5)
        self.play(Write(logic_text_2_group))
        self.wait(2)
        
        # Addition Animation: 4 (from #3) moves to 5 (at #2)
        add_src_2 = row_visuals[2][1].copy()
        add_dst_2 = row_visuals[1][1]
        
        # Create text "4+5"
        add_text_2 = Text(f"{hw_data[2]['cnt']}+{new_data[1]['cnt']}", font_size=24, color=YELLOW)
        add_text_2.move_to(add_dst_2.get_center())
        
        self.play(add_src_2.animate.move_to(add_dst_2.get_center()), run_time=0.8)
        self.play(Transform(add_src_2, add_text_2), FadeOut(add_dst_2))
        self.wait(0.5)
        self.remove(add_src_2, add_text_2)
        self.add(add_dst_2)

        # We update all 3 rows because #1 is inside group #2 and gets updated too
        animate_register_update([0, 1, 2], new_data_2)
        
        # 3. Visual Tree Merge (Root)
        root_pos = parent1.get_center() + UP * 1.5 + RIGHT * 1
        root_node = Circle(radius=0.7, color=GOLD, fill_opacity=0.2).move_to(root_pos)
        root_lbl = Text("9", font_size=32).move_to(root_node)
        # root_idx = Text("ROOT", font_size=20, color=GOLD).next_to(root_node, UP)
        
        r_grp = VGroup(root_node, root_lbl)
        
        l3 = Line(root_node.get_bottom(), node_circles[3].get_top(), color=GREEN) # To #3
        l_grp = Line(root_node.get_bottom(), node_circles[2].get_top(), color=RED) # To #2 (Parent1)
        
        t_3_val = Text("1", font_size=20, color=GREEN).move_to(l3.get_center()+RIGHT*0.3)
        t_grp_val = Text("0", font_size=20, color=RED).move_to(l_grp.get_center()+LEFT*0.3)
        
        bg_3 = SurroundingRectangle(t_3_val, color=BLACK, fill_opacity=0.7, buff=0.05).set_stroke(width=0)
        bg_grp = SurroundingRectangle(t_grp_val, color=BLACK, fill_opacity=0.7, buff=0.05).set_stroke(width=0)
        t_3_val.add_to_back(bg_3)
        t_grp_val.add_to_back(bg_grp)
        
        self.play(
            ApplyMethod(p1_idx.shift, LEFT * 0.5),
            ShowCreation(l3), ShowCreation(l_grp),
            FadeIn(r_grp),
            Write(t_3_val), Write(t_grp_val),
            FadeOut(rect_min1), FadeOut(rect_min2), FadeOut(label_min1), FadeOut(label_min2)
        )
        
        self.wait(2)

        # ==========================================
        # FINAL RESULT
        # ==========================================
        final_box = SurroundingRectangle(row_visuals, color=WHITE)
        final_txt = Text("Final Output Registers", font_size=30).next_to(final_box, DOWN)
        
        self.play(
            FadeOut(iter1_text), FadeOut(logic_text_2_group),
            ShowCreation(final_box), Write(final_txt)
        )
        
        self.wait(2)
