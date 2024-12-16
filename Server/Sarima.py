from statsmodels.tsa.stattools import adfuller
import globals as g
import pandas as pd
from typing import Any
import pmdarima as pm
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

monthly_avg: pd.Series | Any = None
quantity_monthly: pd.Series | Any = None
SARIMA_model: Any = None
SARIMA_model_2: Any = None
plt.switch_backend('agg')

class SarimaProccessor:
    @staticmethod
    def data(param: str):
        global  monthly_avg, quantity_monthly

        html_table = None

        if param == 'MonthlyAvarage':
            # Augmented Dickey–Fuller test:
            print('Results of Dickey Fuller Test:')

            # Resample the 'total_amount' series by month and drop any missing values
            monthly_avg = g.temp_df['total_amount'].resample('MS').mean().dropna()

            # Perform the Augmented Dickey-Fuller test
            dftest = adfuller(monthly_avg, autolag='AIC')

            # Prepare the output
            dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
            for key, value in dftest[4].items():
                dfoutput['Critical Value (%s)' % key] = value

            # Convert results to an HTML table
            html_table = dfoutput.to_frame("Value").to_html(border=1, classes='dataframe')

            return html_table
        elif param == 'QuantityDemand':
            quantity_monthly = g.temp_df['quantity'].resample('M').sum().dropna()
            quantity_monthly = quantity_monthly.iloc[:-1].dropna()[:12]

            # Perform the Augmented Dickey-Fuller test
            dftest = adfuller(quantity_monthly, autolag='AIC')

            # Prepare the output
            dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
            for key, value in dftest[4].items():
                dfoutput['Critical Value (%s)' % key] = value
            
            html_table = dfoutput.to_frame("Value").to_html(border=1, classes='dataframe')

        return html_table
    
    @staticmethod
    def train(param: str):
        global SARIMA_model, SARIMA_model_2, monthly_avg, quantity_monthly
        if param == 'MonthlyAvarage':
            # Standard ARIMA Model
            monthly_avg = g.temp_df['total_amount'].resample('MS').mean().dropna()

            if SARIMA_model == None:
                SARIMA_model = pm.auto_arima(monthly_avg,exogenous=monthly_avg.index.month, start_p=1, start_q=1,
                            max_p=6, max_q=6, max_P=6, max_Q=6, max_order=15, m=6, max_iter=100,
                            start_P=1, seasonal=True, d=None, D=1, trace=True,
                            error_action='ignore', suppress_warnings=False, stepwise=True)
            
            summary_text = SARIMA_model.summary().as_text()
            return summary_text
            
        elif param == 'QuantityDemand':
            quantity_monthly = g.temp_df['quantity'].resample('M').sum().dropna()
            quantity_monthly = quantity_monthly.iloc[:-1].dropna()[:12]
            quantity_monthly.index = pd.to_datetime(quantity_monthly.index)

            if SARIMA_model_2 == None:
                SARIMA_model_2 = pm.auto_arima(quantity_monthly,exogenous=quantity_monthly.index.month, start_p=1, start_q=1,
                            max_p=6, max_q=6, max_P=6, max_Q=6, max_order=15, m=8,maxiter=100,
                            start_P=1, seasonal=True, d=None, D=1, trace=True,
                            error_action='ignore', suppress_warnings=True, stepwise=True)
                
            summary_text = SARIMA_model_2.summary().as_text()
            return summary_text
        
    @staticmethod
    def plot(param: str):
        global SARIMA_model, SARIMA_model_2, monthly_avg, quantity_monthly
        if param == 'MonthlyAvarage':
            # Standard ARIMA Model
            fig = SARIMA_model.plot_diagnostics(figsize=(18,12), lags=6)
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            return img_base64
            
        elif param == 'QuantityDemand':
            fig = SARIMA_model_2.plot_diagnostics(figsize=(18,12), lags=3)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            return img_base64
    
    @staticmethod
    def __forecast_accuracy(forecast, actual):
        forecast = forecast.to_numpy()
        actual = actual.to_numpy()

        mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
        me = np.mean(forecast - actual)             # ME
        mae = np.mean(np.abs(forecast - actual))    # MAE
        mpe = np.mean((forecast - actual)/actual)   # MPE
        rmse = np.mean((forecast - actual)**2)**.5  # RMSE
        corr = np.corrcoef(forecast, actual)[0,1]   # corr
        mins = np.amin(np.hstack([forecast[:,None],
                                actual[:,None]]), axis=1)
        maxs = np.amax(np.hstack([forecast[:,None],
                                actual[:,None]]), axis=1)
        minmax = 1 - np.mean(mins/maxs)             # minmax

        return({'Mean Absolute Percentage Error (MAPE)':mape, 'Mean Error                     (ME)':me, 'Mean Absolute Error            (MAE)': mae,
                'Mean Percentage Error          (MPE)': mpe, 'Root Mean Squared Error        (RMSE)':rmse,
                'Correlation Error              (CORR)':corr, 'Min-Max Error                  (MINMAX)':minmax, })

    @staticmethod
    def forecast(param: str):
        global SARIMA_model, SARIMA_model_2, monthly_avg, quantity_monthly
        if param == 'MonthlyAvarage':
        # Ensure the index is of datetime type for both original and forecasted series
            g.df.index = pd.to_datetime(g.df.index)

            # Forecast
            n_periods =12
            fitted, confint = SARIMA_model.predict_in_sample(return_conf_int=True, start=6, end=18, exogenous=monthly_avg.index.month, dynamic=True)


            # Make series for plotting purpose
            fitted_series = pd.Series(fitted)
            lower_series = pd.Series(confint[:, 0])
            upper_series = pd.Series(confint[:, 1])

            fitted_series.index = pd.to_datetime(fitted_series.index)
            fitted_series.index = pd.to_datetime(fitted_series.index) - pd.DateOffset(months=6)

            forecast_start = monthly_avg.index
            lower_series = pd.Series(confint[:, 0], index=forecast_start)
            upper_series = pd.Series(confint[:, 1], index=forecast_start)
            #fitted_series.index = fitted_series.index + pd.offsets.MonthEnd(0)  # Shift to end of the month

            plt.figure(figsize=(15,7))

            print(monthly_avg)
            print(fitted_series)

            # Plot actual data and forecasted data
            plt.plot(monthly_avg, color='#1f76b4', label="Actual")
            plt.plot(fitted_series.index, fitted_series, color='darkgreen', label="Forecasted")
            plt.fill_between(lower_series.index,
                            lower_series,
                            upper_series,
                            color='k', alpha=.05)

            # Set title and labels
            plt.title("SARIMA - Forecast Avg Monthly Sales")
            plt.legend(loc='upper left')

            # Set date format on x-axis to "Year-Month"
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

            # Rotate x-axis labels for better visibility
            plt.xticks(rotation=45)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            return img_base64, SarimaProccessor.__forecast_accuracy(fitted, monthly_avg)
            
        elif param == 'QuantityDemand':
            # Ensure the index is of datetime type for both original and forecasted series
            g.df.index = pd.to_datetime(g.df.index)

            # Forecast
            n_periods = 12
            fitted, confint = SARIMA_model_2.predict_in_sample(return_conf_int=True, start=8, end=19,
                                            exogenous=quantity_monthly.index.month, dynamic=True)

            # Make series for plotting purpose
            fitted_series = pd.Series(fitted)
            lower_series = pd.Series(confint[:, 0])
            upper_series = pd.Series(confint[:, 1])

            fitted_series.index = pd.to_datetime(fitted_series.index)
            fitted_series.index = pd.to_datetime(fitted_series.index) - pd.DateOffset(months=8)

            forecast_start = quantity_monthly.index
            lower_series = pd.Series(confint[:, 0], index=forecast_start)
            upper_series = pd.Series(confint[:, 1], index=forecast_start)

            #fitted_series.index = fitted_series.index + pd.offsets.MonthEnd(0)  # Shift to end of the month

            plt.figure(figsize=(15,7))

            print(quantity_monthly)
            print(fitted_series)

            # Plot actual data and forecasted data
            plt.plot(quantity_monthly, color='#1f76b4', label="Actual")
            plt.plot(fitted_series.index, fitted_series, color='darkgreen', label="Forecasted")
            plt.fill_between(lower_series.index,
                            lower_series,
                            upper_series,
                            color='k', alpha=.05)


            # Set title and labels
            plt.title("SARIMA - Forecast Quantity / Demand")
            plt.legend(loc='upper left')

            # Set date format on x-axis to "Year-Month"
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

            # Rotate x-axis labels for better visibility
            plt.xticks(rotation=45)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            return img_base64, SarimaProccessor.__forecast_accuracy(fitted, quantity_monthly)
            
        



