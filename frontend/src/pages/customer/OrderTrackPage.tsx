import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { orderApi } from '../../api/orderApi';
import { Order } from '../../types';
import { OrderTimeline } from '../../components/customer/OrderTimeline';
import { ArrowLeft, ShoppingBag } from 'lucide-react';

export const OrderTrackPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [order, setOrder] = useState<Order | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    const fetchOrder = async () => {
      try {
        const res = await orderApi.getOrderById(id);
        if (res.success) setOrder(res.data);
      } catch (err) {
        console.error('Failed to load order detail', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchOrder();

    const interval = setInterval(fetchOrder, 4000);
    return () => clearInterval(interval);
  }, [id]);

  if (isLoading) {
    return <div className="max-w-3xl mx-auto px-4 py-16 text-center text-slate-500">Loading live order tracking...</div>;
  }

  if (!order) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <h2 className="text-xl font-bold text-slate-800">Order Not Found</h2>
        <Link to="/orders" className="text-orange-600 text-sm font-bold mt-2 inline-block">
          Back to Orders
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
      <Link
        to="/orders"
        className="inline-flex items-center gap-1 text-xs font-bold text-slate-500 hover:text-slate-800 mb-6 transition"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Orders
      </Link>

      <div className="flex justify-between items-start mb-6">
        <div>
          <span className="text-xs font-bold text-orange-600 uppercase tracking-wider block">Live Order Tracker</span>
          <h1 className="text-2xl font-black text-slate-900 mt-0.5">Order #{order.id.slice(0, 8)}</h1>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400 block">Total Amount</span>
          <span className="text-xl font-black text-slate-900">₹{order.total_amount}</span>
        </div>
      </div>

      <OrderTimeline status={order.status} />

      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs mt-6">
        <h3 className="font-extrabold text-base text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
          <ShoppingBag className="w-4 h-4 text-orange-600" />
          Dishes in this Order
        </h3>

        <div className="divide-y divide-slate-100">
          {order.items.map((it) => (
            <div key={it.id} className="py-3 flex justify-between items-center text-sm">
              <div className="flex items-center gap-2">
                <span
                  className={`w-3.5 h-3.5 rounded-xs flex items-center justify-center border text-[8px] font-bold ${
                    it.is_vegetarian
                      ? 'border-emerald-600 text-emerald-600'
                      : 'border-rose-600 text-rose-600'
                  }`}
                >
                  ●
                </span>
                <span className="font-bold text-slate-800">{it.quantity}x {it.menu_item_name}</span>
              </div>
              <span className="font-black text-slate-900">₹{it.subtotal}</span>
            </div>
          ))}
        </div>

        {order.delivery_notes && (
          <div className="mt-4 pt-4 border-t border-slate-100 bg-slate-50 p-3 rounded-xl text-xs text-slate-600">
            <span className="font-bold text-slate-700 block mb-0.5">Delivery Notes:</span>
            "{order.delivery_notes}"
          </div>
        )}
      </div>
    </div>
  );
};
