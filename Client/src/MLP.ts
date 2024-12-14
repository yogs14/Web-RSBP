import { fetchData } from './Utils/Fetch'

const API_URL = 'http://127.0.0.1:8000/api'

 // Sklearn Gradient Boosting Regressor
export const mlpTrain = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/mlp_train`, {
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

  export  const mlpEvaluation = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/mlp_eval`, {
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
  
export const mlpFeatureImportance = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/mlp_feature_importance`, {
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

export const mlpShapValues = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/mlp_shap`, {
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

  
export const mlpLimeValues = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/mlp_lime`, {
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

  export const mlpPredictedGraph = async () => {
    //setIsLoading(true)
    try {
      const data = await fetchData(`${API_URL}/mlp_predict`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });
  
      // Handle response
      if (data) {
        console.log("Succesfully Predicted", data);
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
