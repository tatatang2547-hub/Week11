import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class RegExApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Python RegEx Explorer (GUI)")
        self.root.geometry("900x700")

        # ---------------- Section 1: Top Toolbar (Load File) ----------------
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill=tk.X)

        self.btn_load = ttk.Button(
            top_frame, text="📁 โหลดไฟล์ Text", command=self.load_file
        )
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.lbl_file_status = ttk.Label(
            top_frame, text="ยังไม่ได้เลือกไฟล์", foreground="gray"
        )
        self.lbl_file_status.pack(side=tk.LEFT, padx=5)

        # ---------------- Section 2: Input Area ----------------
        input_frame = ttk.LabelFrame(
            root, text=" ข้อความต้นทาง (Input Text) ", padding=10
        )
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.txt_input = tk.Text(input_frame, height=8, wrap=tk.WORD)
        self.txt_input.pack(fill=tk.BOTH, expand=True)

        # ใส่ข้อความเริ่มต้นสำหรับทดสอบ
        sample_text = (
            "Contact info: john.doe@email.com, alice_123@work.org\n"
            "Call us: 081-234-5678 or 02-999-8888\n"
            "Order ID: #ORD-2026-991, #ORD-2026-992\n"
            "Date: 2026-09-16"
        )
        self.txt_input.insert(tk.END, sample_text)

        # ---------------- Section 3: Control Panel (Regex Controls) ----------------
        ctrl_frame = ttk.LabelFrame(
            root, text=" ตั้งค่าและเลือกฟังก์ชัน RegEx ", padding=10
        )
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)

        # เลือก Function
        ttk.Label(ctrl_frame, text="ฟังก์ชัน re:").grid(
            row=0, column=0, sticky=tk.W, padx=5
        )
        self.func_var = tk.StringVar()
        self.combo_func = ttk.Combobox(
            ctrl_frame, textvariable=self.func_var, state="readonly", width=18
        )
        self.combo_func["values"] = (
            "1. re.findall",
            "2. re.search",
            "3. re.match",
            "4. re.finditer",
            "5. re.sub",
            "6. re.subn",
            "7. re.split",
            "8. re.compile",
            "9. re.fullmatch",
            "10. re.escape",
        )
        self.combo_func.current(0)
        self.combo_func.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Input Parameter: Pattern
        ttk.Label(ctrl_frame, text="Pattern (Regex):").grid(
            row=0, column=2, sticky=tk.W, padx=5
        )
        self.ent_pattern = ttk.Entry(ctrl_frame, width=25)
        self.ent_pattern.insert(0, r"\w+@\w+\.\w+")  # ค้นหา Email
        self.ent_pattern.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        # Input Parameter: Replacement / Flags
        ttk.Label(ctrl_frame, text="Replace text:").grid(
            row=1, column=0, sticky=tk.W, padx=5
        )
        self.ent_replace = ttk.Entry(ctrl_frame, width=20)
        self.ent_replace.insert(0, "[REDACTED]")
        self.ent_replace.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Checkbox Flags
        self.var_ignorecase = tk.BooleanVar()
        self.chk_icase = ttk.Checkbutton(
            ctrl_frame, text="IGNORECASE (i)", variable=self.var_ignorecase
        )
        self.chk_icase.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)

        # ปุ่มประมวลผล
        self.btn_process = ttk.Button(
            ctrl_frame, text="⚡ ประมวลผล", command=self.process_regex
        )
        self.btn_process.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)

        # ---------------- Section 4: Output Area ----------------
        output_frame = ttk.LabelFrame(
            root, text=" ผลลัพธ์การค้นหา/กรองข้อมูล (Output) ", padding=10
        )
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.txt_output = tk.Text(
            output_frame, height=10, wrap=tk.WORD, bg="#f4f4f4"
        )
        self.txt_output.pack(fill=tk.BOTH, expand=True)

    # ---------------- Logics & Handlers ----------------
    def load_file(self):
        """โหลดข้อความจากไฟล์ .txt"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.txt_input.delete("1.0", tk.END)
                    self.txt_input.insert(tk.END, content)
                self.lbl_file_status.config(
                    text=f"โหลดไฟล์สำเร็จ: {os.path.basename(file_path)}",
                    foreground="green",
                )
            except Exception as e:
                messagebox.showerror(
                    "Error", f"ไม่สามารถอ่านไฟล์ได้:\n{str(e)}"
                )

    def process_regex(self):
        """ประมวลผลคำสั่ง Regex โดยใช้ Try-Except ดักจับ Error"""
        self.txt_output.delete("1.0", tk.END)

        text_in = self.txt_input.get("1.0", tk.END).strip()
        pattern_str = self.ent_pattern.get()
        replace_str = self.ent_replace.get()
        selected_func = self.func_var.get()

        # ตั้งค่า Flags
        flags = re.IGNORECASE if self.var_ignorecase.get() else 0

        # จัดการ Try-Except ป้องกัน Pattern ผิด語法 หรือ Runtime Exception
        try:
            result_output = ""

            # 1. re.findall: ค้นหาคำที่เข้าเงื่อนไขทั้งหมด คืนค่าเป็น List
            if "1. re.findall" in selected_func:
                res = re.findall(pattern_str, text_in, flags=flags)
                result_output = (
                    f"--- re.findall ---\nจำนวนที่พบ: {len(res)}\nรายการที่พบ:\n{res}"
                )

            # 2. re.search: ค้นหาจุดแรกที่ตรงกัน คืนค่า Match Object
            elif "2. re.search" in selected_func:
                match = re.search(pattern_str, text_in, flags=flags)
                if match:
                    result_output = f"--- re.search ---\nพบที่ตำแหน่ง Span: {match.span()}\nข้อความที่เจอ: '{match.group()}'"
                else:
                    result_output = "--- re.search ---\nไม่พบข้อความที่ตรงตาม Pattern"

            # 3. re.match: ค้นหาเฉพาะช่วงเริ่มต้นของข้อความเท่านั้น
            elif "3. re.match" in selected_func:
                match = re.match(pattern_str, text_in, flags=flags)
                if match:
                    result_output = f"--- re.match ---\nพบที่จุดเริ่มต้น! ข้อความ: '{match.group()}'"
                else:
                    result_output = "--- re.match ---\nไม่พบข้อมูลตรงกับ Pattern ที่ 'เริ่มต้น' ของข้อความ"

            # 4. re.finditer: ค้นหาแบบส่งคืน Iterator ของ Match Object
            elif "4. re.finditer" in selected_func:
                matches = list(re.finditer(pattern_str, text_in, flags=flags))
                result_output = f"--- re.finditer ---\nพบทั้งหมด {len(matches)} ตำแหน่ง:\n"
                for i, m in enumerate(matches, 1):
                    result_output += f"{i}. Match: '{m.group()}' ที่ช่วง index {m.span()}\n"

            # 5. re.sub: แทนที่ข้อความด้วยคำใหม่
            elif "5. re.sub" in selected_func:
                res_text = re.sub(
                    pattern_str, replace_str, text_in, flags=flags
                )
                result_output = (
                    f"--- re.sub ---\nข้อความหลังการแทนที่:\n\n{res_text}"
                )

            # 6. re.subn: แทนที่ข้อความพร้อมส่งคืน Tuple (ข้อความใหม่, จำนวนที่แทนที่)
            elif "6. re.subn" in selected_func:
                res_text, count = re.subn(
                    pattern_str, replace_str, text_in, flags=flags
                )
                result_output = f"--- re.subn ---\nจำนวนจุดที่เปลี่ยน: {count}\n\nข้อความหลังแทนที่:\n{res_text}"

            # 7. re.split: ตัดข้อความตาม Pattern
            elif "7. re.split" in selected_func:
                res_list = re.split(pattern_str, text_in, flags=flags)
                result_output = f"--- re.split ---\nตัดได้ทั้งหมด {len(res_list)} ส่วน:\n{res_list}"

            # 8. re.compile: คอมไพล์ Pattern แล้วนำไปใช้ (เพิ่มประสิทธิภาพ)
            elif "8. re.compile" in selected_func:
                compiled_pattern = re.compile(pattern_str, flags=flags)
                res = compiled_pattern.findall(text_in)
                result_output = f"--- re.compile + findall ---\n[ใช้ Pattern Object] ผลลัพธ์การค้นหา:\n{res}"

            # 9. re.fullmatch: ตรวจสอบว่าทั้งข้อความตรงตาม Pattern เป๊ะๆ หรือไม่
            elif "9. re.fullmatch" in selected_func:
                match = re.fullmatch(pattern_str, text_in, flags=flags)
                if match:
                    result_output = f"--- re.fullmatch ---\nข้อความทั้งหมดยาวตรงกับ Pattern แบบ 100%"
                else:
                    result_output = f"--- re.fullmatch ---\nข้อความทั้งหมด 'ไม่ตรง' ตาม Pattern แบบสมบูรณ์"

            # 10. re.escape: ใส่ Escape Sequence ให้ตัวอักษรพิเศษอัตโนมัติ
            elif "10. re.escape" in selected_func:
                escaped = re.escape(pattern_str)
                result_output = f"--- re.escape ---\nแปลงข้อความในช่อง Pattern ป้องกันอักขระพิเศษ:\n{escaped}"

            self.txt_output.insert(tk.END, result_output)

        except re.error as e:
            # จับ Error กรณีผู้ใช้ป้อน Regex Syntax ผิดพลาด
            err_msg = (
                f"[RegEx Syntax Error]\nรูปแบบ Pattern ไม่ถูกต้อง:\n{str(e)}"
            )
            self.txt_output.insert(tk.END, err_msg)
            messagebox.showwarning(
                "RegEx Error", "รูปแบบ Pattern ไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง"
            )

        except Exception as e:
            # จับ Error ทั่วไปอื่นๆ
            err_msg = f"[Runtime Error]\nเกิดข้อผิดพลาด: {str(e)}"
            self.txt_output.insert(tk.END, err_msg)


if __name__ == "__main__":
    root = tk.Tk()
    app = RegExApp(root)
    root.mainloop()