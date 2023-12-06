import pandas as pd
import pytz
import ast


class DataCleaner:

    def __init__(self, df):
        self.df = df
    
    # drop unwanted columns
    def drop_column(self, column_name):
        self.df.drop(columns=[column_name], inplace=True)

    def reset_index(self):
        self.df.reset_index(drop=True, inplace=True)

    def remove_null_reviews(self, column_name):
        self.df = self.df.loc[~self.df[column_name].isnull()].reset_index(drop=True)


    def drop_duplicates(self, subset=None):
        """
        Drop duplicate rows from the DataFrame.

        Parameters:
        - subset (list, optional): Columns to consider when identifying duplicates. Default is None.

        Returns:
        - None: Modifies the DataFrame in place.
        """
        self.df.drop_duplicates(subset=subset, keep='first', inplace=True)
        self.df.reset_index(drop=True, inplace=True)
    
    # to express each rating in values between 0 to 10
    def get_ratings(self, column_name):
        self.df[column_name] = self.df[column_name]/10
    
    # to have the text data in each row of the column to be in lower case
    def lower(self, column_name):
        self.df[column_name] = self.df[column_name].apply(lambda text: text.lower())