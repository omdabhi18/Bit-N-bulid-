import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  Lightbulb,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Sparkles,
  ShieldCheck,
  Info
} from 'lucide-react';

export default function AIAdvisoryPage() {
  const { advisories, approveAdvisory, rejectAdvisory } = useFarm();
  const { t, language } = useLanguage();
  const [activeModalAdvisory, setActiveModalAdvisory] = useState(null);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-amber-100 text-amber-800">
              <Lightbulb className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("advisoryPage.title", "Explainable AI Advisory Engine")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("advisoryPage.subtitle", "Transparent agronomical recommendations backed by root telemetry, degree-day models, and multi-agent consensus")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? "પારદર્શક AI કૃષિ સલાહ પોર્ટલ. દરેક ભલામણ સાથે જમીનનો ભેજ અને હવામાનના કારણો આપેલા છે જેથી ખેડૂત પૂરા વિશ્વાસ સાથે નિર્ણય લઈ શકે."
              : "Explainable AI Advisory portal. Every recommendation is accompanied by the underlying environmental factors and agent logic so you have full confidence before execution."}
            label={t("advisoryPage.explainAdvisories", "Explain Advisories")}
          />
        </div>
      </div>

      {/* Trust & Transparency Banner */}
      <div className="bg-gradient-to-r from-emerald-50 via-teal-50 to-sky-50 border border-emerald-200 p-4 rounded-3xl flex items-center gap-3 text-xs text-emerald-900">
        <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0" />
        <div>
          <span className="font-extrabold block">{t("advisoryPage.zeroBlackBox", "Zero Black-Box Decisions")}:</span>
          {t("advisoryPage.zeroBlackBoxDesc", "Farmers deserve to know exactly why a dosage, watering window, or chemical treatment was suggested. Click 'Ask AI Why?' on any advisory to trace the multi-agent reasoning chain.")}
        </div>
      </div>

      {/* Advisory Cards List */}
      <div className="space-y-6">
        {advisories.map((adv) => {
          const isApproved = adv.status === 'Approved';
          const isRejected = adv.status === 'Rejected';

          const titleDisplay = language === 'gu' && adv.titleGu ? adv.titleGu :
                               language === 'hi' && adv.titleHi ? adv.titleHi : adv.title;

          return (
            <div
              key={adv.id}
              className={`p-6 rounded-3xl bg-white border-2 shadow-card-soft transition-all relative overflow-hidden ${
                isApproved ? 'border-emerald-400 bg-emerald-50/20' :
                isRejected ? 'border-slate-300 opacity-60' : 'border-slate-200 hover:border-amber-300'
              }`}
            >
              {/* Header Details */}
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                <div className="space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase ${
                      adv.priority === 'High' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {adv.priority} {t("common.priority", "Priority")}
                    </span>
                    <span className="text-xs font-bold text-slate-500">{adv.field}</span>
                    <span className="text-[11px] text-slate-400">• {adv.timestamp}</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      isApproved ? 'bg-emerald-100 text-emerald-800' :
                      isRejected ? 'bg-slate-200 text-slate-700' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {adv.status}
                    </span>
                  </div>

                  <h3 className="text-lg font-bold text-slate-900">{titleDisplay}</h3>
                  <p className="text-xs sm:text-sm text-slate-600 max-w-3xl leading-relaxed">
                    {adv.orchestratorSummary}
                  </p>
                </div>

                <div className="flex items-center sm:flex-col items-end gap-2 shrink-0">
                  <div className="text-right">
                    <div className="flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4 text-emerald-600" />
                      <span className="text-xl font-extrabold text-emerald-700">{adv.confidenceScore}%</span>
                    </div>
                    <span className="text-[10px] text-slate-400 font-semibold block">{t("common.confidence", "AI Confidence")}</span>
                  </div>

                  <VoiceSpeaker
                    text={`${titleDisplay}. ${adv.orchestratorSummary}`}
                    label={t("common.readAloud", "Listen")}
                  />
                </div>
              </div>

              {/* Action Blueprint Pill Box */}
              <div className="mt-4 p-4 rounded-2xl bg-slate-50 border border-slate-100 grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs">
                <div>
                  <span className="text-[10px] text-slate-400 block font-medium">{t("common.details", "Intervention")}</span>
                  <span className="font-extrabold text-slate-800">{adv.actionDetails.action}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 block font-medium">{t("common.volume", "Volume")}</span>
                  <span className="font-extrabold text-slate-800">{adv.actionDetails.volume}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 block font-medium">{t("common.duration", "Duration")}</span>
                  <span className="font-extrabold text-slate-800">{adv.actionDetails.duration}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 block font-medium">Sub-Zone</span>
                  <span className="font-bold text-slate-800 truncate block">{adv.actionDetails.zone}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 block font-medium">{t("common.cost", "Cost Estimate")}</span>
                  <span className="font-bold text-emerald-700">{adv.actionDetails.costEstimate}</span>
                </div>
              </div>

              {/* Explainability Factors Breakdown */}
              <div className="mt-4 pt-4 border-t border-slate-100">
                <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5 mb-2.5">
                  <Info className="w-3.5 h-3.5 text-emerald-600" />
                  {t("advisoryPage.influencingTelemetry", "Telemetry Influencing this Recommendation:")}
                </span>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                  {adv.explainability.factors.map((factor, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-white border border-slate-200 text-xs">
                      <div className="flex items-center justify-between">
                        <span className="text-slate-500 font-medium truncate">{factor.name}</span>
                        <span className="font-extrabold text-slate-900">{factor.value}</span>
                      </div>
                      <div className="flex items-center justify-between mt-1 text-[10px]">
                        <span className="text-amber-700 font-semibold">{factor.impact}</span>
                        <span className="text-slate-400">Baseline: {factor.threshold}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Bar */}
              <div className="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
                <button
                  onClick={() => setActiveModalAdvisory(adv)}
                  className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition-all flex items-center gap-1.5"
                >
                  <HelpCircle className="w-4 h-4 text-emerald-600" />
                  <span>{t("common.askWhy", "Ask AI Why?")}</span>
                </button>

                {!isApproved && !isRejected ? (
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => rejectAdvisory(adv.id)}
                      className="px-4 py-2 rounded-xl border border-slate-200 hover:bg-rose-50 hover:text-rose-700 text-slate-600 text-xs font-bold transition-all flex items-center gap-1"
                    >
                      <XCircle className="w-4 h-4" />
                      <span>{t("common.reject", "Reject")}</span>
                    </button>
                    <button
                      onClick={() => approveAdvisory(adv.id)}
                      className="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 text-white text-xs font-bold shadow-md shadow-emerald-500/20 transition-all flex items-center gap-1.5"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span>{t("common.approve", "Approve Advisory")}</span>
                    </button>
                  </div>
                ) : (
                  <span className="text-xs font-bold text-slate-500">
                    {isApproved ? "✅ Recommendation has been scheduled." : "❌ Recommendation dismissed by farmer."}
                  </span>
                )}
              </div>

            </div>
          );
        })}
      </div>

      {/* "Ask AI Why?" Deep Explainability Modal */}
      {activeModalAdvisory && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 max-w-xl w-full shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95">
            <div className="flex items-start justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <span className="p-2 rounded-xl bg-emerald-100 text-emerald-800">
                  <Sparkles className="w-5 h-5 text-emerald-600" />
                </span>
                <div>
                  <h3 className="font-extrabold text-slate-900 text-base">
                    {t("advisoryPage.reasoningPath", "Explainable AI Reasoning Path")}
                  </h3>
                  <p className="text-xs text-slate-500">{t("advisoryPage.multiAgentTrail", "Multi-Agent Consensus Trail")}</p>
                </div>
              </div>
              <button
                onClick={() => setActiveModalAdvisory(null)}
                className="text-slate-400 hover:text-slate-600 p-1 font-bold"
              >
                ✕
              </button>
            </div>

            <div className="mt-4 space-y-4 text-xs">
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 leading-relaxed text-slate-700">
                <span className="font-bold text-slate-900 block mb-1">
                  {t("advisoryPage.synthesizedRationale", "Synthesized Decision Rationale:")}
                </span>
                {activeModalAdvisory.explainability.whyText}
              </div>

              <div className="space-y-2">
                <span className="font-bold text-slate-800 block">
                  {t("advisoryPage.participatingAgents", "Participating Specialized Agents:")}
                </span>
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between p-2 rounded-xl bg-emerald-50/50 border border-emerald-100 text-[11px]">
                    <span className="font-semibold text-emerald-900">Soil & Root Agent</span>
                    <span className="text-emerald-700">Flagged critical root moisture deficit (31.4%)</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-xl bg-sky-50/50 border border-sky-100 text-[11px]">
                    <span className="font-semibold text-sky-900">Meteorological Agent</span>
                    <span className="text-sky-700">Confirmed under 15% rain risk for next 24 hours</span>
                  </div>
                  <div className="flex items-center justify-between p-2 rounded-xl bg-purple-50/50 border border-purple-100 text-[11px]">
                    <span className="font-semibold text-purple-900">Constrained Planner Agent</span>
                    <span className="text-purple-700">Optimized 18:00 - 20:00 watering window (low evaporation)</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setActiveModalAdvisory(null)}
                className="px-5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold"
              >
                {t("advisoryPage.understoodClose", "Understood & Close")}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
