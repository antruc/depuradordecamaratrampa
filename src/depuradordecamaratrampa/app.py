import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

from ultralytics import YOLO

from pathlib import Path
import shutil
import threading
import time


class DepuradordeCamaraTrampa(toga.App):
    def startup(self):
        # Create Toga components
        main_box = toga.Box(style=Pack(direction=COLUMN))
        input_box = toga.Box(style=Pack(direction=ROW, padding=10))
        output_box = toga.Box(
            style=Pack(direction=ROW, padding_right=10, padding_left=10)
        )
        progress_box = toga.Box(
            style=Pack(direction=ROW, padding_right=10, padding_left=10, padding_top=15)
        )
        run_box = toga.Box(style=Pack(direction=ROW, padding=10))

        self.input_label = toga.Label(
            "Seleccione carpeta de origen", style=Pack(padding_top=3, padding_left=10)
        )
        self.output_label = toga.Label(
            "Seleccione carpeta de destino", style=Pack(padding_top=3, padding_left=10)
        )

        self.input_button = toga.Button("Entrada", on_press=self.select_input_folder)
        self.output_button = toga.Button("Salida", on_press=self.select_output_folder)
        self.run_button = toga.Button(
            "Procesar", on_press=self.run_app, style=Pack(flex=2)
        )
        cancel_button = toga.Button(
            "Cancelar", on_press=self.cancel_run, style=Pack(flex=2)
        )

        # Initialize variables
        # self.buttons = [self.input_button, self.output_button, self.run_button]
        self.run_finished = False

        # Add components into boxes
        input_box.add(self.input_button)
        input_box.add(self.input_label)

        output_box.add(self.output_button)
        output_box.add(self.output_label)

        self.progress = toga.ProgressBar(max=None, style=Pack(flex=1))
        progress_box.add(self.progress)

        run_box.add(self.run_button)
        run_box.add(cancel_button)

        main_box.add(input_box)
        main_box.add(output_box)
        main_box.add(progress_box)
        main_box.add(run_box)

        # Create and show main window
        self.main_window = toga.Window(size=toga.Size(345, 135), resizable=True)
        self.main_window.content = main_box
        self.main_window.show()

    def run_app(self, widget):
        threading.Thread(target=self.run_model).start()

    def run_model(self):
        self.running = True

        # Load model
        model_path = Path(__file__).parent / "yolo11n-dynamic.onnx"
        model = YOLO(model_path, task="detect")

        # Run prediction
        try:
            results = model.predict(
                self.input_path,
                classes=[0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                stream=True,
                verbose=False,
            )
            last_file = ""

            # self.disable_buttons()
            self.start_progress_bar()

            # Iterate over results and copy images with detections
            for i, result in enumerate(results):
                # Check if any detections were made
                if len(result.boxes) > 0:
                    # In case of videos just copy it once
                    if last_file != result.path:
                        if self.output_path != "":
                            shutil.copy2(result.path, self.output_path)
                            last_file = result.path
                        else:
                            raise AttributeError
                if self.running == False:
                    raise AttributeError

            # self.enable_buttons()
            self.run_finished = True
            self.stop_progress_bar()
            time.sleep(1)
            self.run_finished = False
        except AttributeError:
            if self.input_label.text == "Seleccione carpeta de origen":
                self.input_label.text = "Error: Debe seleccionar una carpeta"

            if self.output_label.text == "Seleccione carpeta de destino":
                self.output_label.text = "Error: Debe seleccionar una carpeta"

            # self.enable_buttons()
            self.stop_progress_bar()

        except FileNotFoundError:
            self.input_label.text = "Error: No se encontraron archivos soportados"
            # self.enable_buttons()
            self.stop_progress_bar()

        except Exception:
            self.input_label.text = "Error: Hay un problema con sus archivos"
            # self.enable_buttons()
            self.stop_progress_bar()

    def cancel_run(self, widget):
        self.running = False

    async def select_input_folder(self, widget):
        try:
            path_name = await self.dialog(toga.SelectFolderDialog("Carpeta de origen"))
            if path_name is not None:
                self.input_path = path_name
                self.input_label.text = path_name
        except ValueError:
            self.input_label.text = "Carpeta sin seleccionar"

    async def select_output_folder(self, widget):
        try:
            path_name = await self.dialog(toga.SelectFolderDialog("Carpeta de destino"))
            if path_name is not None:
                self.output_path = path_name
                self.output_label.text = path_name
        except ValueError:
            self.output_label.text = "Carpeta sin seleccionar"

    """ 
    Doesn't work on Windows
    def enable_buttons(self):
        for button in self.buttons:
        button.enabled = True

    def disable_buttons(self):
        for button in self.buttons:
        button.enabled = False
    """

    def start_progress_bar(self):
        self.loop.call_soon_threadsafe(self.progress_bar_start)

    def progress_bar_start(self):
        self.progress.max = None
        self.progress.start()

    def stop_progress_bar(self):
        self.loop.call_soon_threadsafe(self.progress_bar_stop)

    def progress_bar_stop(self):
        if self.run_finished == True:
            self.progress.max = 100
            self.progress.value = 100
            self.progress.stop()
        else:
            self.progress.stop()


def main():
    return DepuradordeCamaraTrampa()
