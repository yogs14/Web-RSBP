import { fetchData } from './Utils/Fetch'

const API_URL = 'http://127.0.0.1:8000/api'

 // Sklearn Gradient Boosting Regressor
export const sklearnTrain = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sklearn_train`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Train", data);
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

  export  const sklearnEvaluation = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sklearn_eval`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Eval", data);
        return data
        //const sklearn_data = Sklearn
        //sklearn_data.evaluation = data.evaluation
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }
  
export const sklearnFeatureImportance = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sklearn_feature_importance`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        return data
        //console.log("Succesfully Eval", data);
        //const sklearn_data = Sklearn
        //sklearn_data.feature_importance = data
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }

export const sklearnShapValues = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sklearn_shap`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Shap", data);
        return data
        //const sklearn_data = Sklearn
        //sklearn_data.shap = data
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }

  
export const sklearnLimeValues = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/sklearn_lime`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Lime", data);
        return data
        //const sklearn_data = Sklearn
        //sklearn_data.lime = data
        //setSklearn(sklearn_data)
        //console.log(sklearn_data)
        //setIsLoading(false); 
      } 
    } catch (error) {
      console.error("Error during Training", error);
      //setIsLoading(false); 
    }
  }
