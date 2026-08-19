import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-20 py-8 text-slate-500 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="font-bold text-slate-800">CraveAI</span>
          <span>•</span>
          <span>Food Ordering with AI Natural Language Menu Search</span>
        </div>

      </div>
    </footer>
  );
};
