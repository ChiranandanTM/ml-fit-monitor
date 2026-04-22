import axios from "axios";

const API = "http://localhost:9000";

// Add timeout to all requests - 90 seconds
const API_TIMEOUT = 90000; // 90 seconds

export const uploadDataset = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/train`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: API_TIMEOUT
    });
    
    console.log("API response:", res.data);
    return res.data;
  } catch (error: any) {
    console.error("API error:", error.response?.data || error.message);
    throw error;
  }
};

export const generateDataset = async (fitType: "good_fit" | "overfitting" | "underfitting") => {
  try {
    const res = await axios.get(`${API}/generate-dataset/${fitType}`, {
      timeout: API_TIMEOUT
    });
    return res.data;
  } catch (error: any) {
    console.error("Generate dataset error:", error.response?.data || error.message);
    throw error;
  }
};

export const simulateDrift = async (data: any) => {
  try {
    const res = await axios.post(`${API}/simulate-drift`, data, {
      timeout: API_TIMEOUT
    });
    return res.data;
  } catch (error: any) {
    console.error("Drift API error:", error.response?.data || error.message);
    throw error;
  }
};

export const getComprehensiveAnalysis = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/analyze`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: API_TIMEOUT
    });
    
    return res.data;
  } catch (error: any) {
    console.error("Analysis API error:", error.response?.data || error.message);
    throw error;
  }
};

export const getSuggestions = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/suggest`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: API_TIMEOUT
    });
    
    return res.data;
  } catch (error: any) {
    console.error("Suggestions API error:", error.response?.data || error.message);
    throw error;
  }
};

export const getDriftSimulation = async (file: File) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/drift-simulate`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: API_TIMEOUT
    });
    
    return res.data;
  } catch (error: any) {
    console.error("Drift simulation API error:", error.response?.data || error.message);
    throw error;
  }
};

export const improveFitDataset = async (file: File, strategy: "best_model" | "generic" = "best_model") => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/improve-fit?strategy=${strategy}`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      timeout: API_TIMEOUT
    });

    return res.data;
  } catch (error: any) {
    console.error("Improve fit API error:", error.response?.data || error.message);
    throw error;
  }
};

