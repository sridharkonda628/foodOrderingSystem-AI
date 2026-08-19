import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, UserRole } from '../types';
import { authApi } from '../api/authApi';

interface AuthContextType {
  user: User | null;
  role: UserRole | null;
  isAuthenticated: boolean;
  isAdmin: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string, role?: string) => Promise<void>;
  logout: () => Promise<void>;
  switchUser: (role: UserRole) => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Validate active session on initial load using the secure HttpOnly cookie
  useEffect(() => {
    const initAuth = async () => {
      // Clear any legacy insecure localStorage entries
      localStorage.removeItem('kpitech_token');
      localStorage.removeItem('kpitech_user');

      try {
        const res = await authApi.getMe();
        if (res.success && res.data) {
          setUser(res.data);
        }
      } catch {
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await authApi.login(email, password);
    if (res.success && res.data) {
      setUser(res.data.user);
    }
  };

  const register = async (email: string, password: string, fullName: string, role: string = 'customer') => {
    const res = await authApi.register(email, password, fullName, role);
    if (res.success && res.data) {
      setUser(res.data.user);
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } catch {
      // Ignore network errors on logout
    } finally {
      setUser(null);
    }
  };

  const switchUser = async (targetRole: UserRole) => {
    if (targetRole === 'admin') {
      await login('admin@kpitech.com', 'AdminPass123!');
    } else {
      await login('customer@example.com', 'CustomerPass123!');
    }
  };

  const role = user ? (user.role as UserRole) : null;
  const isAuthenticated = !!user;
  const isAdmin = role === 'admin';

  return (
    <AuthContext.Provider
      value={{
        user,
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
