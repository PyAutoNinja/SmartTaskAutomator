from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import os
import shutil


class FileOrganizerApp(App):

    def build(self):

        main_layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        # Input Box
        self.path_input = TextInput(
            hint_text="Enter full folder path",
            size_hint=(1, 0.12),
            multiline=False
        )

        main_layout.add_widget(self.path_input)

        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.12), spacing=10)

        preview_btn = Button(text="Preview")
        organize_btn = Button(text="Organize")

        preview_btn.bind(on_press=self.preview_files)
        organize_btn.bind(on_press=self.organize_files)

        btn_layout.add_widget(preview_btn)
        btn_layout.add_widget(organize_btn)

        main_layout.add_widget(btn_layout)

        # Output Area (Scrollable)
        self.output = Label(
            text="Output will appear here...",
            size_hint_y=None,
            valign="top"
        )

        self.output.bind(
            width=lambda *x: self.output.setter("text_size")(self.output, (self.output.width, None))
        )

        self.output.bind(
            texture_size=lambda *x: self.output.setter("height")(self.output, self.output.texture_size[1])
        )

        scroll = ScrollView()
        scroll.add_widget(self.output)

        main_layout.add_widget(scroll)

        return main_layout


    def preview_files(self, instance):

        folder = self.path_input.text.strip()

        if not os.path.exists(folder):
            self.output.text = "Error: Invalid folder path!"
            return

        files = os.listdir(folder)

        text = "Preview Mode\n"
        text += "-" * 25 + "\n\n"

        count = 0

        for f in files:

            full_path = os.path.join(folder, f)

            if os.path.isfile(full_path):
                text += f + "\n"
                count += 1

        text += f"\nTotal files found: {count}"

        self.output.text = text


    def organize_files(self, instance):

        folder = self.path_input.text.strip()

        if not os.path.exists(folder):
            self.output.text = "Error: Invalid folder path!"
            return

        files = os.listdir(folder)

        log = "Organizing Files\n"
        log += "-" * 25 + "\n\n"

        moved = 0

        for f in files:

            src = os.path.join(folder, f)

            # Skip folders
            if not os.path.isfile(src):
                continue

            ext = f.split(".")[-1].lower()

            # Skip files without extension
            if ext == f.lower():
                continue

            dest_folder = os.path.join(folder, ext)

            # Create folder if not exists
            if not os.path.exists(dest_folder):
                os.mkdir(dest_folder)

            dest = os.path.join(dest_folder, f)

            # Avoid overwrite
            if os.path.exists(dest):
                log += f"Skipped (Already exists): {f}\n"
                continue

            shutil.move(src, dest)

            log += f"Moved: {f}  ->  {ext}/\n"

            moved += 1


        log += f"\nTotal files moved: {moved}"

        self.output.text = log


FileOrganizerApp().run()