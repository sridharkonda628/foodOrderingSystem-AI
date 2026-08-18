import React, { createContext, useContext, useState, useEffect } from 'react';
import { MenuItem } from '../types';

export interface CartItem {
  item: MenuItem;
  quantity: number;
}

interface CartContextType {
  items: CartItem[];
  addItem: (item: MenuItem, quantity?: number) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  removeItem: (itemId: string) => void;
  clearCart: () => void;
  totalItems: number;
  totalAmount: number;
  getItemQuantity: (itemId: string) => number;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [items, setItems] = useState<CartItem[]>(() => {
    const saved = localStorage.getItem('kpitech_cart');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('kpitech_cart', JSON.stringify(items));
  }, [items]);

  const addItem = (item: MenuItem, quantity: number = 1) => {
    setItems((prev) => {
      const existing = prev.find((ci) => ci.item.id === item.id);
      if (existing) {
        return prev.map((ci) =>
          ci.item.id === item.id ? { ...ci, quantity: ci.quantity + quantity } : ci
        );
      }
      return [...prev, { item, quantity }];
    });
  };

  const updateQuantity = (itemId: string, quantity: number) => {
    if (quantity <= 0) {
      removeItem(itemId);
      return;
    }
    setItems((prev) =>
      prev.map((ci) => (ci.item.id === itemId ? { ...ci, quantity } : ci))
    );
  };

  const removeItem = (itemId: string) => {
    setItems((prev) => prev.filter((ci) => ci.item.id !== itemId));
  };

  const clearCart = () => {
    setItems([]);
  };

  const getItemQuantity = (itemId: string): number => {
    const found = items.find((ci) => ci.item.id === itemId);
    return found ? found.quantity : 0;
  };

  const totalItems = items.reduce((sum, ci) => sum + ci.quantity, 0);
  const totalAmount = items.reduce((sum, ci) => sum + ci.item.price * ci.quantity, 0);

  return (
    <CartContext.Provider
      value={{
        items,
        addItem,
        updateQuantity,
        removeItem,
        clearCart,
        totalItems,
        totalAmount,
        getItemQuantity,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within a CartProvider');
  return context;
};
