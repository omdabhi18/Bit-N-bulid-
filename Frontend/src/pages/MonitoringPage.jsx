import React from 'react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  Activity,
  Droplets,
  Thermometer,
  Radio,
  BatteryCharging,
  Layers,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';
import { telemetryTimeSeries, npkRadarData } from '../data/mockFarmData';

export default function MonitoringPage() {
  const { telemetry, sensors } = useFarm();
  const { t, language } = useLanguage();

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
              <Activity className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("monitoringPage.title", "Live Sensor Monitoring & Analytics")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("monitoringPage.subtitle", "Real-time telemetry stream from 4 autonomous IoT edge nodes")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? `લાઇવ સેન્સર રિપોર્ટ. જમીનમાં ભેજ ૩૧.૪ ટકા છે જે સામાન્ય કરતાં ઓછો છે. જમીનનું તાપમાન ૨૭.૮ અંશ છે. ફોસ્ફરસ ખાતર ૧૪ mg/kg છે જે ઓછું છે.`
              : `Live sensor telemetry report. Soil moisture is at 31.4 percent, which is below the optimal threshold. Soil temperature is 27.8 degrees Celsius. Available phosphorus is low at 14 milligrams per kilogram.`}
            label={t("monitoringPage.listenStatus", "Listen Status")}
          />
        </div>
      </div>

      {/* Live Telemetry KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        
        <div className="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-card-soft card-hover">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>{t("metrics.soilMoisture", "Soil Moisture")}</span>
            <Droplets className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-amber-600">{telemetry.soilMoisture}%</span>
            <span className="flex items-center text-xs font-bold text-amber-600">
              <ArrowDownRight className="w-4 h-4" /> 5%
            </span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full mt-3 overflow-hidden">
            <div className="bg-amber-500 h-full rounded-full" style={{ width: `${telemetry.soilMoisture}%` }}></div>
          </div>
          <span className="text-[11px] text-slate-400 mt-1.5 block">{t("metrics.deficit", "Deficit")} • Target: 45%</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-card-soft card-hover">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>{t("metrics.soilTemp", "Soil Temperature")}</span>
            <Thermometer className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{telemetry.soilTemperature}°C</span>
            <span className="flex items-center text-xs font-bold text-emerald-600">
              <ArrowUpRight className="w-4 h-4" /> {t("metrics.normal", "Normal")}
            </span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full mt-3 overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: '68%' }}></div>
          </div>
          <span className="text-[11px] text-slate-400 mt-1.5 block">Root temperature safe</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-card-soft card-hover">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>{t("metrics.phLevel", "Soil Acidity / pH")}</span>
            <Layers className="w-4 h-4 text-sky-500" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-slate-900">{telemetry.soilPH}</span>
            <span className="text-xs font-bold text-emerald-600">{t("metrics.optimal", "Optimal")}</span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full mt-3 overflow-hidden">
            <div className="bg-sky-500 h-full rounded-full" style={{ width: '70%' }}></div>
          </div>
          <span className="text-[11px] text-slate-400 mt-1.5 block">Neutral (6.5 - 7.5)</span>
        </div>

        <div className="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-card-soft card-hover">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold">
            <span>{t("metrics.phosphorus", "Phosphorus (P)")}</span>
            <Activity className="w-4 h-4 text-rose-500" />
          </div>
          <div className="mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-rose-600">{telemetry.phosphorusLevel}</span>
            <span className="text-xs font-bold text-rose-600">mg/kg</span>
          </div>
          <div className="w-full bg-slate-100 h-2 rounded-full mt-3 overflow-hidden">
            <div className="bg-rose-500 h-full rounded-full" style={{ width: '30%' }}></div>
          </div>
          <span className="text-[11px] text-rose-600 font-semibold mt-1.5 block">{t("metrics.deficient", "Deficient (Target > 22 mg/kg)")}</span>
        </div>

      </div>

      {/* Recharts Analytics Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 7 Cols: Soil Moisture 24h Area Chart */}
        <div className="lg:col-span-7 bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-card-soft">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Droplets className="w-4 h-4 text-sky-600" />
                {t("monitoringPage.moistureTrend", "Soil Moisture Depletion Trend (24 Hours)")}
              </h3>
              <p className="text-xs text-slate-500">{t("monitoringPage.moistureSubtitle", "Root zone moisture trajectory toward wilting point")}</p>
            </div>
            <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
              Threshold: 28%
            </span>
          </div>

          <div className="h-72 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={telemetryTimeSeries} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="moistureGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#0284c7" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#0284c7" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="time" stroke="#94a3b8" fontSize={11} />
                <YAxis stroke="#94a3b8" fontSize={11} domain={[20, 50]} unit="%" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderRadius: '16px', color: '#fff', fontSize: '12px', border: 'none' }}
                />
                <Area type="monotone" dataKey="moisture" stroke="#0284c7" strokeWidth={3} fillOpacity={1} fill="url(#moistureGrad)" name="Moisture %" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right 5 Cols: NPK Soil Radar / Bar Chart */}
        <div className="lg:col-span-5 bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-card-soft">
          <div className="flex items-center justify-between pb-4 border-b border-slate-100">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Layers className="w-4 h-4 text-emerald-600" />
                {t("monitoringPage.npkBalance", "Nutrient Balance Index (NPK)")}
              </h3>
              <p className="text-xs text-slate-500">{t("monitoringPage.npkSubtitle", "Current levels vs agronomic target")}</p>
            </div>
          </div>

          <div className="h-72 w-full mt-4 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={npkRadarData} layout="vertical" margin={{ top: 10, right: 20, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis type="number" domain={[0, 100]} stroke="#94a3b8" fontSize={10} />
                <YAxis dataKey="nutrient" type="category" stroke="#64748b" fontSize={11} width={80} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderRadius: '12px', color: '#fff', fontSize: '12px' }} />
                <Bar dataKey="actual" fill="#10b981" radius={[0, 6, 6, 0]} name="Actual Value" />
                <Bar dataKey="optimal" fill="#cbd5e1" radius={[0, 6, 6, 0]} name="Benchmark Target" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* IoT Hardware Node Fleet Status */}
      <div className="bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/80 shadow-card-soft">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <Radio className="w-5 h-5 text-emerald-600 live-indicator" />
            <div>
              <h3 className="text-base font-bold text-slate-900">
                {t("monitoringPage.hardwareFleet", "IoT Edge Sensor Hardware Fleet")}
              </h3>
              <p className="text-xs text-slate-500">
                {t("monitoringPage.hardwareSubtitle", "Autonomous battery, LoRaWAN and 4G communication status")}
              </p>
            </div>
          </div>
          <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
            {t("monitoringPage.allOnline", "4 / 4 Online")}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          {sensors.map((s) => (
            <div key={s.id} className="p-4 rounded-2xl bg-slate-50 border border-slate-200/70 text-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-extrabold text-slate-900">{s.id}</span>
                <span className="flex items-center gap-1 text-emerald-600 font-bold text-[10px]">
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  {t("common.online", "Online")}
                </span>
              </div>
              <p className="text-slate-600 font-medium">{s.name}</p>
              <p className="text-[11px] text-slate-400">{s.field} • {s.type}</p>
              <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px]">
                <span className="flex items-center gap-1 text-slate-600">
                  <BatteryCharging className="w-3.5 h-3.5 text-emerald-600" />
                  {s.battery}%
                </span>
                <span className="text-slate-400">{s.lastSync}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
