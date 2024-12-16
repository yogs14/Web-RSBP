import { fetchData } from './Fetch'

const API_URL = 'http://127.0.0.1:8000/api'

 // Sklearn Gradient Boosting Regressor
export const SarimaData = async (param: string) => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sarimax_data/${param}`, {
        method: 'GET',
        headers: {
            'Accept': 'text/html',
        },
        parseJson: false
      });
  
      // Handle response
      if (data) {
        const htmlData = await data.text()
        console.log("Succesfully Train", data);
        return htmlData
        //const sklearn_data = Sklearn
        //sklearn_data.training_result = data.best_parameter
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }

  export const SarimaTrain = async (param: string) => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sarimax_train/${param}`, {
        method: 'GET',
        headers: {
            'Accept': 'text/html',
        },
        parseJson: false
      });
  
      // Handle response
      if (data) {
        const htmlData = await data.text()
        console.log("Succesfully Train", data);
        return htmlData
        //const sklearn_data = Sklearn
        //sklearn_data.training_result = data.best_parameter
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }

  export const SarimaPlot = async (param: string) => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sarimax_plot/${param}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Plot", data);
        return data
        //const sklearn_data = Sklearn
        //sklearn_data.training_result = data.best_parameter
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }

  export const SarimaForecast = async (param: string) => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sarimax_forecast/${param}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Forecast", data);
        return data
        //const sklearn_data = Sklearn
        //sklearn_data.training_result = data.best_parameter
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }

