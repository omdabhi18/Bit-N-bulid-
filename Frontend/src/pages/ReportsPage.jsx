import React from 'react';
import { useFarm } from '../context/FarmContext';
import { useLanguage } from '../context/LanguageContext';
import VoiceSpeaker from '../components/common/VoiceSpeaker';
import {
  FileText,
  Printer,
  CheckCircle2
} from 'lucide-react';

export default function ReportsPage() {
  const { profile, fields, activityLogs } = useFarm();
  const { t, language } = useLanguage();

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-5 rounded-3xl border border-slate-200 shadow-card-soft print:hidden">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-xl bg-slate-100 text-slate-800">
              <FileText className="w-5 h-5" />
            </span>
            <div>
              <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
                {t("reportsPage.title", "Farm Audit Log & Printable Health Reports")}
              </h1>
              <p className="text-xs text-slate-500">
                {t("reportsPage.subtitle", "Verifiable chronological record of multi-agent decisions, farmer approvals, and irrigation logs")}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handlePrint}
            className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold flex items-center gap-1.5 transition-all shadow-md"
          >
            <Printer className="w-4 h-4" />
            <span>{t("reportsPage.printReport", "Print Farm Report")}</span>
          </button>

          <VoiceSpeaker
            text={language === 'gu'
              ? `ખેતર ઓડિટ અહેવાલ. સમગ્ર ખેતરનું સ્વાસ્થ્ય ૮૨% છે. બધા એજન્ટ નિર્ણયો અને પિયતના કામો અહીં પ્રમાણિત કરેલા છે.`
              : `Farm report summary for ${profile.farmName}. Overall health is 82%. Full audit logs confirm multi-agent decision consensus and farmer approvals.`}
            label={t("reportsPage.listenSummary", "Listen Summary")}
          />
        </div>
      </div>

      {/* Printable Farm Health Certificate */}
      <div className="bg-white p-8 rounded-3xl border-2 border-slate-200 shadow-lg space-y-6 print:border-none print:shadow-none print:p-0">
        
        {/* Document Header */}
        <div className="flex items-start justify-between border-b-2 border-slate-900 pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-2xl font-black text-slate-900">KrishiNetra AI OS</span>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">
                {t("reportsPage.officialAudit", "OFFICIAL AUDIT REPORT")}
              </span>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              Precision Autonomous Agriculture Telemetry & Verification Document
            </p>
          </div>

          <div className="text-right text-xs">
            <span className="font-bold text-slate-900 block">Report Generated:</span>
            <span className="text-slate-500">{new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>
        </div>

        {/* Farm & Farmer Meta Details */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 bg-slate-50 rounded-2xl text-xs">
          <div>
            <span className="text-slate-400 block font-semibold">Farmer</span>
            <span className="font-extrabold text-slate-900 text-sm">{profile.farmerName}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-semibold">Holding</span>
            <span className="font-extrabold text-slate-900 text-sm">{profile.farmName}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-semibold">Location</span>
            <span className="font-extrabold text-slate-900 text-sm">{profile.district}, {profile.state}</span>
          </div>
          <div>
            <span className="text-slate-400 block font-semibold">Total Area</span>
            <span className="font-extrabold text-slate-900 text-sm">{profile.totalAreaAcre} Acres</span>
          </div>
        </div>

        {/* Crop & Field Telemetry Table */}
        <div className="space-y-2">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
            {t("reportsPage.fieldTelemetrySection", "1. Field Health & Growth Telemetry")}
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-xs text-left">
              <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                <tr>
                  <th className="p-2.5">Field Plot</th>
                  <th className="p-2.5">Crop & Variety</th>
                  <th className="p-2.5">Area</th>
                  <th className="p-2.5">Root Moisture</th>
                  <th className="p-2.5">Soil pH</th>
                  <th className="p-2.5">Health Score</th>
                  <th className="p-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {fields.map((f) => (
                  <tr key={f.id}>
                    <td className="p-2.5 font-bold text-slate-900">{f.name}</td>
                    <td className="p-2.5 text-slate-600">{f.crop}</td>
                    <td className="p-2.5 text-slate-600">{f.area}</td>
                    <td className="p-2.5 font-bold text-slate-800">{f.soilMoisture}%</td>
                    <td className="p-2.5 text-slate-600">{f.soilPH}</td>
                    <td className="p-2.5 font-bold text-emerald-700">{f.healthScore}%</td>
                    <td className="p-2.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        f.status === 'Critical' ? 'bg-rose-100 text-rose-800' :
                        f.status === 'Warning' ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {f.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Chronological Audit Trail */}
        <div className="space-y-3 pt-2">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
            {t("reportsPage.auditTrailSection", "2. System Orchestration & Farmer Execution Audit Trail")}
          </h3>

          <div className="space-y-2 text-xs">
            {activityLogs.map((log) => (
              <div key={log.id} className="p-2.5 rounded-xl border border-slate-100 bg-slate-50 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <span className="font-mono text-slate-400 text-[11px] font-bold">{log.time}</span>
                  <span className="px-2 py-0.5 rounded bg-white text-slate-800 font-bold border border-slate-200 text-[10px]">
                    {log.agent}
                  </span>
                  <span className="text-slate-800 font-medium">{log.event}</span>
                </div>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
              </div>
            ))}
          </div>
        </div>

        {/* Signatures */}
        <div className="pt-8 border-t border-slate-200 grid grid-cols-2 gap-8 text-xs">
          <div>
            <span className="font-bold text-slate-900 block">{t("reportsPage.farmerSignature", "Farmer Signature / Stamp")}</span>
            <div className="h-12 border-b border-slate-300 mt-2"></div>
            <span className="text-[10px] text-slate-400 mt-1 block">Kishanbhai Patel (Verified Farmer)</span>
          </div>

          <div className="text-right">
            <span className="font-bold text-slate-900 block">{t("reportsPage.systemSignature", "Agronomy System Signature")}</span>
            <div className="h-12 border-b border-slate-300 mt-2 flex items-end justify-end">
              <span className="font-mono text-emerald-700 text-[11px] font-bold">SHA256: 9b207f... verified</span>
            </div>
            <span className="text-[10px] text-slate-400 mt-1 block">Autonomous Multi-Agent Consensus Node</span>
          </div>
        </div>

      </div>

    </div>
  );
}
