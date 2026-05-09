import tkinter as tk
from tkinter import ttk, messagebox
import socket
import json
import os
import ctypes
import time

def copy_to_clipboard(text):
    try:
        ctypes.windll.user32.OpenClipboard(0)
        ctypes.windll.user32.EmptyClipboard()
        ctypes.windll.user32.SetClipboardData(13, text.encode('utf-16-le'))
        ctypes.windll.user32.CloseClipboard()
    except:
        pass

def send_server(data):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect(("127.0.0.1", 11262))
        s.send(json.dumps(data).encode())
        res = s.recv(8192).decode()
        s.close()
        return json.load(res)
    except:
        return None

def write_registry():
    try:
        key = ctypes.HKEY_CURRENT_USER
        path = r"Software\HubFlow"
        ctypes.windll.advapi32.RegCreateKeyW(key, path, ctypes.byref(ctypes.HKEY()))
    except:
        pass

LANG = {
    "en": {
        "welcome": "Welcome to HubFlow Setup",
        "welcome_desc1": "This wizard will install HubFlow to your computer.",
        "welcome_desc2": "Please click Next to continue.",
        "verify_title": "Account Verification",
        "email": "Registered Email:",
        "code": "Verification Code:",
        "get_code": "Get Code",
        "no_buy_install_free": "Not purchased, install Free version directly",
        "ver_select_title": "Select Version Edition",
        "ver_pro": "HubFlow v1.2.1 Pro (Recommended)",
        "ver_normal": "HubFlow v1.2.1",
        "ver_free_disable": "HubFlow v1.2.1-free (Purchased Official Edition)",
        "install_path": "Install Path:",
        "installing": "Installing HubFlow, please wait...",
        "install_complete": "Installation Completed",
        "complete_tip": "HubFlow has been installed successfully.",
        "next": "Next",
        "back": "Back",
        "finish": "Finish",
        "code_copied": "Code copied to clipboard",
        "code_fail": "Failed to get code",
        "must_verify_code": "Please complete verification first before next step",
    },
    "zh": {
        "welcome": "欢迎使用 HubFlow 安装向导",
        "welcome_desc1": "该向导将把 HubFlow 安装到您的计算机中。",
        "welcome_desc2": "请点击下一步继续。",
        "verify_title": "账户验证",
        "email": "注册邮箱：",
        "code": "验证码：",
        "get_code": "获取验证码",
        "no_buy_install_free": "未购买产品，直接安装免费版",
        "ver_select_title": "选择安装版本",
        "ver_pro": "HubFlow v1.2.1 Pro（推荐）",
        "ver_normal": "HubFlow v1.2.1",
        "ver_free_disable": "HubFlow v1.2.1-free（已购买正式版）",
        "install_path": "安装路径：",
        "installing": "正在安装 HubFlow，请稍候...",
        "install_complete": "安装完成",
        "complete_tip": "HubFlow 已成功安装至您的电脑。",
        "next": "下一步",
        "back": "上一步",
        "finish": "完成",
        "code_copied": "验证码已复制到剪贴板",
        "code_fail": "获取验证码失败",
        "must_verify_code": "必须完成验证码验证才能进入下一步",
    }
}

class HubFlowSetup:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HubFlow v1.2.1 Setup")
        self.root.geometry("680x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")

        self.step = 0
        self.cur_lang = "zh"
        self.has_verified = False
        self.is_purchased = True
        self.select_ver = tk.StringVar(value="pro")
        self.is_free_flow = False

        self.header = tk.Frame(self.root, height=90, bg="white")
        self.header.pack(fill=tk.X)
        try:
            self.logo_img = tk.PhotoImage(file="install_logo.png")
            tk.Label(self.header, image=self.logo_img, bg="white", bd=0).pack()
        except:
            tk.Label(self.header, text="HubFlow Installer", font=("Arial", 18, "bold"), bg="white").pack(pady=25)

        self.main_frame = tk.Frame(self.root, bg="white", width=680, height=340)
        self.main_frame.place(x=0, y=90)

        self.footer = tk.Frame(self.root, bg="#f0f0f0", height=70)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

        self.btn_back = ttk.Button(self.footer, text=self.t("back"), state=tk.DISABLED, command=self.go_prev)
        self.btn_back.place(x=20, y=20, width=100)

        self.btn_next = ttk.Button(self.footer, text=self.t("next"), command=self.go_next)
        self.btn_next.place(x=560, y=20, width=100)

        self.render_step0()

    def t(self, key):
        return LANG[self.cur_lang].get(key, key)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def render_step0(self):
        self.clear_main()
        tk.Label(self.main_frame, text=self.t("welcome"), font=("Arial", 15, "bold"), bg="white").place(x=30, y=30)
        tk.Label(self.main_frame, text=self.t("welcome_desc1"), bg="white").place(x=30, y=80)
        tk.Label(self.main_frame, text=self.t("welcome_desc2"), bg="white").place(x=30, y=110)
        tk.Label(self.main_frame, text="Language / 语言", bg="white").place(x=480, y=25)
        lang_box = ttk.Combobox(self.main_frame, values=["zh", "en"], width=8, state="readonly")
        lang_box.place(x=580, y=25)
        lang_box.set(self.cur_lang)
        lang_box.bind("<<ComboboxSelected>>", lambda e: self.switch_lang(lang_box.get()))

    def switch_lang(self, lang):
        self.cur_lang = lang
        self.btn_back.config(text=self.t("back"))
        self.btn_next.config(text=self.t("next"))
        self.render_step0()

    def render_step1(self):
        self.clear_main()
        tk.Label(self.main_frame, text=self.t("verify_title"), font=("Arial",15,"bold"), bg="white").place(x=30,y=30)
        tk.Label(self.main_frame, text=self.t("email"), bg="white").place(x=40,y=100)
        self.var_email = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.var_email).place(x=180,y=100,width=380)
        tk.Label(self.main_frame, text=self.t("code"), bg="white").place(x=40,y=160)
        self.var_code = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.var_code).place(x=180,y=160,width=260)
        ttk.Button(self.main_frame, text=self.t("get_code"), command=self.get_verify_code).place(x=450,y=160,width=110)
        self.label_status = tk.Label(self.main_frame, text="", fg="green", bg="white")
        self.label_status.place(x=180,y=200)
        ttk.Button(self.main_frame, text=self.t("no_buy_install_free"), command=self.install_free_direct).place(x=180,y=240,width=380)

    def render_step2(self):
        self.clear_main()
        tk.Label(self.main_frame, text=self.t("ver_select_title"), font=("Arial",15,"bold"), bg="white").place(x=30,y=30)
        ttk.Radiobutton(self.main_frame, text=self.t("ver_pro"), variable=self.select_ver, value="pro").place(x=40,y=100)
        ttk.Radiobutton(self.main_frame, text=self.t("ver_normal"), variable=self.select_ver, value="normal").place(x=40,y=140)
        ttk.Radiobutton(self.main_frame, text=self.t("ver_free_disable"), state=tk.DISABLED).place(x=40,y=180)

    def render_step3(self):
        self.clear_main()
        tk.Label(self.main_frame, text=self.t("install_path"), font=("Arial",15,"bold"), bg="white").place(x=30,y=30)
        self.install_path = tk.StringVar(value=os.path.expanduser("~\\HubFlow"))
        ttk.Entry(self.main_frame, textvariable=self.install_path).place(x=40,y=100,width=580)

    def render_step4(self):
        self.clear_main()
        tk.Label(self.main_frame, text=self.t("installing"), font=("Arial",14), bg="white").place(x=30,y=30)
        pbar = ttk.Progressbar(self.main_frame, length=580, mode="indeterminate")
        pbar.place(x=40,y=120,height=25)
        pbar.start(10)
        self.root.update()
        self.do_install_task()

    def render_step5(self):
        self.clear_main()
        tk.Label(self.main_frame, text=self.t("install_complete"), font=("Arial",16,"bold"), bg="white", fg="#080").place(x=30,y=80)
        tk.Label(self.main_frame, text=self.t("complete_tip"), bg="white").place(x=30,y=130)
        self.btn_next.config(text=self.t("finish"), command=self.root.destroy)

    def get_verify_code(self):
        email = self.var_email.get().strip()
        if not email: return
        self.label_status.config(text="Getting code...")
        self.root.update()
        res = send_server({"act":"send_code","email":email})
        if res and res.get("status")=="ok":
            code = res.get("code")
            self.var_code.set(code)
            copy_to_clipboard(code)
            self.label_status.config(text=self.t("code_copied"), fg="green")
            self.has_verified = True
        else:
            self.label_status.config(text=self.t("code_fail"), fg="red")

    def install_free_direct(self):
        self.is_free_flow = True
        self.step = 3
        self.select_ver.set("free")
        self.render_step3()
        self.btn_back.config(state=tk.DISABLED)

    def do_install_task(self):
        path = self.install_path.get()
        os.makedirs(path, exist_ok=True)
        time.sleep(0.5)
        write_registry()
        ver = self.select_ver.get()
        with open(os.path.join(path,"core.py"),"w",encoding="utf-8") as f:
            f.write(f'# HubFlow {ver}\n__version__="1.2.1"\n__edition__="{ver}"\n')
        time.sleep(0.5)
        self.step =5
        self.render_step5()

    def go_prev(self):
        if self.is_free_flow: return
        if self.step>0:
            self.step -=1
            self.render_current_step()

    def go_next(self):
        if self.step ==1 and not self.has_verified:
            messagebox.showwarning("", self.t("must_verify_code"))
            return
        self.step +=1
        self.render_current_step()

    def render_current_step(self):
        steps = [self.render_step0,self.render_step1,self.render_step2,self.render_step3,self.render_step4,self.render_step5]
        steps[self.step]()
        if self.is_free_flow:
            self.btn_back.config(state=tk.DISABLED)
        else:
            self.btn_back.config(state=tk.NORMAL if self.step>0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.step<4 else tk.DISABLED)
        self.btn_back.config(text=self.t("back"))
        self.btn_next.config(text=self.t("next"))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    HubFlowSetup().run()
