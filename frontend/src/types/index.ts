export type UserRole = 'admin' | 'customer';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  display_order: number;
  is_active: boolean;
  created_at: string;
}

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  category_id: number;
  category_name?: string;
  category_slug?: string;
  price: number;
  is_vegetarian: boolean;
  is_spicy: boolean;
  dietary_tags: string[];
  is_available: boolean;
  popularity_score: number;
  created_at: string;
  updated_at: string;
}

export interface ScoredMenuItem extends MenuItem {
  relevance_score: number;
  match_explanation: string;
  match_highlights: string[];
}

export interface SearchIntent {
  vegetarian: boolean | null;
  spicy: boolean | null;
  max_price: number | null;
  min_price: number | null;
  category: string | null;
  preferred_tags: string[];
  avoid_tags: string[];
  meal_type: string | null;
  extracted_keywords: string[];
}

export interface SearchResponseData {
  query: string;
  normalized_query: string;
  detected_intent: SearchIntent;
  results_count: number;
  search_mode: 'ai' | 'fallback' | 'cached';
  execution_time_ms: number;
  items: ScoredMenuItem[];
}

export type OrderStatus = 'placed' | 'confirmed' | 'preparing' | 'ready' | 'picked_up' | 'cancelled';

export interface OrderItem {
  id: string;
  menu_item_id: string;
  menu_item_name: string;
  quantity: number;
  unit_price: number;
  subtotal: number;
  is_vegetarian: boolean;
}

export interface Order {
  id: string;
  customer_id: string;
  customer_name?: string;
  customer_email?: string;
  status: OrderStatus;
  total_amount: number;
  delivery_notes?: string;
  created_at: string;
  updated_at: string;
  items: OrderItem[];
}

export interface MetricSummary {
  total_orders_today: number;
  total_revenue_today: number;
  average_order_value_today: number;
  active_orders_count: number;
}

export interface StatusCount {
  status: string;
  count: number;
}

export interface TopItemMetric {
  menu_item_id: string;
  name: string;
  category_name: string;
  units_sold: number;
  revenue_generated: number;
}

export interface DashboardData {
  summary: MetricSummary;
  orders_by_status: StatusCount[];
  top_selling_items: TopItemMetric[];
  recent_orders: Order[];
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message: string;
  error?: {
    code: string;
    message: string;
    details?: any;
  };
}
