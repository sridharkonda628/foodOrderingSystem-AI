import React from 'react';
import { MenuItem } from '../../types';
import { useCart } from '../../context/CartContext';
import { Flame, AlertCircle } from 'lucide-react';

interface MenuCardProps {
  item: MenuItem;
}

export const MenuCard: React.FC<MenuCardProps> = ({ item }) => {
  const { addItem, getItemQuantity, updateQuantity } = useCart();
  const qty = getItemQuantity(item.id);

  return (
    <div className={`bg-white rounded-2xl p-4 sm:p-5 border transition duration-200 flex flex-col justify-between ${
      item.is_available ? 'border-slate-200 hover:border-orange-300 hover:shadow-lg' : 'border-slate-200 opacity-60 bg-slate-50'
    }`}>
      <div>
        <div className="flex justify-between items-start gap-2 mb-2">
          <div className="flex items-center gap-1.5 sm:gap-2">
            <span
              className={`w-3.5 h-3.5 sm:w-4 sm:h-4 rounded-xs sm:rounded-sm flex items-center justify-center border text-[8px] sm:text-[9px] font-bold shrink-0 ${
                item.is_vegetarian
                  ? 'border-emerald-600 text-emerald-600'
                  : 'border-rose-600 text-rose-600'
              }`}
              title={item.is_vegetarian ? 'Vegetarian' : 'Non-Vegetarian'}
            >
              ●
            </span>
            <span className="text-[11px] sm:text-xs font-semibold text-slate-500 uppercase tracking-wide">
              {item.category_name}
            </span>
          </div>

          {item.is_spicy && (
            <span className="flex items-center gap-0.5 bg-red-50 text-red-600 text-[10px] font-bold px-2 py-0.5 rounded-full border border-red-200 shrink-0">
              <Flame className="w-3 h-3" />
              Spicy
            </span>
          )}
        </div>

        <h3 className="font-extrabold text-sm sm:text-base text-slate-900 mb-1 leading-snug">{item.name}</h3>
        <p className="text-xs text-slate-500 line-clamp-2 mb-3 leading-relaxed">{item.description}</p>

        <div className="flex flex-wrap gap-1.5 mb-4">
          {item.dietary_tags.map((tag, idx) => (
            <span
              key={idx}
              className="bg-slate-100 text-slate-600 text-[10px] font-medium px-2 py-0.5 rounded-md"
            >
              {tag.replace('-', ' ')}
            </span>
          ))}
        </div>
      </div>

      <div className="flex justify-between items-center pt-3 border-t border-slate-100 mt-2">
        <div>
          <span className="text-base sm:text-lg font-black text-slate-900">₹{item.price}</span>
        </div>

        {!item.is_available ? (
          <span className="text-[11px] sm:text-xs font-bold text-red-600 bg-red-50 px-2.5 py-1 rounded-lg border border-red-100 flex items-center gap-1">
            <AlertCircle className="w-3 h-3 shrink-0" />
            Out of Stock
          </span>
        ) : qty > 0 ? (
          <div className="flex items-center bg-orange-600 text-white rounded-xl shadow-xs">
            <button
              onClick={() => updateQuantity(item.id, qty - 1)}
              className="px-2.5 py-1 text-sm font-bold hover:bg-orange-700 rounded-l-xl cursor-pointer"
              aria-label="Decrease quantity"
            >
              -
            </button>
            <span className="px-2 font-bold text-xs">{qty}</span>
            <button
              onClick={() => updateQuantity(item.id, qty + 1)}
              className="px-2.5 py-1 text-sm font-bold hover:bg-orange-700 rounded-r-xl cursor-pointer"
              aria-label="Increase quantity"
            >
              +
            </button>
          </div>
        ) : (
          <button
            onClick={() => addItem(item, 1)}
            className="bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs px-3.5 sm:px-4 py-1.5 sm:py-2 rounded-xl shadow-xs transition hover:shadow cursor-pointer"
          >
            Add
          </button>
        )}
      </div>
    </div>
  );
};
