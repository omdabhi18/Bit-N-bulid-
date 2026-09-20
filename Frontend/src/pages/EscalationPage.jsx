import React, { useState } from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  UserCheck,
  AlertTriangle,
  Send,
  PhoneCall,
  Building
} from 'lucide-react';

export default function EscalationPage() {
  const { escalations, submitEscalation } = useFarm();
  const { t, language } = useLanguage();
  const [showModal, setShowModal] = useState(false);
  const [issueDescription, setIssueDescription] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('BT Cotton');

  const handleEscalate = (e) => {
    e.preventDefault();
    if (!issueDescription.trim()) return;

    submitEscalation({
      field: "Field A (Cotton)",
      crop: selectedCrop,
      issue: issueDescription,
      aiConfidence: 54,
      reason: "Farmer initiated agronomy second opinion request",
      assignedAgronomist: "Dr. Arvind Dave (Senior Agronomist, JAU)",
      telemetrySnapshot: { moisture: "31.4%", soilPH: "6.8", nitrogen: "82 mg/kg", phosphorus: "14 mg/kg" },
      agronomistNotes: "Ticket created. University agronomy desk will review within 2 hours."
    });

    setIssueDescription('');
    setShowModal(false);
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-purple-100 text-purple-800">
              <UserCheck className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("escalationPage.title", "University Agronomist & Expert Escalation")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("escalationPage.subtitle", "Direct human-in-the-loop expert review when AI model confidence drops below safety threshold")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold flex items-center gap-1.5 transition-all shadow-md"
          >
            <Send className="w-4 h-4" />
            <span>{t("escalationPage.requestCall", "Request Agronomist Call")}</span>
          </button>

          <VoiceSpeaker
            text={language === 'gu'
              ? "કૃષિ નિષ્ણાત સહાય. જ્યારે AI ની ચોકસાઈ ઓછી હોય ત્યારે સીધા યુનિવર્સિટી વૈજ્ઞાનિકનો સંપર્ક થાય છે."
              : "Agronomist escalation desk. Whenever AI confidence is below threshold, your case is forwarded to University agricultural scientists."}
            label={t("escalationPage.listenOverview", "Listen Overview")}
          />
        </div>
      </div>

      {/* Safety Guardrail Banner */}
      <div className="bg-amber-50 border border-amber-200 p-5 rounded-3xl flex items-start gap-3 text-xs text-amber-900">
        <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-extrabold text-sm block">{t("escalationPage.safeguardTitle", "Human-in-the-Loop Safeguard")}</span>
          <p className="text-amber-800 leading-relaxed">
            {t("escalationPage.safeguardDesc", "AI recommendations with confidence below 65% are marked for expert human validation. Junagadh Agricultural University (JAU) & MPKV specialists review your sensor logs, thermal scans, and crop photo before authorizing high-cost chemical interventions.")}
          </p>
        </div>
      </div>

      {/* Escalation Tickets List */}
      <div className="space-y-4">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-1">
          {t("escalationPage.activeTickets", "Active Expert Review Tickets")}
        </h3>

        {escalations.map((ticket) => (
          <div
            key={ticket.id}
            className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-card-soft space-y-4"
          >
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 pb-3 border-b border-slate-100">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-100 text-amber-800">
                    {ticket.status}
                  </span>
                  <span className="text-xs font-bold text-slate-400">Ticket #{ticket.id}</span>
                  <span className="text-xs text-slate-400">• {ticket.submittedAt}</span>
                </div>
                <h3 className="text-base font-bold text-slate-900 mt-1">{ticket.issue}</h3>
                <p className="text-xs text-slate-500">{ticket.crop} • {ticket.field}</p>
              </div>

              <div className="text-right shrink-0">
                <span className="text-xs font-bold text-rose-600 bg-rose-50 px-2.5 py-1 rounded-full border border-rose-200 block">
                  AI {t("common.confidence", "Confidence")}: {ticket.aiConfidence}% (Flagged)
                </span>
                <span className="text-[10px] text-slate-400 mt-1 block">Low Confidence Trigger</span>
              </div>
            </div>

            {/* Reason & Telemetry Snapshot */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                <span className="font-bold text-slate-700 block">Root Cause:</span>
                <p className="text-slate-600 leading-relaxed">{ticket.reason}</p>
              </div>

              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
                <span className="font-bold text-slate-700 block">Attached Telemetry Snapshot:</span>
                <div className="grid grid-cols-2 gap-1 text-[11px] text-slate-600">
                  <span>Moisture: {ticket.telemetrySnapshot.moisture}</span>
                  <span>Soil pH: {ticket.telemetrySnapshot.soilPH}</span>
                  <span>Nitrogen: {ticket.telemetrySnapshot.nitrogen}</span>
                  <span>Phosphorus: {ticket.telemetrySnapshot.phosphorus}</span>
                </div>
              </div>
            </div>

            {/* Agronomist Notes & Direct Connect */}
            <div className="p-4 rounded-2xl bg-purple-50/60 border border-purple-100 text-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-purple-900 flex items-center gap-1.5">
                  <Building className="w-4 h-4 text-purple-600" />
                  Assigned Scientist: {ticket.assignedAgronomist}
                </span>
                <span className="text-[11px] text-purple-700 font-semibold">Callback Scheduled</span>
              </div>
              <p className="text-purple-800 leading-relaxed italic">
                "{ticket.agronomistNotes}"
              </p>
            </div>

            <div className="pt-2 flex items-center justify-end gap-2">
              <a
                href="tel:18001801551"
                className="px-4 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-800 text-xs font-bold flex items-center gap-1.5 transition-all border border-emerald-200"
              >
                <PhoneCall className="w-3.5 h-3.5 text-emerald-600" />
                <span>{t("escalationPage.callCenter", "Call Kisan Call Center (1800-180-1551)")}</span>
              </a>
            </div>

          </div>
        ))}
      </div>

      {/* Request Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-200 animate-in fade-in zoom-in-95">
            <h3 className="text-base font-bold text-slate-900">{t("escalationPage.requestCall", "Request Agronomist Review")}</h3>
            <p className="text-xs text-slate-500 mt-0.5">Attach your current soil & leaf telemetry to a university scientist</p>

            <form onSubmit={handleEscalate} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Affected Crop</label>
                <select
                  value={selectedCrop}
                  onChange={(e) => setSelectedCrop(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-purple-500"
                >
                  <option value="BT Cotton">Field A: BT Cotton (કપાસ)</option>
                  <option value="Sharbati Wheat">Field B: Sharbati Wheat (ઘઉં)</option>
                  <option value="Groundnut GG-20">Field C: Groundnut (મગફળી)</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Describe Symptoms</label>
                <textarea
                  value={issueDescription}
                  onChange={(e) => setIssueDescription(e.target.value)}
                  rows="3"
                  placeholder="e.g. Yellow leaf spots with necrosis spreading after rain..."
                  className="w-full p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:border-purple-500"
                  required
                />
              </div>

              <div className="pt-3 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-600 font-bold hover:bg-slate-100"
                >
                  {t("common.cancel", "Cancel")}
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold"
                >
                  Submit Ticket
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
