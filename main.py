import os
import tkinter as tk
from tkinter import filedialog

import pandas as pd


class Vlaakith:
    def __init__(self) -> None:
        # build main window
        self.main_window = tk.Tk()
        self.main_window.geometry('800x200')
        self.main_window.resizable(False, False)
        self.main_window.title('Vlaakith | BIP Export Concatenator')
        self.selected_payload_directory = 'Please select a payload directory...'
        self.selected_output_directory = 'Please select an output directory...'

        # payload button
        self.btn_get_payload_dir = tk.Button(
            self.main_window,
            text='Payload Directory',
            command=self.get_payload_dir
        )

        self.btn_get_payload_dir.place(
            x=20,
            y=20,
            height=30,
            width=160
        )

        # payload label
        self.label_selected_payload_dir = tk.Label(
            self.main_window,
            text=self.selected_payload_directory
        )

        self.label_selected_payload_dir.place(
            x=200,
            y=20,
            height=30
        )

        # output btn
        self.btn_get_output_dir = tk.Button(
            self.main_window,
            text='Output Directory',
            command=self.get_output_dir
        )

        self.btn_get_output_dir.place(
            x=20,
            y=55,
            height=30,
            width=160
        )

        # output label
        self.label_selected_output_dir = tk.Label(
            self.main_window,
            text=self.selected_output_directory
        )

        self.label_selected_output_dir.place(
            x=200,
            y=55,
            height=30
        )

        # start process btn
        self.btn_start = tk.Button(
            self.main_window,
            text='Process Files',
            command=self.build_file
        )

        self.btn_start.place(
            x=20,
            y=105,
            height=30,
            width=160
        )

        # launch window
        self.main_window.mainloop()

    # set the payload dir
    def get_payload_dir(self) -> None:
        payload_dir = filedialog.askdirectory()

        if payload_dir:
            self.selected_payload_directory = payload_dir
            self.label_selected_payload_dir['text'] = payload_dir

    # set the output dir

    def get_output_dir(self) -> None:
        output_dir = filedialog.askdirectory()

        if output_dir:
            self.selected_output_directory = output_dir
            self.label_selected_output_dir['text'] = output_dir

    # start process

    def build_file(self) -> None:
        # init
        payload_directory = self.selected_payload_directory
        output_directory = self.selected_output_directory
        frames = []

        # loop through each csv file in dir
        for file in os.listdir(payload_directory):
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(
                        f'{payload_directory}/{file}',
                        encoding='ISO-8859-1',
                        index_col='ShortId'
                    )

                    # add each new df to a list
                    frames.append(df)

                except Exception as e:
                    print(e)

        # concat all dataframes from the list to 1 singular dataframe and output the csv
        df_merged = pd.concat(frames)
        df_merged.to_csv(f'{output_directory}/concatenated.csv')


def main():
    Vlaakith()


if __name__ == '__main__':
    main()
