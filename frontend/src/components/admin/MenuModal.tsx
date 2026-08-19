import React, { useState, useEffect } from 'react';
import { MenuItem, Category } from '../../types';
import { X } from 'lucide-react';

interface MenuModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: Partial<MenuItem>) => Promise<void>;
  categories: Category[];
  initialItem?: MenuItem | null;
}

export const MenuModal: React.FC<MenuModalProps> = ({
  isOpen,
  onClose,
  onSave,
  categories,
  initialItem,
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [categoryId, setCategoryId] = useState<number>(categories[0]?.id || 1);
  const [price, setPrice] = useState<number>(100);
  const [isVegetarian, setIsVegetarian] = useState(true);
  const [isSpicy, setIsSpicy] = useState(false);
  const [dietaryTagsStr, setDietaryTagsStr] = useState('');
  const [isAvailable, setIsAvailable] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (initialItem) {
      setName(initialItem.name);
      setDescription(initialItem.description);
      setCategoryId(initialItem.category_id);
      setPrice(initialItem.price);
      setIsVegetarian(initialItem.is_vegetarian);
      setIsSpicy(initialItem.is_spicy);
      setDietaryTagsStr(initialItem.dietary_tags.join(', '));
      setIsAvailable(initialItem.is_available);
    } else {
      setName('');
      setDescription('');
      setCategoryId(categories[0]?.id || 1);
      setPrice(100);
      setIsVegetarian(true);
      setIsSpicy(false);
      setDietaryTagsStr('starter, high-protein');
      setIsAvailable(true);
    }
  }, [initialItem, categories, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    const tags = dietaryTagsStr
      .split(',')
      .map((t) => t.trim().toLowerCase())
      .filter(Boolean);

    await onSave({
      name,
      description,
      category_id: categoryId,
      price: Number(price),
      is_vegetarian: isVegetarian,
      is_spicy: isSpicy,
      dietary_tags: tags,
      is_available: isAvailable,
    });
    setIsSubmitting(false);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-3 sm:p-4 overflow-y-auto">
      <div className="bg-white rounded-3xl max-w-lg w-full p-5 sm:p-6 shadow-2xl border border-slate-100 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center pb-3 sm:pb-4 border-b border-slate-100 mb-4">
          <h3 className="font-extrabold text-base sm:text-lg text-slate-900">
            {initialItem ? 'Edit Menu Dish' : 'Add New Menu Dish'}
          </h3>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100 transition"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Dish Name</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
              placeholder="e.g. Paneer Tikka"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Description</label>
            <textarea
              rows={2}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
              placeholder="Flavorful cottage cheese marinated in spices..."
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Category</label>
              <select
                value={categoryId}
                onChange={(e) => setCategoryId(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden bg-white"
              >
                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Price (₹)</label>
              <input
                type="number"
                required
                min="1"
                step="0.01"
                value={price}
                onChange={(e) => setPrice(Number(e.target.value))}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
              Dietary Tags (comma separated)
            </label>
            <input
              type="text"
              value={dietaryTagsStr}
              onChange={(e) => setDietaryTagsStr(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm focus:ring-2 focus:ring-orange-500 focus:outline-hidden"
              placeholder="high-protein, gluten-free, tandoor, light"
            />
          </div>

          <div className="flex flex-wrap items-center gap-4 sm:gap-6 pt-2">
            <label className="flex items-center gap-2 text-xs sm:text-sm font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                checked={isVegetarian}
                onChange={(e) => setIsVegetarian(e.target.checked)}
                className="w-4 h-4 text-orange-600 rounded"
              />
              <span>Vegetarian</span>
            </label>

            <label className="flex items-center gap-2 text-xs sm:text-sm font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                checked={isSpicy}
                onChange={(e) => setIsSpicy(e.target.checked)}
                className="w-4 h-4 text-orange-600 rounded"
              />
              <span>Spicy</span>
            </label>

            <label className="flex items-center gap-2 text-xs sm:text-sm font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                checked={isAvailable}
                onChange={(e) => setIsAvailable(e.target.checked)}
                className="w-4 h-4 text-orange-600 rounded"
              />
              <span>In Stock</span>
            </label>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs sm:text-sm font-bold text-slate-600 hover:bg-slate-100 rounded-xl cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-5 py-2 text-xs sm:text-sm font-bold bg-orange-600 hover:bg-orange-700 text-white rounded-xl shadow-xs cursor-pointer"
            >
              {isSubmitting ? 'Saving...' : 'Save Dish'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
