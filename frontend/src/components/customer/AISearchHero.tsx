import React, { useState } from 'react';
import { Sparkles, Search, Zap, Flame } from 'lucide-react';
import { searchApi } from '../../api/searchApi';
import { SearchResponseData } from '../../types';
import { useCart } from '../../context/CartContext';

const EXAMPLE_QUERIES = [
  "something spicy and vegetarian under 200 rupees",
  "a light lunch that is not fried",
  "high protein food",
  "something filling but not too expensive",
  "vegetarian food without dairy",
  "spicy chicken dishes below 300"
];

interface AISearchHeroProps {
  onResultsFound?: (results: SearchResponseData | null) => void;
}

export const AISearchHero: React.FC<AISearchHeroProps> = ({ onResultsFound }) => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [searchData, setSearchData] = useState<SearchResponseData | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const { addItem, getItemQuantity, updateQuantity } = useCart();

  const handleSearch = async (targetQuery?: string) => {
    const q = (targetQuery !== undefined ? targetQuery : query).trim();
    if (!q) return;

    setQuery(q);
    setIsLoading(true);
    setErrorMsg(null);

    try {
      const res = await searchApi.searchNaturalLanguage(q, 8);
      if (res.success && res.data) {
        setSearchData(res.data);
        if (onResultsFound) onResultsFound(res.data);
      }
    } catch (err: any) {
      setErrorMsg(err.response?.data?.error?.message || 'Failed to process AI search.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setSearchData(null);
    setQuery('');
    if (onResultsFound) onResultsFound(null);
  };

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-slate-800 to-orange-950 text-white p-5 sm:p-8 lg:p-10 shadow-2xl border border-slate-700/50 my-4 sm:my-6">
      {/* Ambient background glows */}
      <div className="absolute top-0 right-0 -mt-10 -mr-10 w-60 sm:w-80 h-60 sm:h-80 bg-orange-500/20 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -mb-10 -ml-10 w-60 sm:w-80 h-60 sm:h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-3xl mx-auto text-center">
        <div className="inline-flex items-center gap-1.5 sm:gap-2 px-3 py-1 sm:px-3.5 sm:py-1.5 rounded-full bg-orange-500/20 border border-orange-500/30 text-orange-300 text-[10px] sm:text-xs font-bold uppercase tracking-wider mb-3 sm:mb-4 animate-pulse">
          <Sparkles className="w-3.5 h-3.5 shrink-0" />
          <span>AI-Powered Natural Language Menu Search</span>
        </div>

        <h1 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight mb-2 sm:mb-3 leading-tight">
          What are you craving today?
        </h1>
        <p className="text-slate-300 text-xs sm:text-sm lg:text-base max-w-xl mx-auto mb-5 sm:mb-6 leading-relaxed">
          Search dishes naturally by price, taste, spicy level, or dietary goals. Our hybrid AI parses your intent and ranks matching food in milliseconds.
        </p>

        {/* Search Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSearch();
          }}
          className="relative flex items-center mb-3 sm:mb-4"
        >
          <div className="absolute left-3.5 sm:left-4 text-slate-400 pointer-events-none">
            <Search className="w-4 h-4 sm:w-5 sm:h-5" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder='Try: "something spicy and vegetarian under 200"...'
            className="w-full pl-10 sm:pl-12 pr-24 sm:pr-32 py-3.5 sm:py-4 bg-white/10 hover:bg-white/15 focus:bg-white/20 text-white placeholder-slate-400 rounded-2xl border border-white/20 focus:outline-hidden focus:ring-2 focus:ring-orange-500 backdrop-blur-md text-xs sm:text-sm lg:text-base transition"
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="absolute right-1.5 sm:right-2 px-3.5 sm:px-5 py-2 sm:py-2.5 bg-gradient-to-r from-orange-500 to-amber-500 hover:from-orange-600 hover:to-amber-600 disabled:opacity-50 text-white font-bold rounded-xl text-xs sm:text-sm flex items-center gap-1.5 shadow-md transition cursor-pointer"
          >
            {isLoading ? (
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <span>Search</span>
                <Sparkles className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              </>
            )}
          </button>
        </form>

        {errorMsg && (
          <div className="mb-4 bg-red-500/20 border border-red-500/40 text-red-200 text-xs px-3 py-2 rounded-xl">
            {errorMsg}
          </div>
        )}

        {/* Quick Suggestion Pills */}
        <div className="flex flex-wrap items-center justify-center gap-1.5 sm:gap-2 text-[11px] sm:text-xs">
          <span className="text-slate-400 font-semibold w-full sm:w-auto block sm:inline mb-1 sm:mb-0">
            Try queries:
          </span>
          {EXAMPLE_QUERIES.map((ex, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSearch(ex)}
              className="bg-white/10 hover:bg-orange-500/30 border border-white/15 hover:border-orange-400/50 text-slate-200 hover:text-white px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full transition cursor-pointer text-[11px] sm:text-xs"
            >
              {ex}
            </button>
          ))}
        </div>
      </div>

      {/* AI Search Results Container */}
      {searchData && (
        <div className="relative z-10 mt-6 sm:mt-8 pt-6 sm:pt-8 border-t border-white/15">
          {/* Intent Summary Box */}
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 sm:p-5 border border-white/15 mb-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <div className="w-7 h-7 rounded-lg bg-orange-500/30 flex items-center justify-center text-orange-400 shrink-0">
                  <Zap className="w-4 h-4" />
                </div>
                <div>
                  <span className="text-[10px] sm:text-xs text-slate-400 block uppercase font-bold tracking-wider">
                    AI Detected Intent
                  </span>
                  <span className="text-xs sm:text-sm font-bold text-white">"{searchData.query}"</span>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="bg-emerald-500/20 text-emerald-300 px-2.5 py-0.5 sm:py-1 rounded-full border border-emerald-500/30 font-medium text-[11px] sm:text-xs">
                  ⚡ {searchData.execution_time_ms}ms
                </span>
                <span className="bg-blue-500/20 text-blue-300 px-2.5 py-0.5 sm:py-1 rounded-full border border-blue-500/30 font-medium uppercase text-[10px]">
                  Mode: {searchData.search_mode}
                </span>
                <button
                  onClick={handleClear}
                  className="text-slate-400 hover:text-white underline text-xs ml-auto sm:ml-2 cursor-pointer font-semibold"
                >
                  Clear Results
                </button>
              </div>
            </div>

            {/* Constraint Badges */}
            <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 mt-3 text-xs">
              <span className="text-slate-300 font-semibold text-[11px] sm:text-xs">Extracted Filters:</span>
              {searchData.detected_intent.vegetarian !== null && (
                <span className={`px-2.5 py-0.5 rounded-full font-bold text-[11px] sm:text-xs ${
                  searchData.detected_intent.vegetarian
                    ? 'bg-emerald-500/30 text-emerald-300 border border-emerald-500/40'
                    : 'bg-rose-500/30 text-rose-300 border border-rose-500/40'
                }`}>
                  {searchData.detected_intent.vegetarian ? '🌱 Vegetarian' : '🍗 Non-Vegetarian'}
                </span>
              )}

              {searchData.detected_intent.spicy !== null && (
                <span className={`px-2.5 py-0.5 rounded-full font-bold text-[11px] sm:text-xs ${
                  searchData.detected_intent.spicy
                    ? 'bg-red-500/30 text-red-300 border border-red-500/40'
                    : 'bg-blue-500/30 text-blue-300 border border-blue-500/40'
                }`}>
                  {searchData.detected_intent.spicy ? '🔥 Spicy' : '🥛 Mild / Non-Spicy'}
                </span>
              )}

              {searchData.detected_intent.max_price !== null && (
                <span className="bg-amber-500/30 text-amber-300 border border-amber-500/40 px-2.5 py-0.5 rounded-full font-bold text-[11px] sm:text-xs">
                  💰 Max: ₹{searchData.detected_intent.max_price}
                </span>
              )}

              {searchData.detected_intent.preferred_tags?.map((t, idx) => (
                <span key={idx} className="bg-purple-500/30 text-purple-300 border border-purple-500/40 px-2.5 py-0.5 rounded-full font-medium text-[11px] sm:text-xs">
                  🏷️ {t}
                </span>
              ))}
            </div>
          </div>

          {/* Heading */}
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2">
              <span>Matching Dishes</span>
              <span className="text-xs bg-orange-500/30 text-orange-300 px-2 py-0.5 rounded-full border border-orange-500/40 font-bold">
                {searchData.results_count} found
              </span>
            </h3>
          </div>

          {/* Grid of Results */}
          {searchData.items.length === 0 ? (
            <div className="text-center py-10 bg-white/5 rounded-2xl border border-white/10 px-4">
              <p className="text-slate-300 font-semibold mb-1 text-sm sm:text-base">No dishes matched your exact criteria.</p>
              <p className="text-xs text-slate-400">Try relaxing constraints like price or dietary requirements.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-slate-900">
              {searchData.items.map((item) => {
                const qty = getItemQuantity(item.id);
                const relevancePct = Math.round(item.relevance_score * 100);

                return (
                  <div
                    key={item.id}
                    className="bg-white rounded-2xl p-4 sm:p-5 shadow-lg border border-slate-100 flex flex-col justify-between hover:shadow-xl transition"
                  >
                    <div>
                      <div className="flex justify-between items-start gap-2 mb-2">
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
                          <span className="text-xs font-semibold text-slate-500">{item.category_name}</span>
                        </div>
                        <span className="bg-gradient-to-r from-orange-500 to-amber-500 text-white font-black text-[10px] sm:text-[11px] px-2 py-0.5 rounded-full shadow-xs shrink-0">
                          {relevancePct}% Match
                        </span>
                      </div>

                      <h4 className="font-extrabold text-sm sm:text-base text-slate-900 leading-snug">{item.name}</h4>
                      <p className="text-xs text-slate-500 mt-1 line-clamp-2">{item.description}</p>

                      <div className="mt-2.5 bg-orange-50 border border-orange-200/70 rounded-xl p-2 text-[11px] text-orange-900 font-medium flex items-start gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-orange-600 shrink-0 mt-0.5" />
                        <span className="leading-tight">{item.match_explanation}</span>
                      </div>
                    </div>

                    <div className="flex justify-between items-center mt-4 pt-3 border-t border-slate-100">
                      <span className="text-base sm:text-lg font-black text-slate-900">₹{item.price}</span>

                      {qty > 0 ? (
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
                          className="bg-orange-600 hover:bg-orange-700 text-white font-bold text-xs px-3.5 py-2 rounded-xl shadow-xs transition hover:shadow cursor-pointer"
                        >
                          Add to Cart
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
