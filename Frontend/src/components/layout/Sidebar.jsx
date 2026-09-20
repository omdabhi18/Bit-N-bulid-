import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  MapPin,
  Activity,
  AlertTriangle,
  Lightbulb,
  FileCheck2,
  CheckSquare,
  Bot,
  ScanEye,
  CloudSun,
  Store,
  Mic,
  UserCheck,
  FileText,
  Settings2,
  X,
  Sparkles,
  PanelLeftClose
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { useFarm } from '../../context/FarmContext';

export default function Sidebar({ isVisible, onClose }) {
  const { t } = useLanguage();
  const { advisories, risks, tasks, telemetry, profile } = useFarm();

  const pendingAdv = advisories.filter(a => a.status === 'Pending Approval').length;
  const highRisks = risks.filter(r => r.severity === 'Critical' || r.severity === 'High').length;
  const pendingTasks = tasks.filter(t => t.status === 'todo').length;

  const navSections = [
    {
      title: t("nav.coreOverview", "Core Overview"),
      items: [
        { path: "/", label: t("nav.dashboard", "Dashboard"), icon: LayoutDashboard },
        { path: "/map", label: t("nav.farmMap", "Farm Map & Fields"), icon: MapPin },
        { path: "/monitoring", label: t("nav.monitoring", "Live Sensors"), icon: Activity }
      ]
    },
    {
      title: t("nav.aiIntelligence", "AI Intelligence"),
      items: [
        { path: "/risks", label: t("nav.risks", "Risk Detection"), icon: AlertTriangle, badge: highRisks > 0 ? highRisks : null, badgeColor: "bg-rose-500" },
        { path: "/advisory", label: t("nav.advisory", "AI Advisory"), icon: Lightbulb, badge: pendingAdv > 0 ? `${pendingAdv}` : null, badgeColor: "bg-amber-500" },
        { path: "/action-plans", label: t("nav.actionPlans", "Action Plans"), icon: FileCheck2 },
        { path: "/agents", label: t("nav.agents", "AI Agent Center"), icon: Bot, isSpecial: true }
      ]
    },
    {
      title: t("nav.operations", "Operations & Farm Care"),
      items: [
        { path: "/tasks", label: t("nav.tasks", "Task Execution"), icon: CheckSquare, badge: pendingTasks > 0 ? pendingTasks : null, badgeColor: "bg-emerald-600" },
        { path: "/disease-detector", label: t("nav.diseaseDetector", "Crop Disease AI"), icon: ScanEye },
        { path: "/weather", label: t("nav.weather", "Weather Intelligence"), icon: CloudSun },
        { path: "/market", label: t("nav.market", "Mandi Prices"), icon: Store }
      ]
    },
    {
      title: t("nav.farmerAssistance", "Farmer Assistance"),
      items: [
        { path: "/assistant", label: t("nav.voiceAssistant", "Kisan Voice AI"), icon: Mic, isVoice: true },
        { path: "/escalation", label: t("nav.escalation", "Agronomist Help"), icon: UserCheck },
        { path: "/reports", label: t("nav.reports", "Audit & Reports"), icon: FileText },
        { path: "/setup", label: t("nav.farmSetup", "Farm Setup"), icon: Settings2 }
      ]
    }
  ];

  if (!isVisible) {
    return null; // completely hide sidebar when toggled off by user
  }

  return (
    <>
      {/* Mobile backdrop */}
      <div
        onClick={onClose}
        className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-sm lg:hidden transition-opacity"
      />

      <aside className="w-64 shrink-0 bg-white border-r border-slate-200 flex flex-col z-40 h-[calc(100vh-57px)] sticky top-[57px] shadow-sm transition-all overflow-hidden">
        
        {/* Sidebar Header & User Collapse control */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-800 text-xs uppercase tracking-wider">
              {t("nav.coreOverview", "Navigation")}
            </span>
          </div>
          
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-all"
            title={t("navToggle.hideSidebar", "Hide Menu")}
          >
            <PanelLeftClose className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation links list */}
        <div className="flex-1 overflow-y-auto px-3 py-3 space-y-5">
          {navSections.map((section, idx) => (
            <div key={idx}>
              <p className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5 font-sans">
                {section.title}
              </p>
              <div className="space-y-1">
                {section.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.path}
                      to={item.path}
                      className={({ isActive }) =>
                        `flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all group ${
                          isActive
                            ? item.isVoice
                              ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-500/20 font-bold'
                              : 'bg-emerald-50 text-emerald-900 font-bold border border-emerald-200'
                            : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                        }`
                      }
                    >
                      <div className="flex items-center gap-2.5 truncate">
                        <Icon className="w-4 h-4 shrink-0 transition-transform group-hover:scale-110" />
                        <span className="truncate">{item.label}</span>
                      </div>

                      {item.badge && (
                        <span className={`px-1.5 py-0.2 text-[10px] font-bold text-white rounded-full ${item.badgeColor} ml-1`}>
                          {item.badge}
                        </span>
                      )}

                      {item.isSpecial && (
                        <span className="flex items-center gap-0.5 px-1 py-0.5 text-[9px] font-bold bg-purple-100 text-purple-700 rounded ml-1">
                          <Sparkles className="w-2.5 h-2.5 text-purple-600" />
                        </span>
                      )}
                    </NavLink>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar Footer: Farm Health Index Card */}
        <div className="p-3 m-2.5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 text-white text-xs shrink-0">
          <div className="flex items-center justify-between">
            <span className="text-[10px] text-slate-400 font-medium">{t("metrics.farmHealth", "Farm Health Index")}</span>
            <span className="px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold text-[9px]">
              {t("metrics.good", "GOOD")}
            </span>
          </div>
          <div className="mt-1 flex items-baseline justify-between">
            <span className="text-lg font-extrabold text-white">{telemetry.farmHealthScore}%</span>
            <span className="text-[10px] text-slate-300">{profile.totalAreaAcre} Acres</span>
          </div>
          <div className="w-full bg-slate-700 h-1 rounded-full mt-1.5 overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${telemetry.farmHealthScore}%` }}></div>
          </div>
        </div>

      </aside>
    </>
  );
}
