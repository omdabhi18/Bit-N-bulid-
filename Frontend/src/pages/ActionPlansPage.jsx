import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  FileCheck2,
  CheckCircle2,
  Clock,
  IndianRupee,
  CloudSun,
  Shield,
  Wrench,
  Play
} from 'lucide-react';

export default function ActionPlansPage() {
  const { actionPlans, approvePlan, triggerIrrigationValve, activeValve } = useFarm();
  const { t, language } = useLanguage();
  const [selectedPlan, setSelectedPlan] = useState(actionPlans[0]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-teal-100 text-teal-800">
              <FileCheck2 className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("plansPage.title", "Constrained Farm Action Plans")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("plansPage.subtitle", "Action schedules verified against budget caps, weather safety windows, water supplies, and chemical safety")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <VoiceSpeaker
            text={language === 'gu'
              ? "ખેતી માટે એક્શન પ્લાન સેન્ટર. ખેતર A માટે પિયત પ્લાન ૧૦૨૪ સાંજે ૬:૦૦ વાગ્યે શરૂ થશે જેનો અંદાજિત ખર્ચ ₹૪૫ છે."
              : `Action plan management center. Active plan 1024 for Field A schedules automated drip irrigation between 18:00 and 18:35 today with estimated cost of 45 rupees.`}
            label={t("plansPage.listenPlans", "Listen Plans")}
          />
        </div>
      </div>

      {/* Constraints Matrix Highlights */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-card-soft">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <IndianRupee className="w-4 h-4 text-emerald-600" />
            <span>{t("plansPage.costConstraint", "Cost Constraint")}</span>
          </div>
          <p className="text-lg font-extrabold text-slate-900 mt-1">₹45 / ₹150 Cap</p>
          <span className="text-[11px] text-emerald-600 font-bold">Within Budget (68% saved)</span>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-card-soft">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <CloudSun className="w-4 h-4 text-sky-600" />
            <span>{t("plansPage.weatherWindow", "Weather Window")}</span>
          </div>
          <p className="text-lg font-extrabold text-slate-900 mt-1">18:00 - 20:00 IST</p>
          <span className="text-[11px] text-sky-600 font-bold">Low Wind & Zero Rain</span>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-card-soft">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <Shield className="w-4 h-4 text-purple-600" />
            <span>{t("plansPage.safetyPpe", "Safety & PPE")}</span>
          </div>
          <p className="text-lg font-extrabold text-slate-900 mt-1">Verified Safe</p>
          <span className="text-[11px] text-purple-600 font-bold">Safe for Soil Ecology</span>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-slate-200 shadow-card-soft">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-semibold">
            <Wrench className="w-4 h-4 text-amber-600" />
            <span>{t("plansPage.hardwareTarget", "Hardware Target")}</span>
          </div>
          <p className="text-lg font-extrabold text-slate-900 mt-1">Solenoid SV-01</p>
          <span className="text-[11px] text-emerald-600 font-bold">Armed & Ready</span>
        </div>
      </div>

      {/* Main Action Plan Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Plan Selector Cards */}
        <div className="lg:col-span-1 space-y-3">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
            {t("plansPage.queueTitle", "Generated Plans Queue")}
          </h3>

          {actionPlans.map((plan) => {
            const isSelected = selectedPlan?.id === plan.id;
            return (
              <div
                key={plan.id}
                onClick={() => setSelectedPlan(plan)}
                className={`p-4 rounded-2xl border-2 transition-all cursor-pointer bg-white ${
                  isSelected
                    ? 'border-emerald-500 shadow-lg ring-4 ring-emerald-500/10'
                    : 'border-slate-200 hover:border-slate-300 shadow-card-soft'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-400">{plan.id}</span>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase ${
                    plan.status === 'Approved' ? 'bg-emerald-100 text-emerald-800' :
                    plan.status === 'Scheduled' ? 'bg-sky-100 text-sky-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {plan.status}
                  </span>
                </div>

                <h4 className="font-bold text-slate-900 text-sm mt-1">{plan.title}</h4>
                <p className="text-xs text-slate-500 mt-0.5">{plan.targetField}</p>

                <div className="flex items-center justify-between mt-3 text-[11px] text-slate-600 pt-2 border-t border-slate-100">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-400" />
                    {plan.scheduledTime}
                  </span>
                  <span className="font-bold text-emerald-700">₹{plan.estimatedCost}</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right 2 Columns: Detailed Plan Blueprint */}
        {selectedPlan && (
          <div className="lg:col-span-2 bg-white rounded-3xl p-6 border border-slate-200/80 shadow-card-soft space-y-5">
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-100">
              <div>
                <span className="text-xs font-extrabold text-emerald-700 uppercase tracking-wider bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
                  Plan #{selectedPlan.id}
                </span>
                <h2 className="text-xl font-bold text-slate-900 mt-2">{selectedPlan.title}</h2>
                <p className="text-xs text-slate-500">{selectedPlan.targetField} • {selectedPlan.assignedTo}</p>
              </div>

              <VoiceSpeaker
                text={`${selectedPlan.title}. Action: ${selectedPlan.actionType}. Scheduled: ${selectedPlan.scheduledTime}. Estimated cost: ₹${selectedPlan.estimatedCost}.`}
                label={t("plansPage.listenPlans", "Read Plan")}
              />
            </div>

            {/* Constraints Table */}
            <div className="space-y-3">
              <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                {t("plansPage.solverTitle", "Multi-Constraint Solver Verification:")}
              </h4>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                  <span className="font-bold text-slate-500 text-[11px] block">💰 {t("plansPage.costConstraint", "Cost & Budget Limit")}</span>
                  <p className="font-extrabold text-slate-800">{selectedPlan.constraints.costBudget}</p>
                  <span className="text-[10px] text-emerald-600 font-semibold block">Electricity & inputs calculated</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                  <span className="font-bold text-slate-500 text-[11px] block">🌦️ {t("plansPage.weatherWindow", "Weather Safe Window")}</span>
                  <p className="font-extrabold text-slate-800">{selectedPlan.constraints.weatherWindow}</p>
                  <span className="text-[10px] text-sky-600 font-semibold block">Verified by Meteorological Agent</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                  <span className="font-bold text-slate-500 text-[11px] block">💧 {t("common.volume", "Water Volume")}</span>
                  <p className="font-extrabold text-slate-800">{selectedPlan.constraints.waterAvailability}</p>
                  <span className="text-[10px] text-emerald-600 font-semibold block">Volume: {selectedPlan.waterVolume}</span>
                </div>

                <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                  <span className="font-bold text-slate-500 text-[11px] block">🛡️ {t("plansPage.safetyPpe", "Safety Protocol")}</span>
                  <p className="font-extrabold text-slate-800">{selectedPlan.constraints.safetyProtocols}</p>
                  <span className="text-[10px] text-purple-600 font-semibold block">Zero drift & zero toxic runoff</span>
                </div>
              </div>
            </div>

            {/* Execution Controls */}
            <div className="pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => alert(`Plan ${selectedPlan.id} opened in schedule editor.`)}
                  className="px-4 py-2.5 rounded-xl border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-bold"
                >
                  {t("plansPage.modifyPlan", "Modify Plan")}
                </button>
                <button
                  onClick={() => alert(`Plan ${selectedPlan.id} cancelled.`)}
                  className="px-4 py-2.5 rounded-xl border border-slate-200 hover:bg-rose-50 hover:text-rose-700 text-slate-600 text-xs font-bold"
                >
                  {t("common.cancel", "Cancel")}
                </button>
              </div>

              <div className="flex items-center gap-2">
                {selectedPlan.id === 'PLAN-1024' && (
                  <button
                    onClick={() => triggerIrrigationValve('field-a', 35)}
                    className={`px-5 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                      activeValve.fieldA
                        ? 'bg-sky-500 text-white animate-pulse'
                        : 'bg-sky-50 text-sky-700 hover:bg-sky-100 border border-sky-200'
                    }`}
                  >
                    <Play className="w-3.5 h-3.5" />
                    <span>{activeValve.fieldA ? t("dashboard.valveRunning", "Valve Running") : t("plansPage.executeNow", "Execute Solenoid Now")}</span>
                  </button>
                )}

                {selectedPlan.status !== 'Approved' && (
                  <button
                    onClick={() => approvePlan(selectedPlan.id)}
                    className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 text-white text-xs font-bold shadow-md shadow-emerald-500/20 flex items-center gap-1.5"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{t("plansPage.approveDispatch", "Approve & Dispatch Plan")}</span>
                  </button>
                )}
              </div>
            </div>

          </div>
        )}

      </div>

    </div>
  );
}
