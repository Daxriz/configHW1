import os
import sys
import json
import zipfile
import tkinter as tk
from tkinter import scrolledtext

class ShellEmulator:
    def __init__(self, computer_name, vfs_path, log_file_path):
        self.computer_name = computer_name
        self.vfs_path = vfs_path
        self.log_file_path = log_file_path
        self.vfs_root = "virtual_root"
        self.current_dir = self.vfs_root
        self.commands = {"ls": self.ls, "cd": self.cd, "pwd": self.pwd, "clear": self.clear,
                         "rmdir": self.rmdir, "exit": self.exit}
        self.log_data = []
        self.init_vfs()

    def init_vfs(self):
        if not os.path.exists(self.vfs_root):
            os.makedirs(self.vfs_root)
        with zipfile.ZipFile(self.vfs_path, 'r') as zip_ref:
            zip_ref.extractall(self.vfs_root)

    def log_action(self, action, result):
        self.log_data.append({"action": action, "result": result})
        with open(self.log_file_path, 'w') as f:
            json.dump(self.log_data, f, indent=4)

    def ls(self, *args):
        try:
            result = "\n".join(os.listdir(self.current_dir))
        except Exception as e:
            result = str(e)
        self.log_action("ls", result)
        return result

    def cd(self, path):
        try:
            new_path = os.path.normpath(os.path.join(self.current_dir, path))
            if os.path.isdir(new_path):
                self.current_dir = new_path
                result = f"Changed directory to {self.current_dir}"
            else:
                result = f"{path} is not a directory"
        except Exception as e:
            result = str(e)
        self.log_action(f"cd {path}", result)
        return result

    def pwd(self, *args):
        result = os.path.relpath(self.current_dir, self.vfs_root)
        self.log_action("pwd", result)
        return result

    def clear(self, *args):
        return "clear_screen"

    def rmdir(self, dir_name):
        try:
            path = os.path.join(self.current_dir, dir_name)
            if os.path.isdir(path):
                os.rmdir(path)
                result = f"Removed directory {dir_name}"
            else:
                result = f"{dir_name} is not a directory"
        except Exception as e:
            result = str(e)
        self.log_action(f"rmdir {dir_name}", result)
        return result

    def exit(self, *args):
        self.log_action("exit", "Shell exited")
        return "exit_program"

    def execute_command(self, command_line):
        parts = command_line.strip().split()
        if not parts:
            return ""
        cmd, *args = parts
        if cmd in self.commands:
            return self.commands[cmd](*args)
        else:
            return f"Command '{cmd}' not recognized"

class ShellGUI:
    def __init__(self, emulator):
        self.emulator = emulator
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.output_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', height=20, width=80)
        self.output_text.pack()
        self.input_entry = tk.Entry(self.root, width=80)
        self.input_entry.pack()
        self.input_entry.bind("<Return>", self.process_command)
        self.display_output(f"Welcome to {self.emulator.computer_name} shell!\n")

    def display_output(self, message):
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')

    def process_command(self, event):
        command_line = self.input_entry.get()
        self.display_output(f"> {command_line}")
        result = self.emulator.execute_command(command_line)
        if result == "clear_screen":
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, tk.END)
            self.output_text.config(state='disabled')
        elif result == "exit_program":
            self.root.destroy()
        else:
            self.display_output(result)
        self.input_entry.delete(0, tk.END)

    def run(self):
            self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python shell_emulator.py <computer_name> <vfs_path> <log_file_path>")
        sys.exit(1)

    computer_name = sys.argv[1]
    vfs_path = sys.argv[2]
    log_file_path = sys.argv[3]

    shell_emulator = ShellEmulator(computer_name, vfs_path, log_file_path)
    gui = ShellGUI(shell_emulator)
    gui.run()