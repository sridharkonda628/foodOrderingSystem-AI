import { apiClient } from './client';
import { ApiResponse, Order, OrderStatus } from '../types';

export const orderApi = {
  createOrder: async (items: { menu_item_id: string; quantity: number }[], delivery_notes?: string) => {
    const res = await apiClient.post<ApiResponse<Order>>('/orders', { items, delivery_notes });
    return res.data;
  },
  getMyOrders: async () => {
    const res = await apiClient.get<ApiResponse<Order[]>>('/orders');
    return res.data;
  },
  getOrderById: async (id: string) => {
    const res = await apiClient.get<ApiResponse<Order>>(`/orders/${id}`);
    return res.data;
  },
  cancelOrder: async (id: string) => {
    const res = await apiClient.patch<ApiResponse<Order>>(`/orders/${id}/cancel`);
    return res.data;
  },
  // Admin Endpoints
  getAllOrders: async (status?: string) => {
    const res = await apiClient.get<ApiResponse<Order[]>>('/admin/orders', { params: { status } });
    return res.data;
  },
  updateOrderStatus: async (id: string, status: OrderStatus) => {
    const res = await apiClient.patch<ApiResponse<Order>>(`/admin/orders/${id}/status`, { status });
    return res.data;
  },
  getDashboardMetrics: async () => {
    const res = await apiClient.get<ApiResponse<any>>('/admin/dashboard');
    return res.data;
  },
};
