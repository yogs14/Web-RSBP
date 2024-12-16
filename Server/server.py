from fastapi import APIRouter, FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import io
from FileData import FileDataProcessor
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import base64
import globals as g
from starlette.middleware.gzip import GZipMiddleware
from sklearn_gradient import SklearnProcessor
from MLP import MultiLayerPerceptronProccessor
from Arima import ArimaProcessor
from Sarima import SarimaProccessor

warnings.filterwarnings('ignore')
plt.switch_backend('agg')

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)  # minimum_size in bytes

@app.middleware("http")
async def dispatch(request: Request, call_next):
    response = await call_next(request)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@router.get("/status")
async def message():
    return {"message": "Hello Word"}

@router.post("/upload_file/", tags=["General"])
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file and process it.
    """
    if file.content_type != "text/csv":
        return {"error": "The uploaded file must be a CSV file"}
    
    contents = await file.read()
    return FileDataProcessor.process(contents)

@router.get("/describe_csv/", tags=["General"])
async def describe_csv() -> HTMLResponse:
    """
    Upload a CSV file and return the describe() output as an HTML table.
    """

    describe_html = FileDataProcessor.describe()
    
    return HTMLResponse(content=describe_html, status_code=200)
    
@router.get("/csv_detail/", tags=["General"])
async def upload_csv_html() -> HTMLResponse:
    """
    Upload a CSV file and return the describe() output as an HTML table.
    """

    describe_html = FileDataProcessor.describe()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSV Describe Output</title>
        <style>
            .dataframe {{
                width: 100%;
                border-collapse: collapse;
            }}
            .dataframe th, .dataframe td {{
                border: 1px solid #ddd;
                text-align: center;
                padding: 8px;
            }}
            .dataframe th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Describe Output</h1>
        {describe_html}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@router.get('/time_series_analysis/', tags=["General"])
async def time_series_analyses():
    # Create a BytesIO buffer for monthly plot
    monthly_buf = io.BytesIO()
    # Calculate monthly averages and std deviations
    monthly_window_avg = g.temp_df['total_amount'].resample('M').mean()
    monthly_window_std = g.temp_df['total_amount'].resample('M').std()
    
    # Generate the monthly plot
    plt.figure(figsize=(10, 6))
    monthly_window_avg.plot(label='Monthly Average', xlabel='Date', ylabel='Total Amount')
    monthly_window_std.plot(label='Monthly Std Deviation')
    plt.legend()
    plt.title('Average Monthly Sales and Standard Deviation')
    plt.savefig(monthly_buf, format='png')
    monthly_buf.seek(0)
    plt.close()

    # Create a BytesIO buffer for quarterly plot
    quarterly_buf = io.BytesIO()
    # Calculate quarterly averages and std deviations
    quarterly_window = g.temp_df['total_amount'].resample('Q').mean()
    quarterly_window_std = g.temp_df['total_amount'].resample('Q').std()
    
    # Generate the quarterly plot
    plt.figure(figsize=(10, 6))
    quarterly_window.plot(label='Quarterly Average', xlabel='Date', ylabel='Total Amount')
    quarterly_window_std.plot(label='Quarterly Std Deviation')
    plt.legend()
    plt.title('Average Quarterly Sales and Standard Deviation')
    plt.savefig(quarterly_buf, format='png')
    quarterly_buf.seek(0)
    plt.close()

    # Convert the plots to Base64
    monthly_image_base64 = base64.b64encode(monthly_buf.getvalue()).decode('utf-8')
    quarterly_image_base64 = base64.b64encode(quarterly_buf.getvalue()).decode('utf-8')

    # Close the buffers
    monthly_buf.close()
    quarterly_buf.close()

    # Return a JSON response with the Base64 images
    return JSONResponse(content={
        "monthly_sales_plot": f"data:image/png;base64,{monthly_image_base64}",
        "quarterly_sales_plot": f"data:image/png;base64,{quarterly_image_base64}"
    })

@router.post("/sklearn_train", tags=["Sklearn Gradient Boosting"])
async def sklearn_train():
    data = SklearnProcessor.sklearn_training()
    return JSONResponse(content={
        "best_parameter": data,
    }, status_code=200)

@router.get("/sklearn_eval", tags=["Sklearn Gradient Boosting"])
async def sklearn_eval():
    data = SklearnProcessor.model_evaluation()
    return JSONResponse(content=data
    , status_code=200)

@router.get("/sklearn_feature_importance", tags=["Sklearn Gradient Boosting"])
async def sklearn_feature_importance():
    data = SklearnProcessor.feature_importance()
    return JSONResponse(content=f"data:image/png;base64,{data}"
    , status_code=200)

@router.get("/sklearn_shap", tags=["Sklearn Gradient Boosting"])
async def sklearn_shap():
    data1, data2 = SklearnProcessor.shap_value()
    return JSONResponse(content={
        "img1": f"data:image/png;base64,{data1}",
        "img2": f"data:image/png;base64,{data2}"
    }
    , status_code=200)

@router.get("/sklearn_lime", tags=["Sklearn Gradient Boosting"])
async def sklearn_lime():
    data1, data2 = SklearnProcessor.lime()
    return JSONResponse(content={
        "html1": data1,
        "img2": f"data:image/png;base64,{data2}"
    }
    , status_code=200)

@router.get("/sklearn_predict", tags=["Sklearn Gradient Boosting"])
async def sklearn_predict():
    data = SklearnProcessor.predicted()
    return JSONResponse(content=f"data:image/png;base64,{data}"
    , status_code=200)


@router.post("/mlp_train", tags=["Multi Layer"])
async def mlp_train():
    data = MultiLayerPerceptronProccessor.mlp_training()
    return JSONResponse(content={
        "best_parameter": data,
    }, status_code=200)

@router.get("/mlp_eval", tags=["Multi Layer"])
async def mlp_eval():
    data = MultiLayerPerceptronProccessor.model_evaluation()
    return JSONResponse(content=data
    , status_code=200)

@router.get("/mlp_feature_importance", tags=["Multi Layer"])
async def mlp_feature_importance():
    data = MultiLayerPerceptronProccessor.feature_importance()
    return JSONResponse(content=f"data:image/png;base64,{data}"
    , status_code=200)

@router.get("/mlp_shap", tags=["Multi Layer"])
async def mlp_shap():
    data1, data2 = MultiLayerPerceptronProccessor.shap_value()
    return JSONResponse(content={
        "img1": f"data:image/png;base64,{data1}",
        "img2": f"data:image/png;base64,{data2}"
    }
    )

@router.get("/mlp_lime", tags=["Multi Layer"])
async def mlp_lime():
    data1, data2 = MultiLayerPerceptronProccessor.lime()
    return JSONResponse(content={
        "html1": data1,
        "img2": f"data:image/png;base64,{data2}"
    }
    , status_code=200)

@router.get("/mlp_predict", tags=["Multi Layer"])
async def mlppredict():
    data = MultiLayerPerceptronProccessor.predicted()
    return JSONResponse(content=f"data:image/png;base64,{data}"
    , status_code=200)

@router.get("/arimax_data/{param}", tags=["Arima/Arimax"])
async def arima_data(param :str) -> HTMLResponse:
    describe_html = ArimaProcessor.data(param)
    
    return HTMLResponse(content=describe_html, status_code=200)

@router.get("/arimax_train/{param}", tags=["Arima/Arimax"])
async def arima_train(param :str) -> HTMLResponse:
    data = ArimaProcessor.train(param)
    summary_html = f"<pre>{data}</pre>"

    return HTMLResponse(content=summary_html, status_code=200)

@router.get("/arimax_plot/{param}", tags=["Arima/Arimax"])
async def arima_plot(param :str):
    data = ArimaProcessor.plot(param)
    return JSONResponse(content=f"data:image/png;base64,{data}", status_code=200)

@router.get("/arimax_forecast/{param}", tags=["Arima/Arimax"])
async def arima_forecast(param :str):
    data1, data2 = ArimaProcessor.forecast(param)
    return JSONResponse(content={
        "img1": f"data:image/png;base64,{data1}",
        "data1": data2
    }
)

@router.get("/sarimax_data/{param}", tags=["Sarima/Sarimax"])
async def sarima_data(param :str) -> HTMLResponse:
    describe_html = SarimaProccessor.data(param)
    
    return HTMLResponse(content=describe_html, status_code=200)

@router.get("/sarimax_train/{param}", tags=["Sarima/Sarimax"])
async def sarima_train(param :str) -> HTMLResponse:
    data = SarimaProccessor.train(param)
    summary_html = f"<pre>{data}</pre>"

    return HTMLResponse(content=summary_html, status_code=200)

@router.get("/sarimax_plot/{param}", tags=["Sarima/Sarimax"])
async def sarima_plot(param :str):
    data = SarimaProccessor.plot(param)
    return JSONResponse(content=f"data:image/png;base64,{data}", status_code=200)

@router.get("/sarimax_forecast/{param}", tags=["Sarima/Sarimax"])
async def sarima_forecast(param :str):
    data1, data2 = SarimaProccessor.forecast(param)
    return JSONResponse(content={
        "img1": f"data:image/png;base64,{data1}",
        "data1": data2
    }
)

@router.get('/plot/', tags=["General"])
async def send_plot_as_html() -> HTMLResponse:
    """
    Generate a plot and send it as a complete HTML page.
    """
    # Calculate the monthly average and standard deviation
    monthly_window_avg = g.temp_df['total_amount'].resample('M').mean()
    monthly_window_std = g.temp_df['total_amount'].resample('M').std()

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plotting the monthly average and standard deviation
    monthly_window_avg.plot(label='Monthly Average', xlabel='Date', ylabel='Total Amount')
    monthly_window_std.plot(label='Monthly Std Deviation')

    # Add a title and legend
    plt.title('Monthly Average and Standard Deviation of Total Amount')
    plt.legend()

    # Save the plot to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Convert the plot to base64 for embedding in HTML
    plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    # Close the plot to free memory
    plt.close()

    # Construct a full HTML page with the embedded plot
    html_content = f"""
    <html>
        <head>
            <title>Monthly Sales Plot</title>
        </head>
        <body>
            <h1>Average Monthly Sales and Standard Deviation</h1>
            <p>This plot shows the average monthly sales and standard deviation over the given period.</p>
            <img src="data:image/png;base64,{plot_base64}" alt="Monthly Sales Plot" />
        </body>
    </html>
    """

    # Return the full HTML page as a response
    return HTMLResponse(content=html_content)

app.include_router(router, prefix='/api')