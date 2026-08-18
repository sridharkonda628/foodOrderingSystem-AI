import React from 'react';
import { MetricSummary } from '../../types';
import { DollarSign, ShoppingCart, TrendingUp, ChefHat } from 'lucide-react';

interface MetricsGridProps {
  summary: MetricSummary;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ summary }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Today's Revenue</span>
          <span className="text-2xl font-black text-slate-900 mt-1 block">₹{summary.total_revenue_today.toLocaleString()}</span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
          <DollarSign className="w-6 h-6" />
        </div>
      </div>

      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Orders Today</span>
          <span className="text-2xl font-black text-slate-900 mt-1 block">{summary.total_orders_today}</span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
          <ShoppingCart className="w-6 h-6" />
        </div>
      </div>

      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Avg Order Value</span>
          <span className="text-2xl font-black text-slate-900 mt-1 block">₹{summary.average_order_value_today}</span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center">
          <TrendingUp className="w-6 h-6" />
        </div>
      </div>

      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Active in Kitchen</span>
          <span className="text-2xl font-black text-orange-600 mt-1 block">{summary.active_orders_count}</span>
        </div>
        <div className="w-12 h-12 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center">
          <ChefHat className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
};
