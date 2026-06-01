import { createContext, useContext, useEffect, useMemo, useState } from "react";
import api from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(Boolean(localStorage.getItem("access_token")));

  const fetchProfile = async () => {
    const response = await api.get("/auth/profile/");
    setUser(response.data);
    return response.data;
  };

  useEffect(() => {
    if (!localStorage.getItem("access_token")) {
      return;
    }
    fetchProfile()
      .catch(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      })
      .finally(() => setIsLoading(false));
  }, []);

  const login = async (username, password) => {
    const response = await api.post("/auth/login/", { username, password });
    localStorage.setItem("access_token", response.data.access);
    localStorage.setItem("refresh_token", response.data.refresh);
    return fetchProfile();
  };

  const register = async (payload) => {
    await api.post("/auth/register/", payload);
    return login(payload.username, payload.password);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, isAuthenticated: Boolean(user), isLoading, login, register, logout, fetchProfile, setUser }),
    [user, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
