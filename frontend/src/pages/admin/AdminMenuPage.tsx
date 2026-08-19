import React, { useState, useEffect } from 'react';
import { menuApi } from '../../api/menuApi';
import { Category, MenuItem } from '../../types';
import { MenuModal } from '../../components/admin/MenuModal';
import { Shield, Plus, Edit2, Trash2, CheckCircle2, XCircle } from 'lucide-react';

export const AdminMenuPage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<MenuItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [catRes, itemRes] = await Promise.all([
        menuApi.getCategories(),
        menuApi.getMenuItems({ available_only: false }),
      ]);
      if (catRes.success) setCategories(catRes.data);
      if (itemRes.success) setMenuItems(itemRes.data);
    } catch (err) {
      console.error('Failed to load menu', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleToggleAvailability = async (item: MenuItem) => {
    try {
      await menuApi.toggleAvailability(item.id, !item.is_available);
      fetchData();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to toggle availability.');
    }
  };

  const handleDeleteItem = async (itemId: string) => {
    if (!window.confirm('Are you sure you want to delete this menu dish?')) return;
    try {
      await menuApi.deleteMenuItem(itemId);
      fetchData();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to delete dish.');
    }
  };

  const handleSaveItem = async (data: Partial<MenuItem>) => {
    try {
      if (editingItem) {
        await menuApi.updateMenuItem(editingItem.id, data);
      } else {
        await menuApi.createMenuItem(data);
      }
      fetchData();
    } catch (err: any) {
      alert(err.response?.data?.error?.message || 'Failed to save menu dish.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-xl sm:text-2xl lg:text-3xl font-black text-slate-900 flex items-center gap-2">
            <Shield className="w-6 h-6 sm:w-7 sm:h-7 text-orange-600 shrink-0" />
            <span>Menu Catalog Management</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-0.5">
            Add dishes, edit descriptions, adjust prices, and toggle live item availability.
          </p>
        </div>

        <button
          onClick={() => {
            setEditingItem(null);
            setIsModalOpen(true);
          }}
          className="inline-flex items-center justify-center gap-2 bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs px-4 py-2.5 rounded-xl shadow-xs transition w-full sm:w-auto cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>Add New Dish</span>
        </button>
      </div>

      {isLoading ? (
        <div className="bg-white rounded-2xl p-8 border border-slate-200 animate-pulse h-64" />
      ) : (
        <>
          {/* Mobile Card View (< md) */}
          <div className="md:hidden space-y-4">
            {menuItems.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs flex flex-col justify-between gap-3"
              >
                <div>
                  <div className="flex justify-between items-start gap-2 mb-1.5">
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`w-3.5 h-3.5 rounded-xs flex items-center justify-center border text-[8px] font-bold shrink-0 ${
                          item.is_vegetarian
                            ? 'border-emerald-600 text-emerald-600'
                            : 'border-rose-600 text-rose-600'
                        }`}
                      >
                        ●
                      </span>
                      <h4 className="font-extrabold text-sm text-slate-900">{item.name}</h4>
                    </div>
                    <span className="font-black text-sm text-slate-900 shrink-0">₹{item.price}</span>
                  </div>

                  <div className="text-xs text-slate-500 mb-2">{item.category_name}</div>

                  <div className="flex flex-wrap gap-1 mb-2">
                    {item.dietary_tags.map((t, idx) => (
                      <span key={idx} className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[10px]">
                        {t}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                  <button
                    onClick={() => handleToggleAvailability(item)}
                    className={`px-3 py-1 rounded-full text-[11px] font-bold transition cursor-pointer flex items-center gap-1 ${
                      item.is_available
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : 'bg-red-50 text-red-700 border border-red-200'
                    }`}
                  >
                    {item.is_available ? (
                      <>
                        <CheckCircle2 className="w-3 h-3" />
                        <span>In Stock</span>
                      </>
                    ) : (
                      <>
                        <XCircle className="w-3 h-3" />
                        <span>Out of Stock</span>
                      </>
                    )}
                  </button>

                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => {
                        setEditingItem(item);
                        setIsModalOpen(true);
                      }}
                      className="p-2 text-slate-600 hover:text-slate-900 rounded-xl hover:bg-slate-100 transition"
                      title="Edit Dish"
                    >
                      <Edit2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteItem(item.id)}
                      className="p-2 text-slate-400 hover:text-red-600 rounded-xl hover:bg-red-50 transition"
                      title="Delete Dish"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Desktop Table View (>= md) */}
          <div className="hidden md:block bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200 text-left text-xs">
                <thead className="bg-slate-50 text-slate-500 uppercase font-bold tracking-wider">
                  <tr>
                    <th className="px-6 py-3.5">Dish</th>
                    <th className="px-6 py-3.5">Category</th>
                    <th className="px-6 py-3.5">Price</th>
                    <th className="px-6 py-3.5">Dietary</th>
                    <th className="px-6 py-3.5">Availability</th>
                    <th className="px-6 py-3.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {menuItems.map((item) => (
                    <tr key={item.id} className="hover:bg-slate-50 transition">
                      <td className="px-6 py-4 font-bold text-slate-900 flex items-center gap-2">
                        <span
                          className={`w-3.5 h-3.5 rounded-xs flex items-center justify-center border text-[8px] font-bold shrink-0 ${
                            item.is_vegetarian
                              ? 'border-emerald-600 text-emerald-600'
                              : 'border-rose-600 text-rose-600'
                          }`}
                        >
                          ●
                        </span>
                        <span>{item.name}</span>
                      </td>
                      <td className="px-6 py-4 text-slate-600">{item.category_name}</td>
                      <td className="px-6 py-4 font-black text-slate-900">₹{item.price}</td>
                      <td className="px-6 py-4">
                        <div className="flex flex-wrap gap-1">
                          {item.dietary_tags.slice(0, 3).map((t, idx) => (
                            <span key={idx} className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[10px]">
                              {t}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => handleToggleAvailability(item)}
                          className={`px-3 py-1 rounded-full text-xs font-bold transition cursor-pointer ${
                            item.is_available
                              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100'
                              : 'bg-red-50 text-red-700 border border-red-200 hover:bg-red-100'
                          }`}
                        >
                          {item.is_available ? '● In Stock' : '✕ Out of Stock'}
                        </button>
                      </td>
                      <td className="px-6 py-4 text-right space-x-2">
                        <button
                          onClick={() => {
                            setEditingItem(item);
                            setIsModalOpen(true);
                          }}
                          className="p-1.5 text-slate-500 hover:text-slate-900 rounded-lg hover:bg-slate-100 transition cursor-pointer"
                          title="Edit"
                        >
                          <Edit2 className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDeleteItem(item.id)}
                          className="p-1.5 text-slate-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition cursor-pointer"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <MenuModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSaveItem}
        categories={categories}
        initialItem={editingItem}
      />
    </div>
  );
};
