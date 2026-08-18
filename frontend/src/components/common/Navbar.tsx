import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, ShoppingBag, Utensils, LayoutDashboard, ClipboardList, LogOut, User as UserIcon, Shield, Coffee } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, isAdmin, logout, switchUser } = useAuth();
  const { totalItems } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-slate-200 shadow-sm">
      {/* Demo Switcher Ribbon */}
      <div className="bg-gradient-to-r from-orange-600 to-amber-600 text-white text-xs py-1 px-4 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="font-medium bg-white/20 px-2 py-0.5 rounded text-[11px] uppercase tracking-wider">Demo Switcher</span>
          <span>Switch active role instantly:</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => switchUser('customer')}
            className={`px-2.5 py-0.5 rounded transition ${
              user?.role === 'customer'
                ? 'bg-white text-orange-700 font-bold shadow-xs'
                : 'hover:bg-white/20'
            }`}
          >
            👤 Customer (Rahul)
          </button>
          <button
            onClick={() => switchUser('admin')}
            className={`px-2.5 py-0.5 rounded transition ${
              user?.role === 'admin'
                ? 'bg-white text-orange-700 font-bold shadow-xs'
                : 'hover:bg-white/20'
            }`}
          >
            🛡️ Admin (Manager)
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-orange-500 to-amber-400 flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
              <Utensils className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xl font-black bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">
                CraveAI
              </span>
              <span className="text-[10px] block font-semibold text-slate-400 -mt-1 tracking-wider uppercase">
                Smart Food Ordering
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/menu"
              className="text-sm font-semibold text-slate-700 hover:text-orange-600 transition flex items-center gap-1.5"
            >
              <Coffee className="w-4 h-4 text-orange-500" />
              Menu & AI Search
            </Link>

            {isAuthenticated && !isAdmin && (
              <Link
                to="/orders"
                className="text-sm font-semibold text-slate-700 hover:text-orange-600 transition flex items-center gap-1.5"
              >
                <ClipboardList className="w-4 h-4 text-orange-500" />
                My Orders
              </Link>
            )}

            {isAdmin && (
              <>
                <Link
                  to="/admin/dashboard"
                  className="text-sm font-semibold text-slate-700 hover:text-orange-600 transition flex items-center gap-1.5"
                >
                  <LayoutDashboard className="w-4 h-4 text-orange-500" />
                  Dashboard
                </Link>
                <Link
                  to="/admin/orders"
                  className="text-sm font-semibold text-slate-700 hover:text-orange-600 transition flex items-center gap-1.5"
                >
                  <ClipboardList className="w-4 h-4 text-orange-500" />
                  Live Orders
                </Link>
                <Link
                  to="/admin/menu"
                  className="text-sm font-semibold text-slate-700 hover:text-orange-600 transition flex items-center gap-1.5"
                >
                  <Shield className="w-4 h-4 text-orange-500" />
                  Manage Menu
                </Link>
              </>
            )}
          </nav>

          {/* Right Action Icons & User */}
          <div className="flex items-center gap-3">
            {/* Cart Button */}
            {!isAdmin && (
              <Link
                to="/cart"
                className="relative p-2.5 text-slate-700 hover:text-orange-600 rounded-full hover:bg-orange-50 transition"
                title="View Cart"
              >
                <ShoppingBag className="w-6 h-6" />
                {totalItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-orange-600 text-white font-bold text-xs w-5 h-5 rounded-full flex items-center justify-center shadow-sm animate-pulse">
                    {totalItems}
                  </span>
                )}
              </Link>
            )}

            {/* Auth Button */}
            {isAuthenticated ? (
              <div className="flex items-center gap-3 pl-2 border-l border-slate-200">
                <div className="text-right hidden sm:block">
                  <div className="text-xs font-bold text-slate-800">{user?.full_name}</div>
                  <div className="text-[10px] font-semibold text-slate-500 uppercase">{user?.role}</div>
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-500 hover:text-red-600 rounded-lg hover:bg-red-50 transition"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="bg-orange-600 hover:bg-orange-700 text-white text-sm font-bold px-4 py-2 rounded-xl shadow-sm transition hover:shadow"
              >
                Sign In
              </Link>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};
