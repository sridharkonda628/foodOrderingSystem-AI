import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, UserRole } from '../types';
import { authApi } from '../api/authApi';

interface AuthContextType {
  user: User | null;
  token: string | null;
  role: UserRole | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string, role?: string) => Promise<void>;
  logout: () => void;
  switchUser: (role: UserRole) => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('kpitech_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('kpitech_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('kpitech_token');
      if (savedToken) {
        try {
          const res = await authApi.getMe();
          if (res.success && res.data) {
            setUser(res.data);
            localStorage.setItem('kpitech_user', JSON.stringify(res.data));
          }
        } catch {
          logout();
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await authApi.login(email, password);
    if (res.success && res.data) {
      setToken(res.data.access_token);
      setUser(res.data.user);
      localStorage.setItem('kpitech_token', res.data.access_token);
      localStorage.setItem('kpitech_user', JSON.stringify(res.data.user));
    }
  };

  const register = async (email: string, password: string, fullName: string, role: string = 'customer') => {
    const res = await authApi.register(email, password, fullName, role);
    if (res.success && res.data) {
      setToken(res.data.access_token);
      setUser(res.data.user);
      localStorage.setItem('kpitech_token', res.data.access_token);
      localStorage.setItem('kpitech_user', JSON.stringify(res.data.user));
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('kpitech_token');
    localStorage.removeItem('kpitech_user');
  };

  const switchUser = async (targetRole: UserRole) => {
    if (targetRole === 'admin') {
      await login('admin@kpitech.com', 'AdminPass123!');
    } else {
      await login('customer@example.com', 'CustomerPass123!');
    }
  };

  const role = user ? (user.role as UserRole) : null;
  const isAuthenticated = !!token && !!user;
  const isAdmin = role === 'admin';

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        role,
        isAuthenticated,
        isAdmin,
        login,
        register,
        logout,
        switchUser,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
