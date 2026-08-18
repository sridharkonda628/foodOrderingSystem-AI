import React, { useState, useEffect } from 'react';
import { orderApi } from '../../api/orderApi';
import { Order, OrderStatus } from '../../types';
import { ClipboardList } from 'lucide-react';

const STATUS_OPTIONS: OrderStatus[] = ['placed', 'confirmed', 'preparing', 'ready', 'picked_up', 'cancelled'];

export const AdminOrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [isLoading, setIsLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const res = await orderApi.getAllOrders(filterStatus === 'all' ? undefined : filterStatus);
      if (res.success) setOrders(res.data);
    } catch (err) {
      console.error('Failed to load orders', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, [filterStatus]);

  const handleUpdateStatus = async (orderId: string, newStatus: OrderStatus) => {
    try {
      await orderApi.updateOrderStatus(orderId, newStatus);
      fetchOrders();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Invalid status transition!');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 flex items-center gap-2">
            <ClipboardList className="w-7 h-7 text-orange-600" />
            Live Kitchen & Order Management
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Advance orders through strict state machine: Placed → Confirmed → Preparing → Ready → Picked Up.
          </p>
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto">
          <button
            onClick={() => setFilterStatus('all')}
            className={`px-3 py-1.5 rounded-xl text-xs font-bold cursor-pointer ${
              filterStatus === 'all' ? 'bg-orange-600 text-white' : 'bg-white border border-slate-200 text-slate-700'
            }`}
          >
            All
          </button>
          {STATUS_OPTIONS.map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold uppercase cursor-pointer ${
                filterStatus === st ? 'bg-orange-600 text-white' : 'bg-white border border-slate-200 text-slate-700'
              }`}
            >
              {st.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((n) => (
            <div key={n} className="bg-white rounded-2xl p-5 border border-slate-200 animate-pulse h-28" />
          ))}
        </div>
      ) : orders.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 p-8">
          <p className="text-slate-500 text-sm font-semibold">No orders in this status category.</p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="divide-y divide-slate-200">
            {orders.map((order) => {
              const formattedDate = new Date(order.created_at).toLocaleTimeString('en-IN', {
                hour: '2-digit',
                minute: '2-digit',
              });

              return (
                <div key={order.id} className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50 transition">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-bold text-xs text-orange-600">#{order.id.slice(0, 8)}</span>
                      <span className="text-xs text-slate-400">•</span>
                      <span className="font-extrabold text-sm text-slate-900">{order.customer_name || 'Customer'}</span>
                      <span className="text-xs text-slate-400">•</span>
                      <span className="text-xs text-slate-500">{formattedDate}</span>
                    </div>

                    <div className="text-xs font-semibold text-slate-700">
                      {order.items.map((i) => `${i.quantity}x ${i.menu_item_name}`).join(', ')}
                    </div>

                    {order.delivery_notes && (
                      <div className="text-[11px] text-slate-500 mt-1 italic">
                        Note: "{order.delivery_notes}"
                      </div>
                    )}
                  </div>

                  <div className="flex items-center gap-4 self-end md:self-center">
                    <div className="text-right">
                      <span className="text-xs text-slate-400 block">Total</span>
                      <span className="text-base font-black text-slate-900">₹{order.total_amount}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <select
                        value={order.status}
                        onChange={(e) => handleUpdateStatus(order.id, e.target.value as OrderStatus)}
                        className="bg-white border border-slate-300 text-slate-800 font-bold text-xs rounded-xl px-3 py-2 focus:ring-2 focus:ring-orange-500 cursor-pointer uppercase"
                      >
                        {STATUS_OPTIONS.map((st) => (
                          <option key={st} value={st}>
                            {st.replace('_', ' ')}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
