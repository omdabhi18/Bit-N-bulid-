import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  AlertTriangle,
  Droplets,
  Bug,
  Sprout,
  CloudRain,
  TrendingUp,
  FileCheck2,
  Search
} from 'lucide-react';

export default function RiskDetectionPage() {
  const { risks, generatePlanFromRisk, setSelectedFieldId } = useFarm();
  const { t, language } = useLanguage();
  const navigate = useNavigate();

  const getRiskIcon = (category) => {
    if (category.includes('Water') || category.includes('પાણી')) return <Droplets className="w-5 h-5 text-amber-500" />;
    if (category.includes('Pest') || category.includes('જીવાત')) return <Bug className="w-5 h-5 text-rose-500" />;
    if (category.includes('Nutrient') || category.includes('પોષક')) return <Sprout className="w-5 h-5 text-emerald-500" />;
    if (category.includes('Weather') || category.includes('હવામાન')) return <CloudRain className="w-5 h-5 text-sky-500" />;
    return <TrendingUp className="w-5 h-5 text-purple-500" />;
  };

  const handleInspect = (fieldName) => {
    if (fieldName.includes('A')) setSelectedFieldId('field-a');
    else if (fieldName.includes('B')) setSelectedFieldId('field-b');
    else setSelectedFieldId('field-c');
    navigate('/map');
  };

  const handleGenerate = (risk) => {
    generatePlanFromRisk(risk);
    navigate('/action-plans');
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-rose-100 text-rose-800">
              <AlertTriangle className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("risksPage.title", "Autonomous Risk Detection Matrix")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("risksPage.subtitle", "Multi-factor risk modeling integrating IoT root moisture, satellite canopy alerts, and microclimate")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? "જોખમ તપાસ રિપોર્ટ. બે મુખ્ય જોખમો છે: ખેતર A માં પાણીની અછત ૮૮% સંભાવના સાથે, અને ખેતર B માં જીવાતનો ભય ૭૮% સંભાવના સાથે છે."
              : "Risk detection report. There are two primary risks active: Water stress in Field A with 88% probability, and high pest risk in Field B with 78% probability."}
            label={t("risksPage.listenRisks", "Listen Risks")}
          />
        </div>
      </div>

      {/* Summary Stat Ribbon */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-rose-50 border border-rose-200 p-4 rounded-2xl">
          <span className="text-xs font-semibold text-rose-800">{t("risksPage.criticalCount", "Critical Risks")}</span>
          <p className="text-2xl font-extrabold text-rose-900 mt-1">1</p>
          <span className="text-[11px] text-rose-700">Pink Bollworm / Aphids</span>
        </div>
        <div className="bg-amber-50 border border-amber-200 p-4 rounded-2xl">
          <span className="text-xs font-semibold text-amber-800">{t("risksPage.highCount", "High Risks")}</span>
          <p className="text-2xl font-extrabold text-amber-900 mt-1">1</p>
          <span className="text-[11px] text-amber-700">Water Deficit (Field A)</span>
        </div>
        <div className="bg-sky-50 border border-sky-200 p-4 rounded-2xl">
          <span className="text-xs font-semibold text-sky-800">{t("risksPage.mediumCount", "Medium Risks")}</span>
          <p className="text-2xl font-extrabold text-sky-900 mt-1">2</p>
          <span className="text-[11px] text-sky-700">Soil P & Wind Alert</span>
        </div>
        <div className="bg-emerald-50 border border-emerald-200 p-4 rounded-2xl">
          <span className="text-xs font-semibold text-emerald-800">{t("risksPage.protectedHealth", "Field Health Protected")}</span>
          <p className="text-2xl font-extrabold text-emerald-900 mt-1">82%</p>
          <span className="text-[11px] text-emerald-700">Autonomous Monitoring</span>
        </div>
      </div>

      {/* Risk Cards List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {risks.map((risk) => (
          <div
            key={risk.id}
            className={`p-6 rounded-3xl bg-white border-2 shadow-card-soft transition-all ${
              risk.severity === 'Critical' ? 'border-rose-300' :
              risk.severity === 'High' ? 'border-amber-300' : 'border-slate-200'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2.5 rounded-2xl bg-slate-100">
                  {getRiskIcon(risk.category)}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase ${
                      risk.severity === 'Critical' ? 'bg-rose-100 text-rose-800' :
                      risk.severity === 'High' ? 'bg-amber-100 text-amber-800' : 'bg-sky-100 text-sky-800'
                    }`}>
                      {risk.severity} {t("common.priority", "Severity")}
                    </span>
                    <span className="text-xs font-bold text-slate-500">{risk.field}</span>
                  </div>
                  <h3 className="text-base font-bold text-slate-900 mt-1">{risk.category}</h3>
                </div>
              </div>

              <div className="text-right">
                <span className="text-2xl font-extrabold text-slate-900">{risk.probability}%</span>
                <span className="text-[10px] text-slate-400 block font-semibold">{t("common.confidence", "Probability")}</span>
              </div>
            </div>

            {/* Probability Progress Bar */}
            <div className="w-full bg-slate-100 h-2 rounded-full mt-4 overflow-hidden">
              <div
                className={`h-full rounded-full ${
                  risk.probability > 75 ? 'bg-rose-500' :
                  risk.probability > 60 ? 'bg-amber-500' : 'bg-emerald-500'
                }`}
                style={{ width: `${risk.probability}%` }}
              />
            </div>

            {/* Detected Indicators */}
            <div className="mt-4 space-y-1.5 bg-slate-50 p-3.5 rounded-2xl border border-slate-100 text-xs">
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                {t("risksPage.detectedIndicators", "Detected Sensor & Satellite Indicators:")}
              </span>
              {risk.indicators.map((ind, i) => (
                <div key={i} className="flex items-start gap-2 text-slate-700">
                  <span className="text-emerald-600 font-bold">•</span>
                  <span>{ind}</span>
                </div>
              ))}
            </div>

            {/* Recommended Action */}
            <div className="mt-4 p-3 rounded-2xl bg-emerald-50/70 border border-emerald-100 text-xs">
              <span className="font-bold text-emerald-900 block">{t("risksPage.recommendedIntervention", "AI Recommended Intervention:")}</span>
              <p className="text-emerald-800 mt-0.5">{risk.recommendedAction}</p>
            </div>

            {/* Action Buttons */}
            <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
              <button
                onClick={() => handleInspect(risk.field)}
                className="py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold transition-all flex items-center gap-1.5"
              >
                <Search className="w-3.5 h-3.5" />
                <span>{t("common.inspect", "Inspect Field")}</span>
              </button>

              <button
                onClick={() => handleGenerate(risk)}
                className="py-2.5 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white text-xs font-bold shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5"
              >
                <FileCheck2 className="w-3.5 h-3.5" />
                <span>{risk.planGenerated ? t("risksPage.viewActionPlan", "View Action Plan") : t("common.generatePlan", "Generate Action Plan")}</span>
              </button>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
