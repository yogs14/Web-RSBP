/* eslint-disable @typescript-eslint/no-explicit-any */
// utils/fetchUtils.ts

interface FetchOptions extends RequestInit {
    body?: any;
    headers?: Record<string, string>;
    parseJson?: boolean
  }
  
  // Generic fetch function
export const fetchData = async (
url: string,
options: FetchOptions = {}
): Promise<any> => {
const {method, body, parseJson=true, headers, ...restOptions } = options;

    const response = await fetch(url, {
    method: method ? method : 'GET', 
    headers: { 
        ...headers,
    },
    body: body,
    ...restOptions,
    });

    // Check if response is successful (status code 200-299)
    if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Parse response as JSON (default) or plain text if specified
    if (parseJson) {
        return response.json();
    }

    return response
    
};

