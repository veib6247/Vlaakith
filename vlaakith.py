import os

import customtkinter
import pandas as pd
from CTkMessagebox import CTkMessagebox
from customtkinter import filedialog


class Vlaakith:
    def __init__(self) -> None:
        # theming
        customtkinter.set_appearance_mode('System')
        customtkinter.set_default_color_theme('dark-blue')

        # build window
        self.app = customtkinter.CTk()
        self.app.title('Vlaakith | BIP Export Concatenator')
        self.selected_payload_directory = 'Select a payload directory...'
        self.selected_output_directory = 'Select an output directory...'
        self.skipped_file_counter = 0

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
            text=self.selected_payload_directory,
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
            text=self.selected_output_directory,
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

        # label for skipped files
        self.label_skipped_file_counter = customtkinter.CTkLabel(
            master=self.app,
            text=f'Skipped files: {self.skipped_file_counter}',
            height=30
        )

        self.label_skipped_file_counter.place(
            x=20,
            y=145,
        )

        # calculate to launch on center of screen
        app_width = 800
        app_height = 200
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

        try:
            # loop through each csv file in dir
            for file in os.listdir(payload_directory):
                if file.endswith('.csv'):
                    try:

                        df = pd.read_csv(
                            f'{payload_directory}/{file}',
                            encoding='ISO-8859-1'
                        )

                        if 'ShortId' in df.columns:
                            df = df.set_index(['ShortId'])
                            # add each new df to a list
                            frames.append(df)

                        else:
                            self.skipped_file_counter += 1
                            self.label_skipped_file_counter.configure(
                                text=f'Skipped files: {
                                    self.skipped_file_counter}'
                            )

                    except Exception as e:
                        CTkMessagebox(
                            title="Error",
                            icon='cancel',
                            message=e
                        )

            # reset skipped files counter
            self.skipped_file_counter = 0

            # concat all dataframes from the list to 1 singular dataframe and output the csv
            df_merged = pd.concat(frames)
            df_merged.to_csv(f'{output_directory}/concatenated.csv')
            CTkMessagebox(
                title='Success',
                icon='check',
                message='Processing completed'
            )

        except Exception as e:
            CTkMessagebox(
                title='Error',
                icon='cancel',
                message=e
            )


def main():
    Vlaakith()


if __name__ == '__main__':
    main()
