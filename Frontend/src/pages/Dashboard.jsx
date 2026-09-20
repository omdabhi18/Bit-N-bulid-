import React from 'react';
import { Link } from 'react-router-dom';
import {
  HeartPulse,
  Droplets,
  Sun,
  Sprout,
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  Clock,
  ArrowRight,
  TrendingUp,
  Radio,
  Sparkles,
  ShieldAlert,
  Calendar,
  Layers
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useFarm } from '../context/FarmContext';
import FarmMapbox from '../components/map/FarmMapbox';
import VoiceSpeaker from '../components/common/VoiceSpeaker';

export default function Dashboard() {
  const { t, language } = useLanguage();
  const {
    profile,
    telemetry,
    fields,
    advisories,
    risks,
    tasks,
    moveTask,
    approveAdvisory,
    triggerIrrigationValve,
    activeValve
  } = useFarm();

  const primaryAdvisory = advisories[0];
  const pendingTasks = tasks.filter(t => t.status === 'todo').slice(0, 4);

  const advisoryTitle = language === 'gu' && primaryAdvisory?.titleGu ? primaryAdvisory.titleGu :
                        language === 'hi' && primaryAdvisory?.titleHi ? primaryAdvisory.titleHi :
                        primaryAdvisory?.title;

  return (
    <div className="space-y-6 animate-in fade-in duration-200">
      
      {/* Farmer Welcome & Vernacular Audio Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-emerald-800 via-emerald-700 to-teal-800 rounded-3xl p-6 text-white shadow-xl relative overflow-hidden">
        {/* Background ambient glow */}
        <div className="absolute -right-12 -top-12 w-64 h-64 rounded-full bg-emerald-500/20 blur-3xl pointer-events-none" />
        <div className="absolute right-48 -bottom-16 w-64 h-64 rounded-full bg-teal-400/15 blur-3xl pointer-events-none" />

        <div className="relative z-10 space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider bg-white/15 text-emerald-100 backdrop-blur-sm border border-white/10">
              🌿 {profile.farmName}
            </span>
            <span className="flex items-center gap-1 text-xs text-emerald-200">
              <Radio className="w-3 h-3 text-emerald-300 animate-pulse" />
              {t("common.live", "Live AI Supervision Active")}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            {t("welcome", "Welcome back, Kishanbhai")}
          </h1>
          <p className="text-xs sm:text-sm text-emerald-100/90 max-w-2xl">
            {t("welcomeSub", "Autonomous multi-agent system has analyzed 4 sensor nodes and 7-day weather predictions. Water stress detected in Field A.")}
          </p>
        </div>

        <div className="relative z-10 flex flex-wrap items-center gap-3">
          <VoiceSpeaker
            text={`${t("welcome", "Welcome Kishanbhai")}. ${t("metrics.farmHealth", "Farm health")} ${telemetry.farmHealthScore}%. ${advisoryTitle}.`}
            label={t("dashboard.listenSummary", "Listen Farm Summary")}
            className="!bg-white !text-emerald-900 !px-4 !py-2 !text-xs !font-bold hover:!bg-emerald-50 shadow-md"
          />

          <Link
            to="/assistant"
            className="px-4 py-2 rounded-full bg-emerald-500/30 hover:bg-emerald-500/40 text-white text-xs font-bold border border-white/20 backdrop-blur-sm flex items-center gap-1.5 transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>{t("nav.voiceAssistant", "Kisan Voice AI")}</span>
          </Link>
        </div>
      </div>

      {/* Top Metric KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">
        
        {/* Farm Health Gauge */}
        <div className="bg-white p-4 rounded-2xl shadow-card-soft border border-slate-200/80 hover:border-emerald-300 transition-all card-hover">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>{t("metrics.farmHealth", "Farm Health")}</span>
            <HeartPulse className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-1.5">
            <span className="text-2xl font-extrabold text-slate-900">{telemetry.farmHealthScore}%</span>
            <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded">
              {t("metrics.good", "Good")}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">3 Fields Supervised</p>
        </div>

        {/* Soil Moisture */}
        <div className="bg-white p-4 rounded-2xl shadow-card-soft border border-slate-200/80 hover:border-amber-300 transition-all card-hover">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>{t("metrics.soilMoisture", "Soil Moisture")}</span>
            <Droplets className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2 flex items-baseline gap-1.5">
            <span className="text-2xl font-extrabold text-amber-600">{telemetry.soilMoisture}%</span>
            <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded">
              {t("metrics.deficit", "Deficit")}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Target: 45-55%</p>
        </div>

        {/* Weather */}
        <div className="bg-white p-4 rounded-2xl shadow-card-soft border border-slate-200/80 hover:border-sky-300 transition-all card-hover">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>{t("metrics.weather", "Weather")}</span>
            <Sun className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2 flex items-baseline gap-1.5">
            <span className="text-2xl font-extrabold text-slate-900">33°C</span>
            <span className="text-[10px] font-bold text-sky-700 bg-sky-50 px-1.5 py-0.5 rounded">12% Rain</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">14 km/h SW</p>
        </div>

        {/* Crop Stage */}
        <div className="bg-white p-4 rounded-2xl shadow-card-soft border border-slate-200/80 hover:border-emerald-300 transition-all card-hover">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>{t("metrics.cropStage", "Crop Stage")}</span>
            <Sprout className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 flex items-baseline gap-1.5">
            <span className="text-base font-extrabold text-slate-900 truncate">
              {language === 'gu' ? 'ફૂલ અવસ્થા' : language === 'hi' ? 'फूल अवस्था' : 'Flowering'}
            </span>
            <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded">Day 97</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Field A: Cotton</p>
        </div>

        {/* Overall Risk Level */}
        <div className="col-span-2 lg:col-span-1 bg-white p-4 rounded-2xl shadow-card-soft border border-slate-200/80 hover:border-rose-300 transition-all card-hover">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>{t("metrics.riskLevel", "Overall Risk")}</span>
            <AlertTriangle className="w-4 h-4 text-rose-500" />
          </div>
          <div className="mt-2 flex items-baseline gap-1.5">
            <span className="text-2xl font-extrabold text-rose-600">
              {language === 'gu' ? 'મધ્યમ' : language === 'hi' ? 'मध्यम' : 'Medium'}
            </span>
            <span className="text-[10px] font-bold text-rose-700 bg-rose-50 px-1.5 py-0.5 rounded">2 Active</span>
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Water & Pests</p>
        </div>

      </div>

      {/* Main Grid: AI Advisory Spotlight & Interactive Farm Map */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left 7 Columns: Today's Critical AI Recommendation */}
        <div className="lg:col-span-7 space-y-6">
          
          {primaryAdvisory && (
            <div className="bg-white rounded-3xl p-5 sm:p-6 shadow-card-soft border-2 border-amber-200/90 relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-amber-400 via-emerald-500 to-teal-500" />

              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="p-2 rounded-xl bg-amber-100 text-amber-800">
                    <Lightbulb className="w-5 h-5" />
                  </span>
                  <div>
                    <span className="text-[10px] font-bold tracking-wider uppercase text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200">
                      ⚡ {t("dashboard.todayAdvisoryTitle", "Action Required")} • {primaryAdvisory.priority}
                    </span>
                    <h3 className="text-base sm:text-lg font-bold text-slate-900 mt-1">
                      {advisoryTitle}
                    </h3>
                  </div>
                </div>

                <VoiceSpeaker
                  text={`${advisoryTitle}. ${primaryAdvisory.orchestratorSummary}`}
                  label={t("common.readAloud", "Listen")}
                />
              </div>

              <p className="text-xs sm:text-sm text-slate-600 mt-3 leading-relaxed">
                {primaryAdvisory.orchestratorSummary}
              </p>

              {/* Factors Matrix */}
              <div className="mt-4 pt-3 border-t border-slate-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
                    {t("advisoryPage.influencingTelemetry", "Why AI Recommends This:")}
                  </span>
                  <span className="text-xs font-extrabold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                    {primaryAdvisory.confidenceScore}% {t("common.confidence", "Confidence")}
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {primaryAdvisory.explainability.factors.map((f, idx) => (
                    <div key={idx} className="bg-slate-50 p-2 rounded-xl border border-slate-100 text-[11px]">
                      <span className="text-slate-400 block truncate">{f.name}</span>
                      <span className="font-bold text-slate-800">{f.value}</span>
                      <span className="text-[10px] text-amber-600 block mt-0.5 font-medium truncate">{f.impact}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-5 flex flex-wrap items-center gap-3">
                <button
                  onClick={() => approveAdvisory(primaryAdvisory.id)}
                  className="flex-1 min-w-[140px] py-2.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white text-xs font-bold shadow-md shadow-emerald-500/20 flex items-center justify-center gap-1.5 transition-all"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{t("dashboard.approveAndExecute", "Approve & Execute")}</span>
                </button>

                <button
                  onClick={() => triggerIrrigationValve('field-a', 35)}
                  className={`py-2.5 px-4 rounded-xl text-xs font-bold border transition-all flex items-center gap-1.5 ${
                    activeValve.fieldA
                      ? 'bg-sky-500 text-white border-sky-400 animate-pulse'
                      : 'bg-sky-50 text-sky-700 hover:bg-sky-100 border-sky-200'
                  }`}
                >
                  <Droplets className="w-4 h-4 text-sky-500" />
                  <span>
                    {activeValve.fieldA
                      ? t("dashboard.valveRunning", "Valve Running")
                      : t("dashboard.openValveNow", "Open Valve Now (35m)")}
                  </span>
                </button>

                <Link
                  to="/advisory"
                  className="py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-all"
                >
                  {t("common.askWhy", "Ask AI Why?")}
                </Link>
              </div>

            </div>
          )}

          {/* Pending Tasks Checklist */}
          <div className="bg-white rounded-3xl p-5 shadow-card-soft border border-slate-200/80">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-emerald-600" />
                <h3 className="font-bold text-slate-900 text-sm">
                  {t("dashboard.pendingActions", "Pending Farmer Actions")}
                </h3>
              </div>
              <Link to="/tasks" className="text-xs font-semibold text-emerald-600 hover:underline flex items-center gap-1">
                <span>{t("common.viewAll", "View All")}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="divide-y divide-slate-100 mt-2">
              {pendingTasks.map((tsk) => (
                <div key={tsk.id} className="py-2.5 flex items-center justify-between gap-3 group">
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => moveTask(tsk.id, 'completed')}
                      className="w-5 h-5 rounded-lg border-2 border-slate-300 hover:border-emerald-500 flex items-center justify-center transition-colors"
                      title="Mark task completed"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-transparent hover:text-emerald-500" />
                    </button>
                    <div>
                      <p className="text-xs font-bold text-slate-800 group-hover:text-emerald-700 transition-colors">
                        {tsk.title}
                      </p>
                      <p className="text-[11px] text-slate-400">
                        {tsk.field} • Due: {tsk.dueTime} • {tsk.assignedTo}
                      </p>
                    </div>
                  </div>

                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                    tsk.priority === 'High' ? 'bg-rose-100 text-rose-700' : 'bg-slate-100 text-slate-700'
                  }`}>
                    {tsk.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right 5 Columns: Interactive Map & Live Sensors */}
        <div className="lg:col-span-5 space-y-6">
          
          <div className="bg-white rounded-3xl p-4 sm:p-5 shadow-card-soft border border-slate-200/80">
            <div className="flex items-center justify-between pb-3">
              <div>
                <h3 className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                  <Layers className="w-4 h-4 text-emerald-600" />
                  {t("dashboard.fieldOverview", "Field Digital Twin Map")}
                </h3>
                <p className="text-[11px] text-slate-500">Tap plot to inspect</p>
              </div>
              <Link to="/map" className="text-xs font-bold text-emerald-600 hover:underline">
                {t("common.viewAll", "Fullscreen")} →
              </Link>
            </div>

            <FarmMapbox height="320px" />
          </div>

          <div className="bg-white rounded-3xl p-5 shadow-card-soft border border-slate-200/80">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                <Radio className="w-4 h-4 text-emerald-600 live-indicator" />
                {t("dashboard.quickStats", "Live Sensor Summary")}
              </h3>
              <Link to="/monitoring" className="text-xs font-bold text-emerald-600 hover:underline">
                {t("common.viewAll", "View Charts")} →
              </Link>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mt-3">
              <div className="p-2.5 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-semibold text-slate-400 block">{t("metrics.soilTemp", "Soil Temp")}</span>
                <span className="text-sm font-extrabold text-slate-800">{telemetry.soilTemperature}°C</span>
                <span className="text-[10px] text-emerald-600 block mt-0.5">{t("metrics.normal", "Normal")}</span>
              </div>
              <div className="p-2.5 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-semibold text-slate-400 block">{t("metrics.phLevel", "Soil pH")}</span>
                <span className="text-sm font-extrabold text-slate-800">{telemetry.soilPH}</span>
                <span className="text-[10px] text-emerald-600 block mt-0.5">{t("metrics.optimal", "Optimal")}</span>
              </div>
              <div className="p-2.5 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-semibold text-slate-400 block">{t("metrics.phosphorus", "Phosphorus (P)")}</span>
                <span className="text-sm font-extrabold text-rose-600">{telemetry.phosphorusLevel} mg/kg</span>
                <span className="text-[10px] text-rose-600 block mt-0.5">{t("metrics.deficient", "Deficient ⚠️")}</span>
              </div>
              <div className="p-2.5 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-semibold text-slate-400 block">{t("metrics.nitrogen", "Nitrogen (N)")}</span>
                <span className="text-sm font-extrabold text-slate-800">{telemetry.nitrogenLevel} mg/kg</span>
                <span className="text-[10px] text-emerald-600 block mt-0.5">{t("metrics.normal", "Balanced")}</span>
              </div>
              <div className="p-2.5 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-semibold text-slate-400 block">{t("metrics.airHumidity", "Air Humidity")}</span>
                <span className="text-sm font-extrabold text-slate-800">{telemetry.airHumidity}%</span>
                <span className="text-[10px] text-slate-500 block mt-0.5">RH</span>
              </div>
              <div className="p-2.5 rounded-2xl bg-slate-50 border border-slate-100">
                <span className="text-[10px] font-semibold text-slate-400 block">{t("metrics.soilEC", "Electrical Cond.")}</span>
                <span className="text-sm font-extrabold text-slate-800">{telemetry.soilEC} dS/m</span>
                <span className="text-[10px] text-emerald-600 block mt-0.5">{t("metrics.normal", "Normal")}</span>
              </div>
            </div>

          </div>

        </div>

      </div>

    </div>
  );
}
