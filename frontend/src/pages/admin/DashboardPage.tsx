import React, { useState, useEffect } from 'react';
import { orderApi } from '../../api/orderApi';
import { DashboardData } from '../../types';
import { MetricsGrid } from '../../components/admin/MetricsGrid';
import { LayoutDashboard, TrendingUp, Award } from 'lucide-react';
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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 flex items-center gap-2">
            <LayoutDashboard className="w-7 h-7 text-orange-600" />
            Restaurant Admin Dashboard
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Aggregated business KPIs, live orders, and top selling dishes.
          </p>
        </div>

        <Link
          to="/admin/orders"
          className="bg-orange-600 hover:bg-orange-700 text-white text-xs font-bold px-4 py-2.5 rounded-xl shadow-xs transition"
        >
          Manage Live Orders →
        </Link>
      </div>

      <MetricsGrid summary={data.summary} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="font-extrabold text-base text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-500" />
            Top Selling Menu Items
          </h3>

          <div className="space-y-3">
            {data.top_selling_items.map((item, idx) => (
              <div key={item.menu_item_id} className="flex items-center justify-between p-3 rounded-xl bg-slate-50">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-800 font-black text-xs flex items-center justify-center">
                    #{idx + 1}
                  </span>
                  <div>
                    <h4 className="font-extrabold text-slate-900 text-sm">{item.name}</h4>
                    <span className="text-[11px] text-slate-500">{item.category_name}</span>
                  </div>
                </div>
                <div className="text-right">
                  <span className="font-black text-sm text-slate-900 block">{item.units_sold} sold</span>
                  <span className="text-[11px] font-semibold text-emerald-600">₹{item.revenue_generated}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <h3 className="font-extrabold text-base text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-500" />
            Orders by Status
          </h3>

          <div className="space-y-3">
            {data.orders_by_status.map((st) => (
              <div key={st.status} className="flex items-center justify-between p-3 rounded-xl border border-slate-100">
                <span className="font-bold text-xs uppercase tracking-wider text-slate-700">
                  {st.status.replace('_', ' ')}
                </span>
                <span className="font-black text-sm bg-slate-100 text-slate-800 px-3 py-1 rounded-full">
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
