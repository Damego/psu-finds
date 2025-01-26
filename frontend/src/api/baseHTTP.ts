import axios, { AxiosInstance } from "axios";
import { ErrorResponseCodes } from "./enums";
import { getErrorMessage } from "./errorMessage";

export interface IApiError {
  code: ErrorResponseCodes;
  message: string;
}

export interface IApiResponse<T> {
  error?: IApiError;
  data?: T;
}

export default class BaseHTTPClient {
  private client: AxiosInstance;

  constructor(baseUrl: string) {
    this.client = axios.create({ baseURL: baseUrl, validateStatus: (status) => status < 500, withCredentials: true });
  }

  async request<T>(
    method: string,
    endpoint: string,
    {
      data,
      file,
      asFormData,
      auth
    }: { data?: object; file?: File; asFormData?: boolean; auth?: {accessToken: string | null; refreshToken: string | null} } = {}
  ): Promise<IApiResponse<T>> {
    let payload = undefined;

    if (file) {
      payload = new FormData();
      payload.append("file", file);
      if (data) {
        payload.append("json_payload", JSON.stringify(data));
      }
    } else if (asFormData) {
      payload = new FormData();
      Object.entries(data).forEach(([key, value]) => {
        payload.append(key, value);
      });
    } else {
      payload = data;
    }
    console.log(`[HTTP] [${method}] '${endpoint}' data: ${payload}`);
    let cookies = "";
    // if (auth) {
    //     if (auth.accessToken) cookies += `access_token=${auth.accessToken}; `;
    //     if (auth.refreshToken) cookies += `refresh_token=${auth.refreshToken}; `;
    // }

    const response = await this.client.request({
      method,
      url: endpoint,
      data: payload,
      headers: {
        "Content-Type":
          payload instanceof FormData
            ? "multipart/form-data"
            : "application/json",
        // Cookie: cookies,
      },
    });

    if (response.status >= 400) {
      const error = {
        code: response.data.detail.code,
        message: getErrorMessage(response.data.detail.code),
      };

      console.error(
        `HTTP Error with code ${error.code}. Message: ${error.message}`
      );
      return { error };
    }
    return {
      data: response.data,
    };
  }
}
