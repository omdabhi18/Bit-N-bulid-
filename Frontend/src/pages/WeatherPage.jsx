import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  CloudSun,
  CloudRain,
  Wind,
  Droplets,
  Calendar,
  Clock
} from 'lucide-react';
import { weatherForecast } from '../data/mockFarmData';

export default function WeatherPage() {
  const { t, language } = useLanguage();
  const { current, hourly, daily } = weatherForecast;

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-sky-100 text-sky-800">
              <CloudSun className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("weatherPage.title", "Farming Weather Intelligence")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("weatherPage.subtitle", "Decision-first meteorology linking atmospheric forecasts directly to irrigation and chemical spray timing")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? `હવામાન સલાહ. તાપમાન ૩૩ અંશ છે. AI સલાહ આપે છે કે આજે સાંજે પિયત આપવું અનુકૂળ છે.`
              : `Weather intelligence advisory. Current temperature is 33 degrees Celsius. AI advises: ${current.advisory}`}
            label={t("weatherPage.listenForecast", "Listen Forecast")}
          />
        </div>
      </div>

      {/* AI Decision Alert Banner */}
      <div className="bg-gradient-to-r from-sky-900 via-slate-900 to-teal-950 p-6 rounded-3xl text-white shadow-xl space-y-3">
        <div className="flex items-center gap-2">
          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-sky-500 text-white">
            {t("weatherPage.decisionInsight", "AI Farming Decision Insight")}
          </span>
          <span className="text-xs text-sky-300">{t("weatherPage.station", "Station: Rajkot Agro-Met")}</span>
        </div>

        <h2 className="text-lg sm:text-xl font-bold leading-relaxed max-w-3xl">
          "{current.advisory}"
        </h2>

        <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-slate-300">
          <span className="flex items-center gap-1">
            <Wind className="w-4 h-4 text-sky-400" />
            Wind: {current.wind}
          </span>
          <span className="flex items-center gap-1">
            <Droplets className="w-4 h-4 text-sky-400" />
            ET₀: {current.et0}
          </span>
          <span className="flex items-center gap-1">
            <CloudRain className="w-4 h-4 text-sky-400" />
            Rain: {current.rainfallProb}%
          </span>
        </div>
      </div>

      {/* Hourly Weather Forecast */}
      <div className="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-3">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
          <Clock className="w-4 h-4 text-slate-500" />
          {t("weatherPage.hourlyTitle", "Today's Hourly Microclimate & Spraying Window")}
        </h3>

        <div className="grid grid-cols-3 sm:grid-cols-6 gap-3 pt-2">
          {hourly.map((h, i) => (
            <div key={i} className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 text-center space-y-1">
              <span className="text-xs font-bold text-slate-500 block">{h.time}</span>
              <span className="text-lg font-extrabold text-slate-900 block">{h.temp}°C</span>
              <div className="flex items-center justify-center gap-1 text-[11px] text-sky-600 font-semibold">
                <CloudRain className="w-3 h-3" />
                <span>{h.rainProb}%</span>
              </div>
              <span className="text-[10px] text-slate-400 block">Hum: {h.humidity}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* 7-Day Agronomic Forecast Table */}
      <div className="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-4">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
          <Calendar className="w-4 h-4 text-slate-500" />
          {t("weatherPage.sevenDayTitle", "7-Day Farming Action Suitability")}
        </h3>

        <div className="divide-y divide-slate-100">
          {daily.map((d, idx) => (
            <div key={idx} className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
              <div className="w-32 font-bold text-slate-800 text-sm">{d.day}</div>

              <div className="flex items-center gap-4 text-slate-600">
                <span className="w-24 font-bold text-slate-900">{d.tempMax}° / {d.tempMin}°C</span>
                <span className="w-28 flex items-center gap-1 text-sky-700">
                  <CloudRain className="w-3.5 h-3.5 text-sky-500" />
                  {d.rainProb}% Rain
                </span>
                <span className="text-slate-500">{d.condition}</span>
              </div>

              <div className="text-left sm:text-right">
                <span className={`inline-block px-3 py-1 rounded-full text-[11px] font-bold ${
                  d.sprayRating.includes('Good') || d.sprayRating.includes('Excellent')
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : d.sprayRating.includes('Poor')
                    ? 'bg-rose-50 text-rose-700 border border-rose-200'
                    : 'bg-amber-50 text-amber-700 border border-amber-200'
                }`}>
                  {t("weatherPage.sprayRating", "Spray")}: {d.sprayRating}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
