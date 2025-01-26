import BaseHTTPClient from "./baseHTTP";
import type { ErrorResponseCodes } from "./enums";
import type { ICreateItem, IItem, IUpdateItem, IUser } from "./types";

export interface IApiError {
  code: ErrorResponseCodes;
  message: string;
}

export interface IApiResponse<T> {
  error?: IApiError;
  data?: T;
}

class HttpClient {
  private itemsHttpClient: BaseHTTPClient;
  private usersHttpClient: BaseHTTPClient;

  private auth: { accessToken: string | null; refreshToken: string | null };

  constructor() {
    this.itemsHttpClient = new BaseHTTPClient("http://localhost:8000");
    this.usersHttpClient = new BaseHTTPClient("http://localhost:8001");
    this.auth = { accessToken: null, refreshToken: null };
  }

  setTokens({
    accessToken,
    refreshToken,
  }: {
    accessToken: string;
    refreshToken: string;
  }) {
    this.auth.accessToken = accessToken;
    this.auth.refreshToken = refreshToken;
  }

  async refreshAccessToken() {
    this.auth.accessToken = null;
    const res = await this.usersHttpClient.request<{
      access_token: string;
    }>("POST", "/auth/refresh", { auth: this.auth });
    if (res.data) {
      this.auth.accessToken = res.data.access_token;
    }
    return res;
  }

  async signIn(email: string, password: string) {
    const form = new FormData();
    form.append("email", email);
    form.append("password", password);

    const res = await this.usersHttpClient.request<{
      access_token: string;
      refresh_token: string;
    }>("POST", "/auth/signin", { data: form });

    if (res.data) {
      this.auth.accessToken = res.data.access_token;
      this.auth.refreshToken = res.data.refresh_token;
    }

    return res;
  }

  signUp(email: string, name: string, password: string) {
    const form = new FormData();
    form.append("email", email);
    form.append("name", name);
    form.append("password", password);
    return this.usersHttpClient.request("POST", "/auth/signup", { data: form });
  }

  getUsers() {
    return this.usersHttpClient.request<IUser[]>("GET", "/users", {
      auth: this.auth,
    });
  }

  getUser(userId: number) {
    return this.usersHttpClient.request<IUser>("GET", `/users/${userId}`, {
      auth: this.auth,
    });
  }

  getMe() {
    return this.usersHttpClient.request<IUser>("GET", "/users/me", {
      auth: this.auth,
    });
  }

  updateMe(payload) {
    return this.usersHttpClient.request<IUser>("PATCH", "/users/me", {
      data: payload,
      auth: this.auth,
    });
  }

  getAllItems() {
    return this.itemsHttpClient.request<IItem[]>("GET", "/items");
  }

  getUserItems() {
    return this.itemsHttpClient.request<IItem[]>("GET", "/items/me", {
      auth: this.auth,
    });
  }

  getItemById(itemId: number) {
    return this.itemsHttpClient.request("GET", `/items/${itemId}`);
  }

  createItem(payload: ICreateItem) {
    const { image, ...data } = payload;
    return this.itemsHttpClient.request("POST", "/items", {
      data,
      file: image,
      auth: this.auth,
    });
  }

  updateItem(itemId: number, payload: IUpdateItem) {
    return this.itemsHttpClient.request("PATCH", `/items/${itemId}`, {
      data: payload,
      auth: this.auth,
    });
  }

  deleteItem(itemId: number) {
    return this.itemsHttpClient.request("DELETE", `/items/${itemId}`, {
      auth: this.auth,
    });
  }
}

const httpClient = new HttpClient();
export { httpClient };
