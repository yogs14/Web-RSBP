/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, ChangeEvent , useRef} from 'react'
import Navbar from './Components/Navbar'
import { fetchData } from './Utils/Fetch'

function App() {
  const isUploadedRef = useRef(false);
  const fileNameRef = useRef('');
  const [file, setFile] = useState<File | null>(null);
  const [action, setAction] = useState("")
  const [isLoading, setIsLoading] = useState(false);
  const [htmlContent, setHtmlContent] = useState<string>(''); // To store HTML response

  const [monthlyImage, setMonthlyImage] = useState('')
  const [quarterlyImage, setQuarterlyImage] = useState('')

  const [Sklearn, setSklearn] = useState(
    {training_result : ""}
  )

  const API_URL = 'http://127.0.0.1:8000/api'

  const handleFileChange = (event :ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files![0];
    
    const fileName = uploadedFile.name;
    fileNameRef.current = fileName
    console.log("Uploaded file name:", fileName);

    if (event.target.files) {
      setFile(event.target.files[0]);
      console.log('success')
    }
  };

  const handleSelectChange = (event :ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    setAction(selectedValue)
    console.log('Selected Action:', selectedValue); // Log the selected value
  };

  const HandleSubmit = () => {
    switch (action) {
      case 'Upload File':
        if (!file) {
          alert("Please select a file to upload.");
          return;
        }

        HandleSubmitFile();
        break;

      case 'Time Series Analytics':
        console.log("Performing Time Series Analytics...");
        TimeSeriesAnalysis()
        break;

      case 'Train Model':
        console.log("Training Model...");
        break;

      default:
        console.log("No action selected.");
    }
  }

  const HandleSubmitFile = async () => {
    setIsLoading(true); 

    const formData = new FormData();
  
    // Ensure the file exists
    if (!file) {
      console.error("No file selected");
      return;
    }

  formData.append('file', file); 


  try {
      const data = await fetchData(`${API_URL}/upload_file`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
        body: formData,
      });
  
      // Handle response
      if (data) {
        console.log("File uploaded successfully:", data);
        isUploadedRef.current = true
        describeCSV()
        setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during file upload:", error);
      setIsLoading(false); 
    }
  }

  const describeCSV = async () => {
    try {
      const data = await fetchData(`${API_URL}/describe_csv`, {
        method: 'GET',
        headers: {
          'Accept': 'text/html',
        },
        parseJson: false
      });
  
      // Handle response
      if (data) {
        const htmlData = await data.text()
        setHtmlContent(htmlData); // Store HTML content to state
      } 
    } catch (error) {
      console.error("Error during file upload:", error);
      setIsLoading(false); 
    }
  }

  const TimeSeriesAnalysis = async () => {
    setIsLoading(true); 

    try {
      const data = await fetchData(`${API_URL}/time_series_analysis`, {
        method: 'GET',
        headers: {
          'Accept': 'text/html',
        },
        parseJson: true
      });
  
      // Handle response
      if (data) {
        setMonthlyImage(data.monthly_sales_plot)
        setQuarterlyImage(data.quarterly_sales_plot)
        setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during file upload:", error);
      setIsLoading(false); 
    }
  }
  

  return (
    <>
      <div className='h-screen'>
        <Navbar/>

          <div className='text-center mt-4 font-semibold'>
            Forms
          </div>  

          <div className="text-primary-content w-fit p-4 border border-secondary border-solid ml-4 rounded-lg">
              <div className='flex flex-row gap-4'>
              <p className='font-semibold'>Data Uploaded : </p>
              <p className={`font-semibold ${isUploadedRef.current ? 'text-green-500' : 'text-red-600'}`}>
                {isUploadedRef.current ? "True" : "False"}
              </p>
              </div>

              {fileNameRef.current && (
                <div className='flex flex-row gap-4'>
                  <p className='font-semibold'>File : </p>
                  <p className={`font-semibold text-green-600`}>
                    {<p> {fileNameRef.current} </p>}
                  </p>
                </div>
              )}
          </div>


          <div className="max-w-md mx-auto mt-10 shadow-mx bg-[#f5f2f2] rounded-xl">
            <div className="p-6 ">
                {/* Name Field */}
                <div className="form-control mb-4">
                  <label className="label" htmlFor="name">
                    <span className="label-text font-semibold">Pick Action</span>
                  </label>

                  <select className="select select-success w-full rounded-lg" onChange={handleSelectChange} defaultValue={""} >
                    <option disabled value="">
                      Pick Action
                    </option>
                  <option value="Upload File">Upload File</option>
                  <option value="Time Series Analytics">Time Series Analytics</option>
                  <option value="Model Training & Evaluation">Model Training & Evaluation</option>
                  </select>
                </div>

                {action === 'Upload File' && (
                  <div className="form-control mb-4 w-full transition-all duration-1000 ease-in-out">
                    <div className="label-text font-semibold text-center flex justify-center itme-center mb-2 mt-4">Upload Your Data</div>
                    <input 
                        type="file" 
                        className="file-input file-input-bordered w-full rounded-xl" 
                        accept=".csv, .xlsx, .xls, .json, .tsv, .txt" 
                        onChange={handleFileChange}
                        required/>
                 </div>
                )}

              {action === 'Model Training & Evaluation' && (
                <>
                  <div className="form-control mb-4 w-full transition-all duration-1000 ease-in-out">
                    <div className="label-text font-semibold  mb-2 mt-4">Select the model</div>
                    
                    <select className="select select-success w-full rounded-lg"  defaultValue={""} >
                        <option disabled value="">
                          Pick Model
                        </option>
                      <option value="Sklearn Gradient Boosting Regressor">Sklearn Gradient Boosting Regressor</option>
                      <option value="Multi-layer Perceptron regressor">Multi-layer Perceptron regressor</option>
                      <option value="Arima">Arima/Arimax</option>
                      <option value="Sarima">Sarima/Sarimax</option>
                      </select>
                 </div>

                 <div className="form-control mb-4 w-full transition-all duration-1000 ease-in-out">
                    <div className="label-text font-semibold  mb-2 mt-4">Options</div>
                    
                    <select className="select select-success w-full rounded-lg"  defaultValue={""} >
                        <option disabled value="">
                          Select Options
                        </option>
                      <option value="Training">Training</option>
                      <option value="Evaluation">Evaluation</option>
                      <option value="Feature Importances">Feature Importances</option>
                      <option value="Shap Values">Shap Values</option>
                      <option value="Lime">Lime Values</option>
                      <option value="PredictedValues">Predicted VS Actual Value</option>

                      </select>
                 </div>
                
                </>
                )}


                <div className="form-control transition-all ease-in-out mt-12">
                      <button 
                        type="submit" 
                        className="btn btn-accent w-full rounded-2xl" 
                        onClick={() => HandleSubmit()}
                        disabled={isLoading}>
                        Submit
                      </button>
                </div>
            </div>
        </div>
        
        { action === 'Upload File' && (
          <>
          <div className='font-semibold mt-8 text-center text-gray-600 underline'>   File summary  </div>
          <div
          className="html-table-container mt-6"
          dangerouslySetInnerHTML={{ __html: htmlContent }}
          />
          </>
        )
        }

    { action === 'Time Series Analytics' && (
      <div className="flex flex-col lg:flex-row gap-6 mt-12 justify-center items-center">
        {monthlyImage && (
          <img
            src={monthlyImage}
            alt="Monthly time series analysis chart"
            className="flex-grow max-w-[45%] object-contain"
          />
        )}
        {quarterlyImage && (
          <img
            src={quarterlyImage}
            alt="Quarterly time series analysis chart"
            className="flex-grow max-w-[45%] object-contain"
          />
        )}
      </div>
    )}




      </div>
    </>
  )
}

export default App
