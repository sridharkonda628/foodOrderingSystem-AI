import React from 'react';
import { OrderStatus } from '../../types';
import { CheckCircle2, Clock, ChefHat, Bike, PackageCheck, XCircle } from 'lucide-react';

interface OrderTimelineProps {
  status: OrderStatus;
}

const STEPS = [
  { key: 'placed', label: 'Placed', icon: Clock, desc: 'Received by kitchen' },
  { key: 'confirmed', label: 'Confirmed', icon: CheckCircle2, desc: 'Kitchen accepted' },
  { key: 'preparing', label: 'Preparing', icon: ChefHat, desc: 'Chef is cooking' },
  { key: 'ready', label: 'Ready', icon: PackageCheck, desc: 'Packed & ready' },
  { key: 'picked_up', label: 'Picked Up', icon: Bike, desc: 'Delivered / Completed' },
];

export const OrderTimeline: React.FC<OrderTimelineProps> = ({ status }) => {
  if (status === 'cancelled') {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-5 sm:p-6 text-center text-red-700">
        <XCircle className="w-8 h-8 sm:w-10 sm:h-10 mx-auto mb-2 text-red-500" />
        <h4 className="font-extrabold text-sm sm:text-base">This Order was Cancelled</h4>
        <p className="text-xs text-red-500 mt-1">Contact restaurant support if you have any questions.</p>
      </div>
    );
  }

  const currentIndex = STEPS.findIndex((s) => s.key === status);

  return (
    <div className="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
      <h3 className="font-extrabold text-sm sm:text-base text-slate-900 mb-4 sm:mb-6">
        Live Order Status Tracker
      </h3>
      <div className="relative">
        {/* Desktop progress connector line */}
        <div className="hidden sm:block absolute top-5 left-8 right-8 h-1 bg-slate-200 -translate-y-1/2 z-0" />
        
        {/* Stepper Grid (Vertical on mobile, Horizontal on tablet/desktop) */}
        <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 sm:gap-2 relative z-10">
          {STEPS.map((step, idx) => {
            const Icon = step.icon;
            const isCompleted = idx <= currentIndex;
            const isCurrent = idx === currentIndex;

            return (
              <div
                key={step.key}
                className="flex sm:flex-col items-center sm:text-center gap-3 sm:gap-2 p-2 sm:p-0 rounded-xl sm:rounded-none bg-slate-50/50 sm:bg-transparent"
              >
                <div
                  className={`w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center shrink-0 transition-all ${
                    isCurrent
                      ? 'bg-orange-600 text-white ring-4 ring-orange-200 scale-105 sm:scale-110 shadow-md'
                      : isCompleted
                      ? 'bg-emerald-600 text-white'
                      : 'bg-slate-100 text-slate-400 border border-slate-300'
                  }`}
                >
                  <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                </div>
                <div className="flex-1 sm:flex-initial">
                  <div className={`text-xs font-bold ${isCurrent ? 'text-orange-600 font-black' : isCompleted ? 'text-slate-800' : 'text-slate-400'}`}>
                    {step.label}
                  </div>
                  <div className="text-[10px] sm:text-[11px] text-slate-400 leading-tight mt-0.5">{step.desc}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
