from sklearn.neural_network import MLPRegressor
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
from typing import Any, Optional
from sklearn.inspection import permutation_importance

X: pd.DataFrame | Any                   = None
y: pd.DataFrame | Any                   = None
X_train: Any                            = None
X_test: Any                             = None
y_train: Any                            = None
y_test: Any                             = None
X_train_scaled: Optional[pd.DataFrame]  = None
X_test_scaled: Optional[pd.DataFrame]   = None
shap_values_KNN_test                    = None
shap_values_KNN_train                   = None
explainerKNN                            = None
isShaped                                = False
plt.switch_backend('agg')

class MultiLayerPerceptronProccessor:
    @staticmethod
    def mlp_training():
        global X, y, X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled
        
        if g.mlp_model == None:
            # Split the data into training and testing sets
            X = g.df[['transaction_id', 'month', 'year', 'day_of_week', 'day_of_month', 'gender', 'age', 'product_category', 'total_amount', 'price_per_unit']]
            y = g.df['quantity']

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Apply scaling to the features
            scaler = StandardScaler()
            X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
            X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

            # Define the parameter grid for MLPRegressor
            param_grid = {
                'hidden_layer_sizes': [(100,), (100, 50, 25)],  # Different architectures
                'activation': ['tanh'],                            # Activation functions
                'solver': ['adam'],                                # Optimization solvers
                'learning_rate': ['adaptive'],                 # Learning rate schedules
                'alpha': [0.01, 0.1],                            # Regularization term (L2 penalty)
                'max_iter': [1000],
            }

            # Initialize the MLPRegressor model
            mlp_model = MLPRegressor(random_state=42)

            # Perform grid search with cross-validation using the scaled features
            grid_search = GridSearchCV(estimator=mlp_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1, n_jobs=-1)
            grid_search.fit(X_train_scaled, y_train)

            # Evaluate the best model on the test set
            g.mlp_model = grid_search.best_estimator_
            y_pred = g.mlp_model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)

            print(f"Mean Squared Error: {mse:.3f}")
            print(f"Best Parameters: {grid_search.best_params_}")
            g.mlp_param = grid_search.best_params_
            return grid_search.best_params_
            
        else:
            return g.mlp_param
        
    def model_evaluation():
        # Make predictions with the best model
        global y_test, X_test_scaled

        y_pred = g.mlp_model.predict(X_test_scaled)

        # Calculate RMSE
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # Calculate R-Score
        r2 = g.mlp_model.score(X_test_scaled, y_test)

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
        global X_test_scaled, y_test
        buf = io.BytesIO()
        result = permutation_importance(g.mlp_model, X_test_scaled, y_test, n_repeats=10, random_state=42, n_jobs=-1)

        # Extract importance scores
        importance_scores = result.importances_mean  # Mean of the importance scores
        feature_names = X.columns  # Feature names (assuming your data is in a DataFrame)

        # Sort feature importances for better visualization
        sorted_idx = np.argsort(importance_scores)
        sorted_importances = importance_scores[sorted_idx]
        sorted_features = feature_names[sorted_idx]

        # Create a bar plot
        plt.figure(figsize=(10, 6))
        plt.barh(sorted_features, sorted_importances, color='skyblue')
        plt.xlabel("Feature Importance")
        plt.title("Permutation Feature Importance for MLPRegressor")
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        image_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        return image_b64
    
    def shap_value():
        global X_test_scaled,X_train_scaled, shap_values_KNN_test, shap_values_KNN_train, X_train, isShaped, explainerKNN

        # Assume g.df and g.sklearn_model are defined
        if isShaped == False:

            X_train_summary = shap.kmeans(X_test_scaled, 30)

            explainerKNN = shap.KernelExplainer(g.mlp_model.predict, X_train_summary)
            shap_values_KNN_test = explainerKNN.shap_values(X_test_scaled)
            shap_values_KNN_train = explainerKNN.shap_values(X_train_scaled)
            isShaped = True

        df_shap_KNN_test = pd.DataFrame(shap_values_KNN_test, columns=X_test.columns.values)
        df_shap_KNN_train = pd.DataFrame(shap_values_KNN_train, columns=X_train.columns.values)

        instance_index = 171                     
        shap_values_instance = shap_values_KNN_train[instance_index]
        # Get the corresponding data from the NumPy array (X_train_scaled is a NumPy array)
        instance_data = X_train_scaled.iloc[instance_index, :]

        # Create the Explanation object
        explainer_instance = shap.Explanation(values=shap_values_instance,
                                            base_values=explainerKNN.expected_value,
                                            data=instance_data)

        # Create a waterfall plot for that instance
        buffer1 = io.BytesIO()
        plt.figure()  # Create a new figure
        plt.figure(figsize=(20, 7)) 
        shap.waterfall_plot(explainer_instance, show=False)
        # Capture the current figure
        fig = plt.gcf()
        # Modify the figure size
        fig.set_size_inches(20, 6)
        plt.savefig(buffer1, format='png')
        plt.close()  # Close the figure to prevent display
        buffer1.seek(0)  # Reset the buffer pointer

        buffer2 = io.BytesIO()
        plt.figure()  # Create a new figure
        plt.figure(figsize=(17, 7)) 
        shap.summary_plot(shap_values_KNN_train, X_train, show=False)  # This returns an Axes object
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
        global X_train
        instance = X_train.iloc[2]

        # Create a LIME explainer with mode='regression'
        lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            X_train.values,
            feature_names=X_train.columns.values,  # Use actual column names from X_train
            mode='regression',  # Set mode to 'regression'
            discretize_continuous=True
        )

        # Get the LIME explanation for the chosen instance
        lime_explanation = lime_explainer.explain_instance(instance, g.mlp_model.predict, num_features=10)
        exp = lime_explanation.as_list()
        features, effects = zip(*exp)

        exp_df = pd.DataFrame({'Feature': features, 'Effect': effects})
        exp_html = exp_df.to_html(index=False, classes='dataframe', border=1)
        
        # Visualize the explanation
        buffer2 = io.BytesIO()
        plt.figure(figsize=(20, 6))  # Set a larger figure size
        fig = lime_explanation.as_pyplot_figure()
        # Adjust the figure size (width=10, height=5 in inches, for example)
        fig.set_size_inches(20, 6)
        fig.savefig(buffer2, format='png')
        plt.close()
        buffer2.seek(0)  # Reset the buffer pointer

        # Convert buffers to Base64
        img2_base64 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        buffer2.close()

        return exp_html, img2_base64
    
    def predicted():
        # Create a DataFrame for plotting
        global X_test, y_test, X_test_scaled
        y_pred = g.mlp_model.predict(X_test_scaled)
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

