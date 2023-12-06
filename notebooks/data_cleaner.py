import pandas as pd
import pytz
import ast


class DataCleaner:

    def __init__(self, df):
        self.df = df

    def drop_column(self, column_name):
        self.df.drop(columns=[column_name], inplace=True)

    def reset_index(self):
        self.df.reset_index(drop=True, inplace=True)

    def convert_utc_to_local(self, utc_datetime):
        try:
            utc_time = pytz.utc.localize(utc_datetime)
            local_time = utc_time.astimezone(pytz.timezone('Asia/Singapore'))
            return local_time
        except Exception as e:
            return None

    def clean_up_datetime(self, column_name):
        self.df[column_name] = pd.to_datetime(self.df[column_name])
        self.df[f'{column_name}_sgt'] = self.df[column_name].apply(lambda x: self.convert_utc_to_local(x))

    def remove_null_reviews(self, column_name):
        self.df = self.df.loc[~self.df[column_name].isnull()].reset_index(drop=True)

    
    def add_day_hour(self, datetime_column_name):
        self.df['day_of_week'] = self.df[datetime_column_name].apply(lambda date: date.strftime("%A"))
        self.df['hour'] = self.df[datetime_column_name].apply(lambda date: date.strftime("%H"))
        
    
    def process_review_questions(self, column_name):
        data = self.df[column_name].dropna().apply(ast.literal_eval)
        review_questions_df = pd.DataFrame(data.to_list())
        return review_questions_df

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