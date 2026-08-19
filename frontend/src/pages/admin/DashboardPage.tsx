import React, { useState, useEffect } from 'react';
import { orderApi } from '../../api/orderApi';
import { DashboardData } from '../../types';
import { MetricsGrid } from '../../components/admin/MetricsGrid';
import { LayoutDashboard, TrendingUp, Award, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await orderApi.getDashboardMetrics();
        if (res.success) setData(res.data);
      } catch (err) {
        console.error('Failed to load dashboard metrics', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (isLoading || !data) {
    return <div className="max-w-7xl mx-auto px-4 py-16 text-center text-slate-500">Loading restaurant analytics...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 flex items-center gap-2">
            <LayoutDashboard className="w-6 h-6 sm:w-7 sm:h-7 text-orange-600 shrink-0" />
            <span>Restaurant Admin Dashboard</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Aggregated business KPIs, live orders, and top selling dishes.
          </p>
        </div>

        <Link
          to="/admin/orders"
          className="inline-flex items-center justify-center gap-1.5 bg-orange-600 hover:bg-orange-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl shadow-xs transition w-full sm:w-auto"
        >
          <span>Manage Live Orders</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      <MetricsGrid summary={data.summary} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
        <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-xs">
          <h3 className="font-extrabold text-sm sm:text-base text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
            <Award className="w-4 h-4 sm:w-5 sm:h-5 text-amber-500 shrink-0" />
            <span>Top Selling Menu Items</span>
          </h3>

          <div className="space-y-3">
            {data.top_selling_items.map((item, idx) => (
              <div key={item.menu_item_id} className="flex items-center justify-between p-3 rounded-xl bg-slate-50 gap-2">
                <div className="flex items-center gap-2.5 sm:gap-3 min-w-0">
                  <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-800 font-black text-xs flex items-center justify-center shrink-0">
                    #{idx + 1}
                  </span>
                  <div className="truncate">
                    <h4 className="font-extrabold text-slate-900 text-xs sm:text-sm truncate">{item.name}</h4>
                    <span className="text-[10px] sm:text-[11px] text-slate-500 block truncate">{item.category_name}</span>
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <span className="font-black text-xs sm:text-sm text-slate-900 block">{item.units_sold} sold</span>
                  <span className="text-[10px] sm:text-[11px] font-semibold text-emerald-600">₹{item.revenue_generated}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-xs">
          <h3 className="font-extrabold text-sm sm:text-base text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 sm:w-5 sm:h-5 text-blue-500 shrink-0" />
            <span>Orders by Status</span>
          </h3>

          <div className="space-y-2.5 sm:space-y-3">
            {data.orders_by_status.map((st) => (
              <div key={st.status} className="flex items-center justify-between p-3 rounded-xl border border-slate-100">
                <span className="font-bold text-xs uppercase tracking-wider text-slate-700">
                  {st.status.replace('_', ' ')}
                </span>
                <span className="font-black text-xs sm:text-sm bg-slate-100 text-slate-800 px-3 py-1 rounded-full">
                  {st.count} orders
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
