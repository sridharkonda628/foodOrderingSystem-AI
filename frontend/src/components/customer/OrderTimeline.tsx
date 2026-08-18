import React from 'react';
import { OrderStatus } from '../../types';
import { CheckCircle2, Clock, ChefHat, Bike, PackageCheck, XCircle } from 'lucide-react';

interface OrderTimelineProps {
  status: OrderStatus;
}

const STEPS = [
  { key: 'placed', label: 'Order Placed', icon: Clock, desc: 'Received by kitchen' },
  { key: 'confirmed', label: 'Confirmed', icon: CheckCircle2, desc: 'Kitchen accepted' },
  { key: 'preparing', label: 'Preparing', icon: ChefHat, desc: 'Chef is cooking' },
  { key: 'ready', label: 'Ready', icon: PackageCheck, desc: 'Packed & ready' },
  { key: 'picked_up', label: 'Picked Up', icon: Bike, desc: 'Completed / Delivered' },
];

export const OrderTimeline: React.FC<OrderTimelineProps> = ({ status }) => {
  if (status === 'cancelled') {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-6 text-center text-red-700">
        <XCircle className="w-10 h-10 mx-auto mb-2 text-red-500" />
        <h4 className="font-extrabold text-base">This Order was Cancelled</h4>
        <p className="text-xs text-red-500 mt-1">Contact restaurant support if you have questions.</p>
      </div>
    );
  }

  const currentIndex = STEPS.findIndex((s) => s.key === status);

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
      <h3 className="font-extrabold text-base text-slate-900 mb-6">Live Order Status Tracker</h3>
      <div className="relative">
        <div className="hidden sm:block absolute top-1/2 left-4 right-4 h-1 bg-slate-200 -translate-y-1/2 z-0" />
        
        <div className="grid grid-cols-1 sm:grid-cols-5 gap-4 relative z-10">
          {STEPS.map((step, idx) => {
            const Icon = step.icon;
            const isCompleted = idx <= currentIndex;
            const isCurrent = idx === currentIndex;

            return (
              <div key={step.key} className="flex sm:flex-col items-center sm:text-center gap-3 sm:gap-2">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
                    isCurrent
                      ? 'bg-orange-600 text-white ring-4 ring-orange-200 scale-110 shadow-md'
                      : isCompleted
                      ? 'bg-emerald-600 text-white'
                      : 'bg-slate-100 text-slate-400 border border-slate-300'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                </div>
                <div>
                  <div className={`text-xs font-bold ${isCurrent ? 'text-orange-600' : isCompleted ? 'text-slate-800' : 'text-slate-400'}`}>
                    {step.label}
                  </div>
                  <div className="text-[10px] text-slate-400">{step.desc}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
