import React, { createContext, useEffect, useState } from "react";
import Cookies from "js-cookie";
import { httpClient } from "src/api/client";
import { type IUser } from "src/api/types";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<IUser>();

  useEffect(() => {
    // const accessToken = Cookies.get("access_token");
    // const refreshToken = Cookies.get("refresh_token");

    // console.log("CCOKIE", accessToken)

    // if (!accessToken) return;

    // httpClient.setTokens({ accessToken, refreshToken });
    httpClient.getMe().then((res) => {
      if (res.data) {
        setUser(res.data);
      }
    });
  }, []);

  const setUserData = (user: IUser) => {
    if (user === null) {
      Cookies.remove("access_token");
      Cookies.remove("refresh_token");
    } else setUser(user);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        setUserData,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
