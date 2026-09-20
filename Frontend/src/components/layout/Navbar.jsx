import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  Sun,
  CloudRain,
  Droplets,
  Bell,
  Mic,
  Menu,
  PanelLeftClose,
  PanelLeftOpen,
  EyeOff,
  Radio,
  Sparkles
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useFarm } from '../../context/FarmContext';

export default function Navbar({
  isSidebarVisible,
  onToggleSidebar,
  onHideNavbar
}) {
  const { language, setLanguage, t } = useLanguage();
  const { telemetry, activeValve, advisories, risks } = useFarm();
  const [showNotifications, setShowNotifications] = useState(false);

  const pendingAdvisories = advisories.filter(a => a.status === 'Pending Approval');
  const criticalRisks = risks.filter(r => r.severity === 'Critical' || r.severity === 'High');
  const totalAlerts = pendingAdvisories.length + criticalRisks.length;

  const isValveOpen = activeValve.fieldA || activeValve.fieldB || activeValve.fieldC;

  return (
    <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-md border-b border-slate-200 px-4 sm:px-6 py-2.5 transition-all shadow-sm">
      <div className="flex items-center justify-between gap-2 max-w-7xl mx-auto">
        
        {/* Left: Sidebar Toggle & Brand */}
        <div className="flex items-center gap-3">
          
          {/* User Control: Toggle/Hide/Show Sidebar */}
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-xl text-slate-700 hover:bg-slate-100 hover:text-emerald-700 transition-all border border-slate-200 flex items-center gap-1.5 text-xs font-bold"
            title={isSidebarVisible ? t("navToggle.hideSidebar", "Hide Sidebar") : t("navToggle.showSidebar", "Show Sidebar")}
            aria-label="Toggle Sidebar"
          >
            {isSidebarVisible ? (
              <>
                <PanelLeftClose className="w-4 h-4 text-emerald-600" />
                <span className="hidden md:inline">{t("navToggle.hideSidebar", "Hide Menu")}</span>
              </>
            ) : (
              <>
                <PanelLeftOpen className="w-4 h-4 text-emerald-600" />
                <span className="hidden md:inline">{t("navToggle.showSidebar", "Show Menu")}</span>
              </>
            )}
          </button>

          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-400 flex items-center justify-center shadow-md shadow-emerald-500/20 group-hover:scale-105 transition-transform">
              <Sprout className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-base sm:text-lg text-slate-900 tracking-tight font-sans">
                  {t("appName", "KrishiNetra")}
                </span>
                <span className="px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 rounded-md border border-emerald-200">
                  AI OS
                </span>
              </div>
              <p className="text-[10px] text-slate-500 hidden sm:block font-medium">
                {t("farmLocation", "Rajkot, Gujarat • GreenValley Farms")}
              </p>
            </div>
          </Link>
        </div>

        {/* Center: Live Status Tickers */}
        <div className="hidden md:flex items-center gap-3">
          {/* Weather Ticker */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 border border-slate-200/80 text-xs font-medium text-slate-700">
            <Sun className="w-3.5 h-3.5 text-amber-500" />
            <span>33°C {t("metrics.normal", "Sunny")}</span>
            <span className="text-slate-300">•</span>
            <span className="flex items-center gap-1 text-sky-700">
              <CloudRain className="w-3.5 h-3.5 text-sky-500" />
              12% {t("metrics.weather", "Rain")}
            </span>
          </div>

          {/* Drip Irrigation Valve Live Ticker */}
          {isValveOpen ? (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500 text-white text-xs font-semibold shadow-sm animate-pulse">
              <Droplets className="w-4 h-4 text-white" />
              <span>{t("dashboard.valveRunning", "Drip Valve Active (35m)")}</span>
            </div>
          ) : (
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-medium">
              <Radio className="w-3.5 h-3.5 text-emerald-600 live-indicator" />
              <span className="hidden lg:inline">{t("monitoringPage.hardwareFleet", "IoT Fleet")}</span>
              <span className="font-semibold text-emerald-900">{t("monitoringPage.allOnline", "4/4 Online")}</span>
            </div>
          )}
        </div>

        {/* Right: Language Switcher, Voice AI, Hide Topbar, Notifications */}
        <div className="flex items-center gap-2 sm:gap-2.5">
          
          {/* User Control: Hide Top Navbar (Zen Full-View Mode) */}
          <button
            onClick={onHideNavbar}
            className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 border border-slate-200 transition-all text-xs font-medium hidden sm:flex items-center gap-1"
            title={t("navToggle.hideNavbar", "Hide Top Bar (Full Screen)")}
          >
            <EyeOff className="w-3.5 h-3.5 text-slate-500" />
            <span className="hidden lg:inline">{t("navToggle.hideNavbar", "Hide Top Bar")}</span>
          </button>

          {/* Vernacular Language Switcher */}
          <div className="flex items-center bg-slate-100 rounded-xl p-0.5 border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setLanguage('en')}
              className={`px-2 py-1 rounded-lg transition-all ${
                language === 'en'
                  ? 'bg-white text-emerald-700 shadow-sm font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => setLanguage('gu')}
              className={`px-2 py-1 rounded-lg transition-all ${
                language === 'gu'
                  ? 'bg-white text-emerald-700 shadow-sm font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              ગુજરાતી
            </button>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-2 py-1 rounded-lg transition-all ${
                language === 'hi'
                  ? 'bg-white text-emerald-700 shadow-sm font-bold'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              हिंदी
            </button>
          </div>

          {/* Quick Kisan Voice AI link */}
          <Link
            to="/assistant"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-xs font-semibold shadow-sm hover:shadow-emerald-500/20 hover:scale-102 transition-all"
            title="Talk to Kisan AI in your language"
          >
            <Mic className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{t("nav.voiceAssistant", "Voice AI")}</span>
          </Link>

          {/* Notifications Center */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200 transition-colors"
              aria-label="Alerts"
            >
              <Bell className="w-4 h-4" />
              {totalAlerts > 0 && (
                <span className="absolute top-1 right-1 w-4 h-4 bg-rose-500 text-white rounded-full text-[10px] font-bold flex items-center justify-center animate-bounce">
                  {totalAlerts}
                </span>
              )}
            </button>

            {/* Notifications Dropdown */}
            {showNotifications && (
              <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-2xl shadow-2xl border border-slate-200 p-4 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
                <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                  <h4 className="font-bold text-slate-900 text-sm flex items-center gap-1.5">
                    <Bell className="w-4 h-4 text-emerald-600" />
                    {t("dashboard.activeAlerts", "Farm Alerts & Action Requests")}
                  </h4>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-rose-100 text-rose-700">
                    {totalAlerts} {t("common.critical", "Critical")}
                  </span>
                </div>

                <div className="divide-y divide-slate-100 max-h-80 overflow-y-auto mt-2">
                  {pendingAdvisories.map((adv) => (
                    <div key={adv.id} className="py-2.5">
                      <p className="text-xs font-bold text-slate-800">
                        {language === 'gu' && adv.titleGu ? adv.titleGu : language === 'hi' && adv.titleHi ? adv.titleHi : adv.title}
                      </p>
                      <p className="text-[11px] text-slate-500 mt-0.5">{adv.orchestratorSummary}</p>
                      <Link
                        to="/advisory"
                        onClick={() => setShowNotifications(false)}
                        className="inline-block mt-1 text-[11px] font-semibold text-emerald-600 hover:underline"
                      >
                        {t("advisoryPage.explainAdvisories", "Review & Approve Plan")} →
                      </Link>
                    </div>
                  ))}

                  {criticalRisks.map((r) => (
                    <div key={r.id} className="py-2.5">
                      <p className="text-xs font-bold text-slate-800">{r.category} ({r.field})</p>
                      <p className="text-[11px] text-slate-500 mt-0.5">{r.recommendedAction}</p>
                      <Link
                        to="/risks"
                        onClick={() => setShowNotifications(false)}
                        className="inline-block mt-1 text-[11px] font-semibold text-rose-600 hover:underline"
                      >
                        {t("risksPage.title", "Inspect Risk Matrix")} →
                      </Link>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Farmer Profile Avatar */}
          <Link to="/setup" className="flex items-center gap-2 pl-1.5 border-l border-slate-200">
            <div className="w-8 h-8 rounded-full bg-amber-100 border border-amber-300 flex items-center justify-center font-bold text-xs text-amber-800">
              KP
            </div>
          </Link>

        </div>

      </div>
    </header>
  );
}
