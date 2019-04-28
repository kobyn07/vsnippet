# -*- cording: utf-8 -*-
"""
Visual Studio Code のコードスニペットを簡単に作成するツール
"""

import tkinter as tk
import pyperclip


class Application(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("vsnippet")
        self.master.geometry("1075x500")

        self.prefix = ""
        self.description = ""
        self.body = ""
        self.covted_json = ""
        self.widget()

    def widget(self):
        "見た目の部分"
        # prefix の入力
        prefix_ttl = tk.Label(self, text="prefix")
        prefix_ttl.grid(row=0, column=0, sticky=tk.E)
        self.prefix_ent = tk.Entry(self, width=40)
        self.prefix_ent.grid(row=0, column=1, padx=10, pady=10)

        # description の入力
        desc_ttl = tk.Label(self, text="description")
        desc_ttl.grid(row=1, column=0, sticky=tk.E)
        self.desc_ent = tk.Entry(self, width=40)
        self.desc_ent.grid(row=1, column=1, padx=10, pady=10)

        # body の入力
        body_ttl = tk.Label(self, text="body")
        body_ttl.grid(row=2, column=0, padx=10, pady=10)
        self.body_txt = tk.Text(self, width=50, wrap=tk.NONE)
        self.body_txt.grid(row=3, column=0, padx=15)

        # body の整形出力
        covted_ttl = tk.Label(self, text="出力")
        covted_ttl.grid(row=2, column=2, padx=30, pady=10)
        self.covted_txt = tk.Text(self, width=50, wrap=tk.NONE)
        self.covted_txt.grid(row=3, column=2, padx=15)

        # 変換ボタン
        covt_btn = tk.Button(self, text="変換", padx=20, pady=20,
                             font=(10), command=self.clicked_on_convert_button)
        covt_btn.grid(row=3, column=1)

        # クリップボードにコピーするかどうかのチェックボックス
        self.clip_bool = tk.BooleanVar()
        self.clip_bool.set(True)
        clip_btn = tk.Checkbutton(
            self, variable=self.clip_bool, text="クリップボードにコピーする")
        clip_btn.grid(row=4, sticky=tk.W)

        # 消去ボタン
        self.clr_btn = tk.Button(
            self, text="消去", command=self.clicked_on_clear_button)
        self.clr_btn.grid(row=4, column=1)

    def clicked_on_convert_button(self):
        "変換ボタンを押したときの挙動"

        # 出力するテキストボックスを初期化する
        self.init_txt(self.covted_txt)

        # テキストボックスから文字列を取得する
        self.prefix = self.prefix_ent.get()
        self.description = self.desc_ent.get()
        self.body = self.body_txt.get("1.0", "end-1c")

        # body を整形する
        body_list = self.body.split("\n")
        for i, line in enumerate(body_list):
            body_list[i] = "\"" + line + "\","

        self.body = "\n\t\t".join(body_list)
        self.body = self.body.replace("\\", "\\\\").replace("\t", "    ")

        # json 形式に整形する
        self.covted_json = """\"{}\": {{
    \"prefix\": \"{}\",
    \"description\": \"{}\",
    \"body": [
        {}
    ],
}},""".format(self.prefix.capitalize(), self.prefix, self.description, self.body)

        # 整形したものを出力する
        self.covted_txt.insert("1.0", self.covted_json)

        # クリップボードにコピーする
        if self.clip_bool.get():
            pyperclip.copy(self.covted_json)

    def clicked_on_clear_button(self):
        "消去ボタンを押したときの挙動"
        self.init_txt(self.body_txt)
        self.init_txt(self.covted_txt)
        self.init_ent(self.desc_ent)
        self.init_ent(self.prefix_ent)

    def init_txt(self, txt):
        "テキストボックスの文字列を消去する"
        txt.delete("1.0", "end")

    def init_ent(self, ent):
        "エントリーボックスの文字列を消去する"
        ent.delete("0", "end")


if __name__ == "__main__":
    f = Application()
    f.pack()
    f.mainloop()
