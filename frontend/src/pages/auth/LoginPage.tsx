import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Utensils, UserCheck, Shield } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      await login(email, password);
      navigate('/menu');
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Invalid email or password.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickLogin = async (demoEmail: string, demoPass: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await login(demoEmail, demoPass);
      navigate('/menu');
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Login failed.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-8 sm:py-12">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-xl border border-slate-200">
        <div className="text-center mb-6">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-orange-500 to-amber-400 flex items-center justify-center text-white mx-auto mb-3 shadow-md">
            <Utensils className="w-6 h-6" />
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-slate-900">Sign in to CraveAI</h2>
          <p className="text-xs text-slate-500 mt-1">Access natural AI food ordering and real-time order tracking.</p>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-2xl p-3.5 sm:p-4 mb-6">
          <span className="text-[11px] font-bold text-orange-900 uppercase tracking-wider block mb-2 text-center sm:text-left">
            ⚡ Quick 1-Click Demo Login
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickLogin('customer@example.com', 'CustomerPass123!')}
              className="bg-white hover:bg-orange-100 text-slate-800 text-xs font-bold py-2.5 px-3 rounded-xl border border-orange-200 shadow-xs flex items-center justify-center gap-1.5 cursor-pointer transition"
            >
              <UserCheck className="w-3.5 h-3.5 text-orange-600 shrink-0" />
              <span>Customer (Rahul)</span>
            </button>
            <button
              type="button"
              onClick={() => handleQuickLogin('admin@kpitech.com', 'AdminPass123!')}
              className="bg-white hover:bg-orange-100 text-slate-800 text-xs font-bold py-2.5 px-3 rounded-xl border border-orange-200 shadow-xs flex items-center justify-center gap-1.5 cursor-pointer transition"
            >
              <Shield className="w-3.5 h-3.5 text-orange-600 shrink-0" />
              <span>Admin (Manager)</span>
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 text-xs font-semibold p-3 rounded-xl mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl shadow-md transition cursor-pointer text-xs sm:text-sm"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="text-center text-xs text-slate-500 mt-6">
          Don't have an account?{' '}
          <Link to="/register" className="font-bold text-orange-600 hover:underline">
            Create account
          </Link>
        </p>
      </div>
    </div>
  );
};
