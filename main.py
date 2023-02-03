import tkinter
import sys
import os
import distutils
import configparser
import customtkinter as ct
import subprocess
import shlex
import threading
from collections import defaultdict

ct.set_appearance_mode("dark")


# class Redirect:
#     def __init__(self, widget, autoscroll=True):
#         self.widget = widget
#         self.autoscroll = autoscroll

#     def write(self, textbox):
#         self.widget.insert("end", textbox)
#         if self.autoscroll:
#             self.widget.see("end")  # autoscroll

#     def flush(self):
#         pass


class App(ct.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        configs = self.read_config()
        print(configs)

        self.geometry("680x600")
        self.title("Screenshot Bot")
        self.grid_columnconfigure((0, 3), minsize=20)
        self.grid_columnconfigure((1, 2), minsize=160)

        self.columnconfigure(3)

        # ip_label = ct.CTkLabel(self, text="OBS Machine IP", anchor="nw")
        # ip_label.grid(
        #     row=0,
        #     column=1,
        #     pady=(20, 0),
        # )
        # self.ip_entry = ct.CTkEntry(self, placeholder_text="XXX.XXX.XXX.XXX", width=160)
        # self.ip_entry.grid(row=1, column=1, columnspan=1, sticky="nsew")

        # port_label = ct.CTkLabel(self, text="OBS Machine Port", anchor="nw")
        # port_label.grid(
        #     row=0,
        #     column=2,
        #     pady=(10, 0),
        # )
        # self.port_entry = ct.CTkEntry(self, placeholder_text="XXX", width=160)
        # self.port_entry.grid(row=1, column=2, columnspan=1, padx=(20, 0), sticky="nsew")

        source_label = ct.CTkLabel(self, text="OBS Source Name", anchor="nw")
        source_label.grid(
            row=1,
            column=1,
            pady=(10, 0),
        )
        self.source_entry = ct.CTkEntry(
            self,
            placeholder_text="Source name",
            width=160,
        )
        self.source_entry.insert(0, configs.get("source", ""))
        self.source_entry.grid(row=2, column=1, columnspan=1, sticky="nsew")

        password_label = ct.CTkLabel(self, text="OBS Password", anchor="nw")
        password_label.grid(
            row=1,
            column=2,
            pady=(10, 0),
        )
        self.password_entry = ct.CTkEntry(
            self, placeholder_text="Password", width=160, show="*"
        )
        self.password_entry.insert(0, configs.get("password", ""))
        self.password_entry.grid(
            row=2, column=2, columnspan=1, padx=(20, 0), sticky="nsew"
        )

        webhook_label = ct.CTkLabel(self, text="Discord Webhook URL", anchor="nw")
        webhook_label.grid(
            row=7,
            column=1,
            columnspan=2,
            pady=(30, 0),
        )
        self.webhook_entry = ct.CTkEntry(
            self,
            placeholder_text="https://....",
            width=200,
        )
        self.webhook_entry.insert(0, configs.get("webhook", ""))
        self.webhook_entry.grid(row=8, column=1, columnspan=2, sticky="nsew")

        channel_label = ct.CTkLabel(self, text="Twitch Channel name", anchor="nw")
        channel_label.grid(
            row=9,
            column=1,
            pady=(30, 0),
        )
        self.channel_entry = ct.CTkEntry(self, placeholder_text="XXXX", width=200)
        self.channel_entry.insert(0, configs.get("channel", ""))
        self.channel_entry.grid(row=10, column=1, columnspan=1, sticky="nsew")

        token_label = ct.CTkLabel(self, text="Twitch Bot Token", anchor="nw")
        token_label.grid(
            row=9,
            column=2,
            pady=(30, 0),
        )
        self.token_entry = ct.CTkEntry(
            self, placeholder_text="XXXX", width=200, show="*"
        )
        self.token_entry.insert(0, configs.get("token", ""))
        self.token_entry.grid(
            row=10, column=2, padx=(20, 0), columnspan=1, sticky="nsew"
        )

        self.start_button = ct.CTkButton(
            self, text="Start", command=self.start_button_action
        )
        self.start_button.grid(row=11, column=1, columnspan=2, pady=(40, 0))
        self.stop_button = ct.CTkButton(
            self, text="Stop", command=self.stop_button_action, fg_color="red"
        )
        self.stop_button.grid(row=12, column=1, columnspan=2, pady=(0, 20))

        self.info_label = ct.CTkLabel(self, text="")
        self.info_label.grid(row=13, column=1, pady=(0, 0))

        console = ct.CTkLabel(self, text="Twitch Bot Logs", anchor="nw")
        console.grid(row=12, column=0, pady=(50, 0), padx=(30, 0))
        self.text_box = ct.CTkTextbox(self, state="disabled", width=600)
        self.text_box.grid(row=14, column=0, padx=(30, 0), columnspan=6)

    def stop_button_action(self):
        if self.bot:
            self.bot.kill()
            self.insert_to_console("Bot stopped")
        self.start_button.configure(text="Start", state="normal")

    def start_button_action(self):
        threading.Thread(target=self.start_bot).start()

    def read_config(self):
        config = configparser.ConfigParser()
        config.read("bot.ini")
        print(config)
        if "DEFAULT" in config:
            return config["DEFAULT"]
        return defaultdict(str)

    def save_config(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = self.get_entries()
        with open("bot.ini", "w") as configfile:
            config.write(configfile)

    def get_entries(self):
        password = self.password_entry.get() or None
        source = self.source_entry.get() or None
        webhook = self.webhook_entry.get() or None
        channel = self.channel_entry.get() or None
        token = self.token_entry.get() or None
        return {
            "password": password,
            "source": source,
            "webhook": webhook,
            "channel": channel,
            "token": token,
        }

    def insert_to_console(self, line, autoscroll=True):
        self.text_box.configure(state="normal")
        self.text_box.insert(ct.END, line + "\n")
        self.text_box.configure(state="disabled")
        if autoscroll:
            self.text_box.see(ct.END)

    def start_bot(self):
        entries = self.get_entries()
        self.save_config()
        vals = list(entries.values())
        if not all(vals):
            self.info_label.configure(text="A field is missing!", text_color="red")
            return
        args = shlex.join(["bot.exe", *vals])
        self.insert_to_console("Starting Bot...")
        self.bot = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            bufsize=1,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        print("BOT RUNNING")
        self.start_button.configure(text="Bot Running", state="disabled")
        for line in self.bot.stdout:
            if type(line) == bytes:
                line = line.decode("utf-8")
            if line:
                self.insert_to_console(line)
        # while bot.poll() is None:
        #     text = bot.stdout.read(1)
        #     if type(text) == bytes:
        #         msg = msg.decode("utf-8")
        #     print(text or "No text")
        #     if text:
        #         self.text_box.insert(ct.END, text + "\n")
        self.start_button.configure(text="Start", state="normal")
        print("===While ended===")


App().mainloop()
