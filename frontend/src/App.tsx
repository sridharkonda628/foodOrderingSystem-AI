import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import { Navbar } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { MenuPage } from './pages/customer/MenuPage';
import { CartPage } from './pages/customer/CartPage';
import { OrdersPage } from './pages/customer/OrdersPage';
import { OrderTrackPage } from './pages/customer/OrderTrackPage';
import { DashboardPage } from './pages/admin/DashboardPage';
import { AdminOrdersPage } from './pages/admin/AdminOrdersPage';
import { AdminMenuPage } from './pages/admin/AdminMenuPage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';

const queryClient = new QueryClient();

const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isAdmin, isLoading } = useAuth();
  if (isLoading) return null;
  if (!user || !isAdmin) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <CartProvider>
          <BrowserRouter>
            <div className="min-h-screen flex flex-col bg-slate-50">
              <Navbar />
              <main className="flex-1">
                <Routes>
                  <Route path="/" element={<Navigate to="/menu" replace />} />
                  <Route path="/menu" element={<MenuPage />} />
                  <Route path="/cart" element={<CartPage />} />
                  <Route path="/orders" element={<OrdersPage />} />
                  <Route path="/orders/:id" element={<OrderTrackPage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />

                  <Route
                    path="/admin/dashboard"
                    element={
                      <AdminRoute>
                        <DashboardPage />
                      </AdminRoute>
                    }
                  />
                  <Route
                    path="/admin/orders"
                    element={
                      <AdminRoute>
                        <AdminOrdersPage />
                      </AdminRoute>
                    }
                  />
                  <Route
                    path="/admin/menu"
                    element={
                      <AdminRoute>
                        <AdminMenuPage />
                      </AdminRoute>
                    }
                  />
                </Routes>
              </main>
              <Footer />
            </div>
          </BrowserRouter>
        </CartProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
