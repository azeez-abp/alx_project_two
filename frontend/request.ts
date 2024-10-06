import axios from 'axios';

// Backend API path
export const backend_path = "http://127.0.0.1:9393";

// Axios global configuration to allow credentials (cookies) to be sent
axios.defaults.withCredentials = true;

// Axios request function with improved error handling and debugging
export const makeRequest = async (
  url: string,
  data: any,
  cb: (error?: object | null | any, response?: object | null | any) => void,
  mtd?: string,
  headers_opt?: any
): Promise<void> => {
  // Set default or custom headers
  const header_setting = headers_opt !== undefined
    ? headers_opt
    : {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem("alx_token")}`,
      };

  const options = {
    method: mtd ? mtd : 'POST',
    headers: header_setting,
    data: data,
    url: `${backend_path}/api/v1/${url}`,  // Ensure this path is correct
    withCredentials: true,  // Include credentials (cookies)
  };

  try {
    // Make the request with Axios
    const response = await axios(options);
    const out = response.data;

    if (out.error === true) {
      return cb(out, null);
    }

    // Successful response, return the data
    return cb(null, out);
  } catch (error: any) {
    console.error("Axios error:", error);  // Improved logging for debugging

    if (error.response) {
      // The request was made and the server responded with a status code that falls out of the range of 2xx
      if (error.response.data && error.response.data.error) {
        return cb(error.response.data, null);
      }

      return cb({ error: `Error from server: ${error.response.status}` }, null);
    } else if (error.request) {
      // The request was made but no response was received
      console.error("No response received from the server:", error.request);
      return cb({ error: "No response received from the server" }, null);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error("Axios setup error:", error.message);
      return cb({ error: error.message }, null);
    }
  }
};
