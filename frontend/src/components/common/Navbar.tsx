import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  ShoppingBag,
  Utensils,
  LayoutDashboard,
  ClipboardList,
  LogOut,
  Shield,
  Coffee,
  Menu as MenuIcon,
  X,
  User as UserIcon
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, isAdmin, logout, switchUser } = useAuth();
  const { totalItems } = useCart();
  const navigate = useNavigate();
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    setIsMobileMenuOpen(false);
    navigate('/login');
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-xs">
      {/* Demo Switcher Ribbon */}
      <div className="bg-gradient-to-r from-orange-600 to-amber-600 text-white text-xs py-1.5 px-3 sm:px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-1.5 sm:gap-2">
          <div className="flex items-center gap-1.5 text-center sm:text-left">
            <span className="font-bold bg-white/20 px-2 py-0.5 rounded-full text-[10px] sm:text-[11px] uppercase tracking-wider">
              Demo Switcher
            </span>
            <span className="text-[11px] sm:text-xs text-orange-100 hidden xs:inline">
              Switch active role:
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <button
              onClick={() => switchUser('customer')}
              className={`px-2.5 py-0.5 rounded-lg transition text-xs font-semibold cursor-pointer ${
                user?.role === 'customer'
                  ? 'bg-white text-orange-700 font-bold shadow-xs'
                  : 'hover:bg-white/20 text-white'
              }`}
            >
              👤 Customer (Rahul)
            </button>
            <button
              onClick={() => switchUser('admin')}
              className={`px-2.5 py-0.5 rounded-lg transition text-xs font-semibold cursor-pointer ${
                user?.role === 'admin'
                  ? 'bg-white text-orange-700 font-bold shadow-xs'
                  : 'hover:bg-white/20 text-white'
              }`}
            >
              🛡️ Admin (Manager)
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" onClick={closeMobileMenu} className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr from-orange-500 to-amber-400 flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
              <Utensils className="w-5 h-5" />
            </div>
            <div>
              <span className="text-lg sm:text-xl font-black bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent block leading-tight">
                CraveAI
              </span>
              <span className="text-[9px] sm:text-[10px] block font-semibold text-slate-400 -mt-0.5 tracking-wider uppercase">
                Smart Food Ordering
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-6">
            <Link
              to="/menu"
              className={`text-sm font-semibold transition flex items-center gap-1.5 ${
                location.pathname === '/menu'
                  ? 'text-orange-600 font-bold'
                  : 'text-slate-700 hover:text-orange-600'
              }`}
            >
              <Coffee className="w-4 h-4 text-orange-500" />
              Menu & AI Search
            </Link>

            {isAuthenticated && !isAdmin && (
              <Link
                to="/orders"
                className={`text-sm font-semibold transition flex items-center gap-1.5 ${
                  location.pathname === '/orders'
                    ? 'text-orange-600 font-bold'
                    : 'text-slate-700 hover:text-orange-600'
                }`}
              >
                <ClipboardList className="w-4 h-4 text-orange-500" />
                My Orders
              </Link>
            )}

            {isAdmin && (
              <>
                <Link
                  to="/admin/dashboard"
                  className={`text-sm font-semibold transition flex items-center gap-1.5 ${
                    location.pathname === '/admin/dashboard'
                      ? 'text-orange-600 font-bold'
                      : 'text-slate-700 hover:text-orange-600'
                  }`}
                >
                  <LayoutDashboard className="w-4 h-4 text-orange-500" />
                  Dashboard
                </Link>
                <Link
                  to="/admin/orders"
                  className={`text-sm font-semibold transition flex items-center gap-1.5 ${
                    location.pathname === '/admin/orders'
                      ? 'text-orange-600 font-bold'
                      : 'text-slate-700 hover:text-orange-600'
                  }`}
                >
                  <ClipboardList className="w-4 h-4 text-orange-500" />
                  Live Orders
                </Link>
                <Link
                  to="/admin/menu"
                  className={`text-sm font-semibold transition flex items-center gap-1.5 ${
                    location.pathname === '/admin/menu'
                      ? 'text-orange-600 font-bold'
                      : 'text-slate-700 hover:text-orange-600'
                  }`}
                >
                  <Shield className="w-4 h-4 text-orange-500" />
                  Manage Menu
                </Link>
              </>
            )}
          </nav>

          {/* Right Actions (Cart, User, Mobile Toggle) */}
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Cart Button (for customers) */}
            {!isAdmin && (
              <Link
                to="/cart"
                onClick={closeMobileMenu}
                className="relative p-2 sm:p-2.5 text-slate-700 hover:text-orange-600 rounded-full hover:bg-orange-50 transition cursor-pointer"
                title="View Cart"
                aria-label="View Cart"
              >
                <ShoppingBag className="w-5 h-5 sm:w-6 sm:h-6" />
                {totalItems > 0 && (
                  <span className="absolute -top-1 -right-1 bg-orange-600 text-white font-bold text-[10px] sm:text-xs w-4 h-4 sm:w-5 sm:h-5 rounded-full flex items-center justify-center shadow-xs animate-pulse">
                    {totalItems}
                  </span>
                )}
              </Link>
            )}

            {/* Desktop Auth Section */}
            {isAuthenticated ? (
              <div className="hidden sm:flex items-center gap-3 pl-2 border-l border-slate-200">
                <div className="text-right">
                  <div className="text-xs font-bold text-slate-800">{user?.full_name}</div>
                  <div className="text-[10px] font-semibold text-slate-500 uppercase">{user?.role}</div>
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 text-slate-500 hover:text-red-600 rounded-lg hover:bg-red-50 transition cursor-pointer"
                  title="Logout"
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="hidden sm:inline-flex bg-orange-600 hover:bg-orange-700 text-white text-xs sm:text-sm font-bold px-4 py-2 rounded-xl shadow-xs transition hover:shadow cursor-pointer"
              >
                Sign In
              </Link>
            )}

            {/* Mobile Hamburger Menu Toggle Button */}
            <button
              type="button"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-2 rounded-xl text-slate-700 hover:text-orange-600 hover:bg-slate-100 transition cursor-pointer focus:outline-hidden"
              aria-label="Toggle mobile menu"
            >
              {isMobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <MenuIcon className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Collapsible Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-6 space-y-3 shadow-xl animate-in fade-in slide-in-from-top-2 duration-200">
          {/* User profile banner on mobile */}
          {isAuthenticated ? (
            <div className="flex items-center justify-between p-3 rounded-2xl bg-orange-50/70 border border-orange-100 mb-2">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-full bg-orange-200 text-orange-800 flex items-center justify-center font-bold text-sm">
                  {user?.full_name.charAt(0)}
                </div>
                <div>
                  <div className="text-sm font-extrabold text-slate-900">{user?.full_name}</div>
                  <div className="text-[10px] font-bold text-orange-700 uppercase tracking-wider">
                    Role: {user?.role}
                  </div>
                </div>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center gap-1 text-xs font-bold text-red-600 bg-white hover:bg-red-50 px-2.5 py-1.5 rounded-xl border border-red-200 transition"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div className="pb-2">
              <Link
                to="/login"
                onClick={closeMobileMenu}
                className="w-full flex items-center justify-center gap-2 bg-orange-600 hover:bg-orange-700 text-white font-bold py-2.5 rounded-xl shadow-xs text-sm"
              >
                <UserIcon className="w-4 h-4" />
                <span>Sign In / Create Account</span>
              </Link>
            </div>
          )}

          {/* Navigation Links */}
          <nav className="flex flex-col space-y-1">
            <Link
              to="/menu"
              onClick={closeMobileMenu}
              className={`flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-sm font-bold transition ${
                location.pathname === '/menu'
                  ? 'bg-orange-50 text-orange-700 font-extrabold'
                  : 'text-slate-700 hover:bg-slate-50'
              }`}
            >
              <Coffee className="w-4 h-4 text-orange-500" />
              <span>Menu & AI Search</span>
            </Link>

            {isAuthenticated && !isAdmin && (
              <Link
                to="/orders"
                onClick={closeMobileMenu}
                className={`flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-sm font-bold transition ${
                  location.pathname === '/orders'
                    ? 'bg-orange-50 text-orange-700 font-extrabold'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <ClipboardList className="w-4 h-4 text-orange-500" />
                <span>My Orders</span>
              </Link>
            )}

            {!isAdmin && (
              <Link
                to="/cart"
                onClick={closeMobileMenu}
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-bold transition ${
                  location.pathname === '/cart'
                    ? 'bg-orange-50 text-orange-700 font-extrabold'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <ShoppingBag className="w-4 h-4 text-orange-500" />
                  <span>My Cart</span>
                </div>
                {totalItems > 0 && (
                  <span className="bg-orange-600 text-white text-xs font-black px-2 py-0.5 rounded-full">
                    {totalItems} items
                  </span>
                )}
              </Link>
            )}

            {isAdmin && (
              <>
                <div className="pt-2 pb-1 px-3 text-[10px] font-extrabold text-slate-400 uppercase tracking-wider">
                  Admin Controls
                </div>
                <Link
                  to="/admin/dashboard"
                  onClick={closeMobileMenu}
                  className={`flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-sm font-bold transition ${
                    location.pathname === '/admin/dashboard'
                      ? 'bg-orange-50 text-orange-700 font-extrabold'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <LayoutDashboard className="w-4 h-4 text-orange-500" />
                  <span>Admin Dashboard</span>
                </Link>
                <Link
                  to="/admin/orders"
                  onClick={closeMobileMenu}
                  className={`flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-sm font-bold transition ${
                    location.pathname === '/admin/orders'
                      ? 'bg-orange-50 text-orange-700 font-extrabold'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <ClipboardList className="w-4 h-4 text-orange-500" />
                  <span>Live Kitchen Orders</span>
                </Link>
                <Link
                  to="/admin/menu"
                  onClick={closeMobileMenu}
                  className={`flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl text-sm font-bold transition ${
                    location.pathname === '/admin/menu'
                      ? 'bg-orange-50 text-orange-700 font-extrabold'
                      : 'text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  <Shield className="w-4 h-4 text-orange-500" />
                  <span>Manage Menu Catalog</span>
                </Link>
              </>
            )}
          </nav>
        </div>
      )}
    </header>
  );
};
