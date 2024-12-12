from pandas import DataFrame, to_datetime, read_csv
import globals as g
import io

class FileDataProcessor:
    @staticmethod
    def process(contents: bytes):
        '''
        Pre process the uplaoded file
        '''
        g.df = read_csv(io.StringIO(contents.decode("utf-8")))
        
        if g.df is None:
            raise ValueError("g.df is none ?")
        
        g.df.columns = g.df.columns.str.lower().str.replace(' ', '_')
        g.df.duplicated().sum()
        g.df['date'] = to_datetime(g.df['date'])
        g.df['gender'] = g.df['gender'].astype('category')
        g.df['product_category'] = g.df['product_category'].astype('category')
        g.df.drop('customer_id', axis=1, inplace=True)

        g.temp_df = g.df.copy()
        g.temp_df['date'] = to_datetime(g.temp_df['date']) # Convert to datetime
        g.temp_df.set_index('date', inplace=True) # Set 'transaction_date' as index

        # Feature engineering: Extract additional features from the date column
        g.df['month'] = g.df['date'].dt.month
        g.df['year'] = g.df['date'].dt.year
        g.df['day_of_week'] = g.df['date'].dt.dayofweek
        g.df['day_of_month'] = g.df['date'].dt.day

        g.df['gender'] = g.df['gender'].cat.codes
        g.df['product_category'] = g.df['product_category'].cat.codes

        return {"columns": list(g.df.columns), "preview": g.df.head(5).to_dict(orient="records")}

    def describe():

        describe_html = g.df.describe().to_html(border=1, classes='dataframe')

        return describe_html

    