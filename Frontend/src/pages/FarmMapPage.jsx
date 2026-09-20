import React from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import FarmMapbox from '../components/map/FarmMapbox';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import { MapPin, Droplets } from 'lucide-react';

export default function FarmMapPage() {
  const { fields, selectedFieldId, setSelectedFieldId, triggerIrrigationValve, activeValve } = useFarm();
  const { t, language } = useLanguage();

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
              <MapPin className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("mapPage.title", "Farm Map & Digital Twin")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("mapPage.subtitle", "12.5 Acres • GPS: 21.9619° N, 70.7923° E (Gondal Taluka, Rajkot)")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? "ખેતરનો ડિજિટલ નકશો. ખેતર A માં કપાસ છે જેમાં પાણીની અછત છે. ખેતર B માં ઘઉં છે જેમાં જીવાતનો ભય છે. ખેતર C માં મગફળી તંદુરસ્ત છે."
              : "Farm Digital Twin view. Field A has 5.2 acres of Cotton with water stress. Field B has 4.1 acres of Wheat with pest alert. Field C has 3.2 acres of Groundnut in optimal condition."}
            label={t("mapPage.explainMap", "Explain Map")}
          />
        </div>
      </div>

      {/* Main Map Component */}
      <FarmMapbox height="560px" />

      {/* Field Inspection & Comparative Telemetry Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {fields.map((f) => {
          const isSelected = f.id === selectedFieldId;
          return (
            <div
              key={f.id}
              onClick={() => setSelectedFieldId(f.id)}
              className={`p-5 rounded-3xl transition-all cursor-pointer border-2 bg-white ${
                isSelected
                  ? 'border-emerald-500 shadow-lg ring-4 ring-emerald-500/10'
                  : 'border-slate-200 hover:border-slate-300 shadow-card-soft'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase ${
                    f.status === 'Critical' ? 'bg-rose-100 text-rose-700' :
                    f.status === 'Warning' ? 'bg-amber-100 text-amber-800' :
                    'bg-emerald-100 text-emerald-800'
                  }`}>
                    {f.status} {t("common.priority", "Status")}
                  </span>
                  <h3 className="font-bold text-slate-900 text-base mt-1.5">{f.name}</h3>
                  <p className="text-xs text-slate-500">{f.crop} • {f.area}</p>
                </div>

                <div className="text-right">
                  <span className="text-xl font-extrabold text-slate-800">{f.healthScore}%</span>
                  <span className="text-[10px] text-slate-400 block">{t("metrics.farmHealth", "Health")}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 mt-4 p-3 bg-slate-50 rounded-2xl text-xs">
                <div>
                  <span className="text-slate-400 text-[10px] block">{t("metrics.soilMoisture", "Root Moisture")}</span>
                  <span className={`font-bold ${f.soilMoisture < 35 ? 'text-amber-600' : 'text-emerald-600'}`}>
                    {f.soilMoisture}%
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">{t("mapPage.pestDanger", "Pest Risk")}</span>
                  <span className="font-semibold text-slate-800 truncate block">{f.pestRisk}</span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">{t("metrics.phLevel", "Soil pH")}</span>
                  <span className="font-semibold text-slate-800">{f.soilPH}</span>
                </div>
                <div>
                  <span className="text-slate-400 text-[10px] block">IoT Node</span>
                  <span className="font-semibold text-sky-700 truncate block">{f.sensorNode}</span>
                </div>
              </div>

              <p className="text-xs text-slate-600 mt-3 italic">
                "{f.recommendation}"
              </p>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
                {f.id === 'field-a' ? (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      triggerIrrigationValve('field-a', 35);
                    }}
                    className={`w-full py-2 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
                      activeValve.fieldA
                        ? 'bg-sky-500 text-white animate-pulse'
                        : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm'
                    }`}
                  >
                    <Droplets className="w-3.5 h-3.5" />
                    <span>{activeValve.fieldA ? t("dashboard.valveRunning", "Valve Running (35m)") : t("mapPage.triggerDrip", "Trigger Drip Irrigation")}</span>
                  </button>
                ) : (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedFieldId(f.id);
                    }}
                    className="w-full py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition-all"
                  >
                    {t("mapPage.inspectZone", "Inspect Zone Details")}
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
