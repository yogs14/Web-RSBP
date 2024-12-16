from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import globals as g
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import shap
import lime
import pandas as pd
plt.switch_backend('agg')

class SklearnProcessor:
    @staticmethod
    def sklearn_training():
        if g.sklearn_model == None:
            # Split the data into training and testing sets
            X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
            y = g.df['quantity']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Apply scaling to the features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # Define the parameter grid for GradientBoostingRegressor
            param_grid = {
                'n_estimators': [50, 100, 200],           # Number of boosting stages (trees)
                'learning_rate': [0.01, 0.1, 0.2],        # Learning rate shrinks the contribution of each tree
                'max_depth': [3, 5, 7],                    # Maximum depth of individual trees
                'min_samples_split': [2, 5, 10],           # Minimum number of samples required to split an internal node
                'subsample': [0.8, 1.0]                    # Fraction of samples used for fitting each tree
            }

            # Initialize the GradientBoostingRegressor model
            gb_model = GradientBoostingRegressor(random_state=42)

            # Perform grid search with cross-validation using the scaled features
            grid_search = GridSearchCV(estimator=gb_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
            grid_search.fit(X_train, y_train)

            # Evaluate the best model on the test set
            g.sklearn_model = grid_search.best_estimator_
            y_pred = g.sklearn_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            print(f"Mean Squared Error: {mse:.3f}")
            print(f"Best Parameters: {grid_search.best_params_}")
            g.sklearn_param = grid_search.best_params_

            return grid_search.best_params_
        else:
            return g.sklearn_param
        
    def model_evaluation():
        # Best model from grid search
        X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
        y = g.df['quantity']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Make predictions with the best model
        y_pred = g.sklearn_model.predict(X_test)

        # Calculate RMSE
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Calculate R-Score
        r2 = g.sklearn_model.score(X_test, y_test)

        # Calculate MAE
        mae = np.mean(np.abs(y_test - y_pred))

        # Calculate MAPE
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        print(f"RMSE: {rmse}")
        print(f"R-Score: {r2}")
        print(f"MAE: {mae}")
        print(f"MAPE: {mape}")

        return {'evaluation': {'rmse': rmse, 'r2': r2, 'mae': mae, 'mape': mape}}
    
    def feature_importance():
        # Extract feature importances from the best model
        buf = io.BytesIO()
        X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
        feature_importances = g.sklearn_model.feature_importances_
        feature_names = X.columns

        # Sort feature importances for better visualization
        sorted_idx = np.argsort(feature_importances)
        sorted_importances = feature_importances[sorted_idx]
        sorted_features = feature_names[sorted_idx]

        # Create a bar plot
        plt.figure(figsize=(10, 6))
        plt.barh(sorted_features, sorted_importances, color='skyblue')
        plt.xlabel("Feature Importance")
        plt.title("Feature Importance in Sklearn Gradient Boosting Regressor")
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        image_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return image_b64
    
    def shap_value():
        # Assume g.df and g.sklearn_model are defined
        X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
        y = g.df['quantity']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        explainer = shap.Explainer(g.sklearn_model)
        shap_values = explainer(X_test)

        # Create a buffer for the waterfall plot
        buffer1 = io.BytesIO()
        ax = shap.plots.waterfall(shap_values[3], show=False)  # This returns an Axes object
        # Access the parent figure of the Axes object
        fig = ax.figure
        # Set the figure size after creating the plot
        fig.set_size_inches(18, 7) 
        plt.savefig(buffer1, format='png')
        plt.close(fig)  
        buffer1.seek(0)  

        # Create a buffer for the summary plot
        buffer2 = io.BytesIO()
        plt.figure()  # Create a new figure
        plt.figure(figsize=(10, 7)) 
        shap.summary_plot(shap_values, X_test, show=False)  
        plt.savefig(buffer2, format='png')
        plt.close()  # Close the figure to prevent display
        buffer2.seek(0)  # Reset the buffer pointer

        # Convert buffers to Base64
        img1_base64 = base64.b64encode(buffer1.getvalue()).decode('utf-8')
        img2_base64 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        buffer1.close()
        buffer2.close()
        return img1_base64, img2_base64

    def lime():
        X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
        y = g.df['quantity']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        instance = X_test.iloc[3]

        # Create a LIME explainer with mode='regression'
        lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train.values,
            feature_names=X_train.columns.values,  # Use actual column names from X_train
            mode='regression',  # Set mode to 'regression'
            discretize_continuous=True
        )

        # Get the LIME explanation for the chosen instance
        lime_explanation = lime_explainer.explain_instance(instance, g.sklearn_model.predict, num_features=10)
        exp = lime_explanation.as_list()
        features, effects = zip(*exp)

        exp_df = pd.DataFrame({'Feature': features, 'Effect': effects})
        exp_html = exp_df.to_html(index=False, classes='dataframe', border=1)
        
        # Visualize the explanation
        buffer2 = io.BytesIO()
        plt.figure(figsize=(14, 6))  # Set a larger figure size
        fig = lime_explanation.as_pyplot_figure()
        # Adjust the figure size (width=10, height=5 in inches, for example)
        fig.set_size_inches(16, 6)
        fig.savefig(buffer2, format='png')
        plt.close()
        buffer2.seek(0)  # Reset the buffer pointer

         # Convert buffers to Base64
        img2_base64 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        buffer2.close()

        return exp_html, img2_base64
    
    def predicted():
        # Create a DataFrame for plotting
        X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
        y = g.df['quantity']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        instance = X_test.iloc[0]

        y_pred = g.sklearn_model.predict(X_test)
        plot_df = pd.DataFrame({'Year-Month': pd.to_datetime(X_test['year'].astype(str) + '-' + X_test['month'].astype(str), format='%Y-%m'),
                            'Actual': y_test,
                            'Predicted': y_pred})

        # Group by 'Year-Month' and get the mean for visualization
        plot_df = plot_df.groupby('Year-Month').mean()

        # Plotting without grouping
        buffer = io.BytesIO()
        plt.figure(figsize=(15, 6))
        plt.scatter(plot_df.index, plot_df['Actual'], label='Actual Sales', marker='o', alpha=0.5)  # Scatter plot for actual
        plt.plot(plot_df.index, plot_df['Predicted'], label='Predicted Sales', linestyle='-', color='red')  # Line plot for predicted
        plt.xlabel('Year-Month')
        plt.ylabel('Sales Amount')
        plt.title('Actual vs. Predicted Sales Over Time')
        plt.legend()
        plt.grid(True)
        plt.savefig(buffer, format='png')
        plt.close()  # Close the figure to prevent display
        buffer.seek(0)  # Reset the buffer pointer

        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        return img_base64

'''
        exp = lime_explanation.as_list()

        # Separate features and their effects
        features, effects = zip(*exp)

        # Convert explanation into a DataFrame for tabular display
        exp_df = pd.DataFrame({'Feature': features, 'Effect': effects})

        # Create a horizontal bar plot
        plt.figure(figsize=(8, 6))
        plt.barh(features, effects, color='skyblue')
        plt.xlabel('Effect')
        plt.title('LIME Explanation')
        plt.gca().invert_yaxis()  # Invert y-axis to match LIME's display order
        plt.tight_layout()

        # Show the plot
        plt.show()

        # Print the table
        print("LIME Explanation Table:")
        print(exp_df.to_string(index=False))

        # Show the plot
        plt.show()       

        fig = lime_explanation.as_pyplot_figure()

        # Adjust the figure size (width=10, height=5 in inches, for example)
        fig.set_size_inches(15, 5)
'''

