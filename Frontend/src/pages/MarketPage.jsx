import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  Store,
  TrendingUp,
  TrendingDown,
  Sparkles,
  Building2
} from 'lucide-react';
import { marketCommodities } from '../data/mockFarmData';

export default function MarketPage() {
  const { t, language } = useLanguage();
  const [selectedCrop, setSelectedCrop] = useState(marketCommodities[0]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-amber-100 text-amber-800">
              <Store className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("marketPage.title", "APMC Mandi Intelligence & Price Arbitrage")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("marketPage.subtitle", "Live commodity arrivals across Rajkot, Gondal & regional markets with AI optimal selling window advice")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? "બજાર ભાવ રિપોર્ટ. ગોંડલ યાર્ડમાં કપાસનો ભાવ ₹૭,૪૨૦ છે. AI આગામી ૪ થી ૬ દિવસમાં માલ વેચવાની ભલામણ કરે છે."
              : `Market intelligence update. Cotton spot rate in Rajkot APMC is 7,380 rupees per quintal, up 4.2 percent this week. AI advises favorable selling window.`}
            label={t("marketPage.listenRates", "Listen Rates")}
          />
        </div>
      </div>

      {/* Commodity Selector Ribbon */}
      <div className="flex flex-wrap gap-3">
        {marketCommodities.map((item) => (
          <button
            key={item.id}
            onClick={() => setSelectedCrop(item)}
            className={`p-4 rounded-2xl border-2 transition-all text-left flex-1 min-w-[200px] ${
              selectedCrop.id === item.id
                ? 'border-emerald-500 bg-emerald-50 shadow-md ring-4 ring-emerald-500/10'
                : 'border-slate-200 bg-white hover:border-slate-300 shadow-card-soft'
            }`}
          >
            <span className="text-xs text-slate-400 block font-bold truncate">{item.crop}</span>
            <div className="flex items-baseline justify-between mt-1">
              <span className="text-xl font-extrabold text-slate-900">₹{item.currentPrice.toLocaleString()}</span>
              <span className={`text-xs font-bold flex items-center gap-0.5 ${
                item.trend === 'up' ? 'text-emerald-600' : 'text-rose-600'
              }`}>
                {item.trend === 'up' ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
                {item.change7d > 0 ? `+${item.change7d}%` : `${item.change7d}%`}
              </span>
            </div>
          </button>
        ))}
      </div>

      {/* Selected Commodity Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 7 Cols: Price Trend Graph & AI Selling Advice */}
        <div className="lg:col-span-7 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-4">
          
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="text-base font-bold text-slate-900">{selectedCrop.crop} {t("marketPage.priceTrend", "Price Trend (7 Days)")}</h3>
              <p className="text-xs text-slate-500">{t("marketPage.mspBenchmark", "MSP Benchmark")}: ₹{selectedCrop.mspPrice} / Quintal</p>
            </div>
            <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
              Spot: ₹{selectedCrop.currentPrice}
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={selectedCrop.priceHistory} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} domain={['auto', 'auto']} unit="₹" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderRadius: '16px', color: '#fff', fontSize: '12px', border: 'none' }}
                />
                <Line type="monotone" dataKey="price" stroke="#059669" strokeWidth={3} dot={{ r: 4, fill: '#059669' }} name="Price (₹/Qtl)" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* AI Selling Recommendation */}
          <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 text-xs space-y-1">
            <div className="flex items-center gap-2 text-emerald-900 font-bold">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>{t("marketPage.aiRecommendation", "AI Market Timing Recommendation:")}</span>
            </div>
            <p className="text-emerald-800 pl-6 leading-relaxed">
              {selectedCrop.aiRecommendation}
            </p>
          </div>

        </div>

        {/* Right 5 Cols: Nearby APMC Mandi Price Comparison */}
        <div className="lg:col-span-5 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-4">
          
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Building2 className="w-4 h-4 text-emerald-600" />
              {t("marketPage.nearbyMandi", "Nearby Mandi Arbitrage")}
            </h3>
            <span className="text-xs text-slate-400 font-medium">Rajkot Region</span>
          </div>

          <div className="space-y-3">
            {selectedCrop.nearbyMarkets.map((mandi, idx) => {
              const diff = mandi.price - selectedCrop.currentPrice;
              return (
                <div
                  key={idx}
                  className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center justify-between text-xs hover:bg-slate-100 transition-colors"
                >
                  <div>
                    <span className="font-bold text-slate-900 block">{mandi.name}</span>
                    <span className="text-[11px] text-slate-400">
                      {mandi.distance} • Arrivals: {mandi.arrivals}
                    </span>
                  </div>

                  <div className="text-right">
                    <span className="font-extrabold text-slate-900 text-sm block">₹{mandi.price}</span>
                    {diff > 0 ? (
                      <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded">
                        +₹{diff} Premium
                      </span>
                    ) : diff < 0 ? (
                      <span className="text-[10px] font-bold text-slate-400">
                        -₹{Math.abs(diff)}
                      </span>
                    ) : (
                      <span className="text-[10px] font-semibold text-slate-400">Local Reference</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="p-3 bg-amber-50 rounded-2xl border border-amber-200 text-[11px] text-amber-900 space-y-0.5">
            <span className="font-bold block">💡 {t("marketPage.profitTip", "Farmer Profit Tip:")}</span>
            Transporting 20 quintals to Gondal Mandi yields +₹800 net after nominal trucking cost.
          </div>

        </div>

      </div>

    </div>
  );
}
