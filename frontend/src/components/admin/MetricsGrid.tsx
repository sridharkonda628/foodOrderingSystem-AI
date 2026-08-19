import React from 'react';
import { MetricSummary } from '../../types';
import { DollarSign, ShoppingCart, TrendingUp, ChefHat } from 'lucide-react';

interface MetricsGridProps {
  summary: MetricSummary;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ summary }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-6 sm:mb-8">
      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider block">Today's Revenue</span>
          <span className="text-xl sm:text-2xl font-black text-slate-900 mt-0.5 sm:mt-1 block">₹{summary.total_revenue_today.toLocaleString()}</span>
        </div>
        <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
          <DollarSign className="w-5 h-5 sm:w-6 sm:h-6" />
        </div>
      </div>

      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider block">Orders Today</span>
          <span className="text-xl sm:text-2xl font-black text-slate-900 mt-0.5 sm:mt-1 block">{summary.total_orders_today}</span>
        </div>
        <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
          <ShoppingCart className="w-5 h-5 sm:w-6 sm:h-6" />
        </div>
      </div>

      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider block">Avg Order Value</span>
          <span className="text-xl sm:text-2xl font-black text-slate-900 mt-0.5 sm:mt-1 block">₹{summary.average_order_value_today}</span>
        </div>
        <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center shrink-0">
          <TrendingUp className="w-5 h-5 sm:w-6 sm:h-6" />
        </div>
      </div>

      <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs flex items-center justify-between">
        <div>
          <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wider block">Active in Kitchen</span>
          <span className="text-xl sm:text-2xl font-black text-orange-600 mt-0.5 sm:mt-1 block">{summary.active_orders_count}</span>
        </div>
        <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center shrink-0">
          <ChefHat className="w-5 h-5 sm:w-6 sm:h-6" />
        </div>
      </div>
    </div>
  );
};
