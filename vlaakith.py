import os

import customtkinter
import pandas as pd
from CTkMessagebox import CTkMessagebox
from customtkinter import filedialog
from progressbar import progressbar


class Vlaakith:
    def __init__(self) -> None:
        # theming
        customtkinter.set_appearance_mode('System')
        customtkinter.set_default_color_theme('dark-blue')

        # build window
        self.app = customtkinter.CTk()
        self.app.title('Vlaakith | BIP Export Concatenator')
        self.selected_payload_directory = ''
        self.selected_output_directory = ''
        self.skipped_file_counter = 0
        self.skipped_file_names = []

        # get payload button
        self.btn_get_payload_dir = customtkinter.CTkButton(
            master=self.app,
            text='Select Payload Directory',
            command=self.get_payload_dir,
            height=30,
            width=160
        )

        self.btn_get_payload_dir.place(
            x=20,
            y=20
        )

        # selected payload label
        self.label_selected_payload_dir = customtkinter.CTkLabel(
            master=self.app,
            text='Select a payload directory...',
            height=30
        )

        self.label_selected_payload_dir.place(
            x=200,
            y=20,
        )

        # get output button
        self.btn_get_output_dir = customtkinter.CTkButton(
            master=self.app,
            text='Select Output Directory',
            command=self.get_output_dir,
            height=30,
            width=160
        )

        self.btn_get_output_dir.place(
            x=20,
            y=55
        )

        # selected output label
        self.label_selected_output_dir = customtkinter.CTkLabel(
            master=self.app,
            text='Select an output directory...',
            height=30
        )

        self.label_selected_output_dir.place(
            x=200,
            y=55,
        )

        # start process button
        self.btn_start = customtkinter.CTkButton(
            master=self.app,
            text='Process Files',
            command=self.build_file,
            height=30,
            width=160
        )

        self.btn_start.place(
            x=20,
            y=105
        )

        # label for skipped files counter
        self.label_skipped_file_counter = customtkinter.CTkLabel(
            master=self.app,
            text=f'Skipped files: {self.skipped_file_counter}',
            height=30
        )

        self.label_skipped_file_counter.place(
            x=20,
            y=145,
        )

        # textox for skipped file names
        self.textbox_file_names = customtkinter.CTkTextbox(
            master=self.app,
            width=700,
            height=100
        )

        self.textbox_file_names.place(
            x=20,
            y=170,
        )

        # calculate to launch on center of screen
        app_width = 800
        app_height = 300
        x = (self.app.winfo_screenwidth()/2) - (app_width/2)
        y = (self.app.winfo_screenheight()/2) - (app_height/2)
        self.app.geometry('%dx%d+%d+%d' % (app_width, app_height, x, y))
        self.app.resizable(False, False)
        self.app.mainloop()

    # set the payload dir
    def get_payload_dir(self) -> None:
        payload_dir = filedialog.askdirectory()

        if payload_dir:
            self.selected_payload_directory = payload_dir
            self.label_selected_payload_dir.configure(text=payload_dir)

    # set the output dir
    def get_output_dir(self) -> None:
        output_dir = filedialog.askdirectory()

        if output_dir:
            self.selected_output_directory = output_dir
            self.label_selected_output_dir.configure(text=output_dir)

    # start process
    def build_file(self) -> None:
        # init
        payload_directory = self.selected_payload_directory
        output_directory = self.selected_output_directory
        frames = []

        if not payload_directory or not output_directory:
            CTkMessagebox(
                master=self.app,
                title='Missing Directories',
                icon='cancel',
                message='Please select the required directories!'
            )

        else:
            try:
                # loop through each csv file in dir
                # using progress bar here to update in console
                for file in progressbar(os.listdir(payload_directory)):
                    if file.endswith('.csv'):
                        try:
                            df = pd.read_csv(
                                f'{payload_directory}/{file}',
                                encoding='ISO-8859-1'
                            )

                            # add only valid new df to a list
                            # csv file should contain 'ShortId' column
                            if 'ShortId' in df.columns:
                                df = df.set_index(['ShortId'])
                                frames.append(df)

                            else:
                                # count files were skipped because of missing index column
                                self.skipped_file_names.append(file)
                                self.skipped_file_counter += 1

                                # update label for skipped file counter
                                self.label_skipped_file_counter.configure(
                                    text=f'Skipped files: {
                                        self.skipped_file_counter}'
                                )

                        except Exception as e:
                            CTkMessagebox(
                                master=self.app,
                                title="Error",
                                icon='cancel',
                                message=e
                            )

                # reset skipped files counter and names
                self.skipped_file_counter = 0

                # clear textbox
                self.textbox_file_names.delete('0.0', 'end')

                # update textbox for skipped file names
                for index, file_name in enumerate(self.skipped_file_names):
                    self.textbox_file_names.insert(
                        f'{index}.0',
                        f'{file_name}\n'
                    )

                self.skipped_file_names.clear()

                # concat all dataframes from the list to 1 singular dataframe and output the csv
                df_merged = pd.concat(frames)
                df_merged.to_csv(f'{output_directory}/concatenated.csv')

                CTkMessagebox(
                    master=self.app,
                    title='Success',
                    icon='check',
                    message='Processing completed'
                )

            except Exception as e:
                # display error in case parsing fails
                CTkMessagebox(
                    master=self.app,
                    title='Error',
                    icon='cancel',
                    message=e
                )


def main():
    Vlaakith()


if __name__ == '__main__':
    main()
