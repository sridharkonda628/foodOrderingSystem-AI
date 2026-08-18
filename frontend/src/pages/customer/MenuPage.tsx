import React, { useState, useEffect } from 'react';
import { menuApi } from '../../api/menuApi';
import { Category, MenuItem } from '../../types';
import { AISearchHero } from '../../components/customer/AISearchHero';
import { MenuCard } from '../../components/customer/MenuCard';
import { Utensils, Flame, Leaf } from 'lucide-react';

export const MenuPage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [isVegOnly, setIsVegOnly] = useState(false);
  const [isSpicyOnly, setIsSpicyOnly] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const [catRes, itemRes] = await Promise.all([
          menuApi.getCategories(),
          menuApi.getMenuItems({ available_only: false }),
        ]);
        if (catRes.success) setCategories(catRes.data);
        if (itemRes.success) setMenuItems(itemRes.data);
      } catch (err) {
        console.error('Failed to load menu data', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredItems = menuItems.filter((item) => {
    if (selectedCategory !== null && item.category_id !== selectedCategory) return false;
    if (isVegOnly && !item.is_vegetarian) return false;
    if (isSpicyOnly && !item.is_spicy) return false;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <AISearchHero />

      <div className="mt-12 mb-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
          <div>
            <h2 className="text-2xl font-black text-slate-900 flex items-center gap-2">
              <Utensils className="w-6 h-6 text-orange-500" />
              Explore Full Restaurant Menu
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
              Browse our handcrafted categories or use quick dietary filters.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsVegOnly(!isVegOnly)}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold transition cursor-pointer ${
                isVegOnly
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
              }`}
            >
              <Leaf className="w-3.5 h-3.5 text-emerald-500" />
              Pure Veg Only
            </button>

            <button
              onClick={() => setIsSpicyOnly(!isSpicyOnly)}
              className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-bold transition cursor-pointer ${
                isSpicyOnly
                  ? 'bg-red-600 text-white shadow-xs'
                  : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
              }`}
            >
              <Flame className="w-3.5 h-3.5 text-red-500" />
              Spicy Only
            </button>
          </div>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto py-4 scrollbar-none">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition cursor-pointer ${
              selectedCategory === null
                ? 'bg-orange-600 text-white shadow-xs'
                : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
            }`}
          >
            All Categories ({menuItems.length})
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-4 py-2 rounded-xl text-xs font-bold whitespace-nowrap transition cursor-pointer ${
                selectedCategory === cat.id
                  ? 'bg-orange-600 text-white shadow-xs'
                  : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
              }`}
            >
              {cat.name}
            </button>
          ))}
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
            <div key={n} className="bg-white rounded-2xl p-5 border border-slate-200 animate-pulse h-64" />
          ))}
        </div>
      ) : filteredItems.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 p-8">
          <Utensils className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="font-extrabold text-slate-800 text-base">No dishes found</h3>
          <p className="text-xs text-slate-500 mt-1">Try clearing filters to see all available food items.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredItems.map((item) => (
            <MenuCard key={item.id} item={item} />
          ))}
        </div>
      )}
    </div>
  );
};
