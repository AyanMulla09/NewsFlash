import axios from 'axios'
import qs from 'qs'
const http = axios.create({
  method: 'get', // default value
  baseURL: process.env.NODE_ENV === 'development' ? '/api' : '', // base URL
  timeout: 30000,
  withCredentials: false,
  responseType: 'json',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  transformRequest: [
    function (data) {
      return qs.stringify(data);
    },
  ],
});

http.interceptors.request.use(
  (axiosConfig) => {
    // logic processing
    return axiosConfig;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response Interception
http.interceptors.response.use(
  (response) => {
    const { data } = response;
    return data;
  },
  (error) => {
    console.error('Network error:', error);
    return Promise.reject(error);
  },
);
export function fetchData(url, method = 'get', params = {}, data = {}) {
  return http({
    url,
    method,
    params,
    data,
  });
}

export default http;
