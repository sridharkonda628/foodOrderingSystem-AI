import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import { orderApi } from '../../api/orderApi';
import { ShoppingBag, ArrowRight, Trash2, AlertCircle } from 'lucide-react';

export const CartPage: React.FC = () => {
  const { items, updateQuantity, removeItem, clearCart, totalAmount, totalItems } = useCart();
  const { isAuthenticated } = useAuth();
  const [deliveryNotes, setDeliveryNotes] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleCheckout = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (items.length === 0) return;

    setIsLoading(true);
    setErrorMessage(null);

    try {
      const payload = items.map((ci) => ({
        menu_item_id: ci.item.id,
        quantity: ci.quantity,
      }));

      const res = await orderApi.createOrder(payload, deliveryNotes);
      if (res.success && res.data) {
        clearCart();
        navigate(`/orders/${res.data.id}`);
      }
    } catch (err: any) {
      const errData = err.response?.data?.error;
      setErrorMessage(
        errData?.message || 'Failed to place order. One or more items might be unavailable.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-12 sm:py-16 text-center">
        <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-3xl bg-orange-50 text-orange-600 flex items-center justify-center mx-auto mb-4">
          <ShoppingBag className="w-8 h-8 sm:w-10 sm:h-10" />
        </div>
        <h2 className="text-xl sm:text-2xl font-black text-slate-900 mb-2">Your Cart is Empty</h2>
        <p className="text-slate-500 text-xs sm:text-sm mb-6 max-w-sm mx-auto">
          Explore our menu or use natural language AI search to find dishes tailored to your cravings!
        </p>
        <Link
          to="/menu"
          className="inline-flex items-center gap-2 bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs sm:text-sm px-5 sm:px-6 py-2.5 sm:py-3 rounded-2xl shadow-sm transition"
        >
          <span>Explore Menu</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
      <h1 className="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 mb-6 flex items-center gap-2.5">
        <ShoppingBag className="w-6 h-6 sm:w-7 sm:h-7 text-orange-600" />
        <span>Checkout Review ({totalItems} {totalItems === 1 ? 'item' : 'items'})</span>
      </h1>

      {errorMessage && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-2xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold block text-sm">Order Verification Failed</span>
            <span className="text-xs">{errorMessage}</span>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
        <div className="lg:col-span-2 space-y-4">
          {items.map((ci) => (
            <div
              key={ci.item.id}
              className="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span
                    className={`w-3.5 h-3.5 rounded-xs flex items-center justify-center border text-[8px] font-bold shrink-0 ${
                      ci.item.is_vegetarian
                        ? 'border-emerald-600 text-emerald-600'
                        : 'border-rose-600 text-rose-600'
                    }`}
                  >
                    ●
                  </span>
                  <h4 className="font-extrabold text-slate-900 text-sm sm:text-base leading-snug">{ci.item.name}</h4>
                </div>
                <div className="text-xs text-slate-500 mt-1">
                  ₹{ci.item.price} each • Subtotal: <span className="font-bold text-slate-800">₹{(ci.item.price * ci.quantity).toFixed(2)}</span>
                </div>
              </div>

              <div className="flex items-center justify-between sm:justify-end gap-3 pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                <div className="flex items-center bg-slate-100 rounded-xl border border-slate-200">
                  <button
                    onClick={() => updateQuantity(ci.item.id, ci.quantity - 1)}
                    className="px-2.5 py-1 text-sm font-bold text-slate-700 hover:bg-slate-200 rounded-l-xl cursor-pointer"
                    aria-label="Decrease quantity"
                  >
                    -
                  </button>
                  <span className="px-2 font-bold text-xs text-slate-900">{ci.quantity}</span>
                  <button
                    onClick={() => updateQuantity(ci.item.id, ci.quantity + 1)}
                    className="px-2.5 py-1 text-sm font-bold text-slate-700 hover:bg-slate-200 rounded-r-xl cursor-pointer"
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>

                <button
                  onClick={() => removeItem(ci.item.id)}
                  className="text-slate-400 hover:text-red-600 p-1.5 rounded-lg hover:bg-red-50 transition cursor-pointer"
                  title="Remove item"
                  aria-label="Remove item"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}

          <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs">
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1.5">
              Special Delivery Instructions (Optional)
            </label>
            <textarea
              rows={2}
              value={deliveryNotes}
              onChange={(e) => setDeliveryNotes(e.target.value)}
              placeholder="e.g. Ring doorbell, less spicy, pack extra napkins..."
              className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
            />
          </div>
        </div>

        {/* Bill Summary Sidebar */}
        <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-xs h-fit lg:sticky lg:top-24">
          <h3 className="font-extrabold text-slate-900 text-base mb-4 pb-3 border-b border-slate-100">
            Bill Summary
          </h3>

          <div className="space-y-2.5 text-xs text-slate-600">
            <div className="flex justify-between">
              <span>Item Total</span>
              <span className="font-bold text-slate-800">₹{totalAmount.toFixed(2)}</span>
            </div>
            <div className="flex justify-between">
              <span>Delivery Fee</span>
              <span className="font-bold text-emerald-600">FREE</span>
            </div>
            <div className="flex justify-between">
              <span>Taxes & Charges</span>
              <span className="font-bold text-slate-800">₹0.00</span>
            </div>
            <div className="pt-3 border-t border-slate-100 flex justify-between text-sm sm:text-base font-black text-slate-900">
              <span>To Pay</span>
              <span>₹{totalAmount.toFixed(2)}</span>
            </div>
          </div>

          <button
            onClick={handleCheckout}
            disabled={isLoading}
            className="w-full mt-6 bg-orange-600 hover:bg-orange-700 disabled:opacity-50 text-white font-black py-3 sm:py-3.5 rounded-xl shadow-md transition flex items-center justify-center gap-2 cursor-pointer text-xs sm:text-sm"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>Place Order • ₹{totalAmount.toFixed(2)}</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
