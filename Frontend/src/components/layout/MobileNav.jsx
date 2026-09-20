import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MapPin, Lightbulb, CheckSquare, Mic, ChevronDown, ChevronUp } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export default function MobileNav() {
  const { t } = useLanguage();
  const [isMinimized, setIsMinimized] = useState(false);

  const links = [
    { path: "/", label: t("nav.dashboard", "Home"), icon: LayoutDashboard },
    { path: "/map", label: t("nav.farmMap", "Map"), icon: MapPin },
    { path: "/advisory", label: t("nav.advisory", "Advisory"), icon: Lightbulb },
    { path: "/tasks", label: t("nav.tasks", "Tasks"), icon: CheckSquare },
    { path: "/assistant", label: t("nav.voiceAssistant", "Voice AI"), icon: Mic, isVoice: true }
  ];

  if (isMinimized) {
    return (
      <div className="lg:hidden fixed bottom-3 right-3 z-40">
        <button
          onClick={() => setIsMinimized(false)}
          className="p-2.5 rounded-full bg-slate-900 text-white shadow-xl flex items-center gap-1 text-xs font-bold"
          title="Show Navigation"
        >
          <ChevronUp className="w-4 h-4" />
          <span>Menu</span>
        </button>
      </div>
    );
  }

  return (
    <div className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-md border-t border-slate-200 px-2 py-1 flex items-center justify-around shadow-lg">
      
      {/* Minimize toggle */}
      <button
        onClick={() => setIsMinimized(true)}
        className="p-1 text-slate-400 hover:text-slate-600 absolute -top-3 right-4 bg-white border border-slate-200 rounded-full shadow-sm"
        title="Minimize bottom bar"
      >
        <ChevronDown className="w-3.5 h-3.5" />
      </button>

      {links.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex flex-col items-center gap-0.5 px-2.5 py-1 rounded-xl text-[10px] font-medium transition-all ${
                item.isVoice
                  ? isActive
                    ? 'text-emerald-600 font-bold scale-105'
                    : 'text-emerald-600'
                  : isActive
                  ? 'text-emerald-700 font-bold scale-105'
                  : 'text-slate-500 hover:text-slate-900'
              }`
            }
          >
            {item.isVoice ? (
              <div className="w-7 h-7 rounded-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white flex items-center justify-center shadow-md -mt-2">
                <Icon className="w-3.5 h-3.5" />
              </div>
            ) : (
              <Icon className="w-4 h-4" />
            )}
            <span className="truncate max-w-[50px]">{item.label}</span>
          </NavLink>
        );
      })}
    </div>
  );
}
