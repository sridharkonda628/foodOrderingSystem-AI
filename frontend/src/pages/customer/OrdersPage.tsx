import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { orderApi } from '../../api/orderApi';
import { Order } from '../../types';
import { ClipboardList, ArrowRight } from 'lucide-react';

const STATUS_COLORS: Record<string, string> = {
  placed: 'bg-blue-50 text-blue-700 border-blue-200',
  confirmed: 'bg-purple-50 text-purple-700 border-purple-200',
  preparing: 'bg-amber-50 text-amber-700 border-amber-200',
  ready: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  picked_up: 'bg-slate-100 text-slate-700 border-slate-300',
  cancelled: 'bg-red-50 text-red-700 border-red-200',
};

export const OrdersPage: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchOrders = async () => {
    try {
      const res = await orderApi.getMyOrders();
      if (res.success) setOrders(res.data);
    } catch (err) {
      console.error('Failed to load orders', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleCancelOrder = async (orderId: string) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;
    try {
      await orderApi.cancelOrder(orderId);
      fetchOrders();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to cancel order.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <h1 className="text-2xl sm:text-3xl font-black text-slate-900 mb-6 flex items-center gap-2.5">
        <ClipboardList className="w-7 h-7 text-orange-600" />
        My Orders History
      </h1>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((n) => (
            <div key={n} className="bg-white rounded-2xl p-5 border border-slate-200 animate-pulse h-32" />
          ))}
        </div>
      ) : orders.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 p-8">
          <ClipboardList className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="font-extrabold text-slate-800 text-base">No orders placed yet</h3>
          <p className="text-xs text-slate-500 mt-1 mb-4">Discover our tasty dishes and place your first order!</p>
          <Link
            to="/menu"
            className="inline-flex items-center gap-2 bg-orange-600 text-white font-bold text-xs px-4 py-2.5 rounded-xl shadow-xs hover:bg-orange-700"
          >
            Browse Menu
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {orders.map((order) => {
            const formattedDate = new Date(order.created_at).toLocaleString('en-IN', {
              dateStyle: 'medium',
              timeStyle: 'short',
            });
            const statusClass = STATUS_COLORS[order.status] || 'bg-slate-100 text-slate-700';

            return (
              <div
                key={order.id}
                className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-orange-300 transition"
              >
                <div>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-black uppercase tracking-wider border ${statusClass}`}>
                      {order.status.replace('_', ' ')}
                    </span>
                    <span className="text-xs text-slate-400 font-medium">#{order.id.slice(0, 8)}</span>
                    <span className="text-xs text-slate-400">•</span>
                    <span className="text-xs text-slate-500">{formattedDate}</span>
                  </div>

                  <div className="text-sm font-semibold text-slate-800">
                    {order.items.map((i) => `${i.quantity}x ${i.menu_item_name}`).join(', ')}
                  </div>
                  <div className="text-xs font-black text-slate-900 mt-1">Total: ₹{order.total_amount}</div>
                </div>

                <div className="flex items-center gap-3 self-end sm:self-center">
                  {order.status === 'placed' && (
                    <button
                      onClick={() => handleCancelOrder(order.id)}
                      className="text-xs font-bold text-red-600 hover:bg-red-50 px-3 py-1.5 rounded-xl border border-red-200 transition cursor-pointer"
                    >
                      Cancel
                    </button>
                  )}
                  <Link
                    to={`/orders/${order.id}`}
                    className="flex items-center gap-1 bg-slate-900 hover:bg-orange-600 text-white text-xs font-bold px-3.5 py-2 rounded-xl shadow-xs transition"
                  >
                    <span>Track Order</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
